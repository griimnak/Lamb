from urllib import parse
import requests

from lamb import memory


class LoLException(Exception):
    """Exception system inspired by RiotWatcher on github"""
    def __init__(self, err):
        self.error = err

    def __str__(self):
        return self.error


class LoLTracker:
    """Tracks Summoner's Rift stats via riot api
    :param str app_token: input app token to tracker instance
    :usage instance = LeagueTracker(token)
        try:
           instance.get_basic_info("griimnak")
        except LoLException as err:
            ctx.send(err)"""
    def __init__(self, app_token):
        self.base_url = f'https://{memory["riot_api"]["region"]}.api.riotgames.com/lol'
        self.cdn_url = 'https://ddragon.leagueoflegends.com/cdn'

        self.match_path = f'{self.base_url}/match/v4/matchlists/by-account'
        self.summoner_path = f'{self.base_url}/summoner/v4/summoners'
        self.mastery_path = f'{self.base_url}/champion-mastery/v4/champion-masteries/by-summoner'
        self.ranked_path = f'{self.base_url}/league/v4/entries/by-summoner'

        self.token = app_token
        self.lol_ver = memory["riot_api"]["lol_version"]

    @staticmethod
    def raise_status(response):
        if response.status_code == 400:
            raise LoLException("Bad request")
        elif response.status_code == 401:
            raise LoLException("Unauthorized")
        elif response.status_code == 404:
            raise LoLException("Game data not found")
        elif response.status_code == 429:
            raise LoLException("Too many requests")
        elif response.status_code == 500:
            raise LoLException("Internal server error")
        elif response.status_code == 503:
            raise LoLException("Service unavailable")
        else:
            response.raise_for_status()

    def json_get(self, request):
        """Prepare request and raise status code, return json if ok
        :param str request: request url
        :return dict req.json:"""

        req = requests.get(request)
        self.raise_status(req)
        return req.json()

    def get_basic_info(self, username):
        """Return basic info like player level, games played etc.
        :param tuple username: input username tuple that is converted into a str
        :return dict json_from(riot):"""

        username = parse.quote(" ".join(username))
        return self.json_get(f'{self.summoner_path}/by-name/{username}?api_key={self.token}')

    def get_champ_by_id(self, champ_id):
        """Make request to champion.json from cdn, compare ids to param
        :param str champ_id:
        :return str champion:"""

        champion = "??"
        data = self.json_get(f'{self.cdn_url}/{self.lol_ver}/data/en_US/champion.json')

        for champ in data["data"]:
            if data["data"][champ]["key"] == str(champ_id):
                champion = data["data"][champ]["name"]

        return champion

    def get_draft_history(self, account_id):
        """Normal game mode history
        :param str account_id: input account id, typically from dict returned by basic request
        :return dict matches:"""

        index = 1
        matches = {}
        data = self.json_get(f'{self.match_path}/{account_id}?api_key={self.token}')

        for match in data["matches"]:
            matches[index] = match
            index += 1
            # limit to 20 games
            if index > 20:
                return matches
        return matches

    def get_mastery_data(self, summoner_id, champ_id):
        """Returns champion master info from champion id and summoner id
        :param str summoner_id: input summoner id from basic request
        :param str champ_id: input desired champion id"""
        return self.json_get(f'{self.mastery_path}/{summoner_id}/by-champion/{champ_id}?api_key={self.token}')

    def get_ranked_data(self, summoner_id):
        """Retrieves ranked data for summoner id, return default data dict if IndexError
        :param str summoner_id: input summoner id from basic request
        :return dict data:"""
        data = {
            "flex": {"tier": "Unranked", "rank": ""},
            "solo/duo": {"tier": "Unranked", "rank": ""}
        }

        req = self.json_get(f'{self.ranked_path}/{summoner_id}?api_key={self.token}')
        try:
            if req[0]["queueType"] == "RANKED_SOLO_5x5":
                data["solo/duo"]["tier"] = req[0]["tier"]
                data["solo/duo"]["rank"] = req[0]["rank"]
            elif req[0]["queueType"] == "RANKED_FLEX_SR":
                data["flex"]["tier"] = req[0]["tier"]
                data["flex"]["rank"] = req[0]["rank"]
        except IndexError:
            pass

        try:
            if req[1]["queueType"] == "RANKED_SOLO_5x5":
                data["solo/duo"]["tier"] = req[1]["tier"]
                data["solo/duo"]["rank"] = req[1]["rank"]
            elif req[1]["queueType"] == "RANKED_FLEX_SR":
                data["flex"]["tier"] = req[1]["tier"]
                data["flex"]["rank"] = req[1]["rank"]
        except IndexError:
            pass

        return data
