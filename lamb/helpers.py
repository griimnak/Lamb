from datetime import datetime
import json
import re

from .bot import memory


def datetime_now():
    """Returns current date and time in preferred format"""
    return datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")


def load_settings():
    """Loads contents of settings/ into lamb.memory object"""
    try:
        with open('settings/config.json', 'r') as maincfg_f:
            config = json.load(maincfg_f)
            memory.update(config)

        with open(f'settings/strings/{memory["strings_locale"]}.json', 'r') as strings_f:
            strings = json.load(strings_f)
            memory["strings"] = strings

        # set state to active
        memory["active"] = True
        return print(f'[{datetime_now()}] Settings loaded.')
    except Exception as e:
        exit("failure: settings/config.json not loaded!\n"+str(e))


regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
