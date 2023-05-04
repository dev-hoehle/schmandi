import json
import os
import sys
from datetime import datetime

from helpers.general import *

sys.dont_write_bytecode = True
time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

def check_config():
    if not os.path.exists("config.json"):
        if os.path.exists("example.config.json"):
            print_failure_message("Please rename example.config.json to config.json and follow the setup instructions from the README file.")
            sys.exit()
        else:
            print_failure_message("config.json is missing. Please follow the setup instructions from the README file.")
            sys.exit()
    else:
        token = get_config_value("token")
        if not token:
            print_failure_message("Token is missing from config.json. Please follow the setup instructions from the README file.")
            sys.exit()

def get_config_value(key: str) -> str:
    with open("config.json", "r", encoding="UTF-8") as configfile:
        config = json.load(configfile)
        value = config.get(key)
        if not value:
            print_failure_message(f"[ERROR] Value for key '{key}' is missing from config.json. Please check the configuration file and try again.")
            sys.exit()
    configfile.close()
    return value
