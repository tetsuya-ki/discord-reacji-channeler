import os
from os.path import join, dirname
from dotenv import load_dotenv
from logging import DEBUG, INFO, WARNING, ERROR

def if_env(str):
    if str is None or str.upper() != 'TRUE':
        return False
    else:
        return True

def get_log_level(str):
    if str is None:
        return WARNING
    upper_str = str.upper()
    if upper_str == 'DEBUG':
        return DEBUG
    elif upper_str == 'INFO':
        return INFO
    elif upper_str == 'ERROR':
        return ERROR
    else:
        return WARNING

def num_env(param):
    if str is None or not str(param).isdecimal():
        return 5
    else:
        return int(param)

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), 'files' + os.sep + '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
LOG_LEVEL = get_log_level(os.environ.get('LOG_LEVEL'))
IS_HEROKU = if_env(os.environ.get('IS_HEROKU'))
FIRST_REACTION_CHECK = if_env(os.environ.get('FIRST_REACTION_CHECK'))
REACJI_CHANNELER_PERMIT_WEBHOOK_ID = os.environ.get('REACJI_CHANNELER_PERMIT_WEBHOOK_ID')
ENABLE_SLASH_COMMAND_GUILD_ID_LIST = os.environ.get('ENABLE_SLASH_COMMAND_GUILD_ID_LIST')