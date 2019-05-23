import logging
import time

from urllib.request import urlopen

from environs import Env
from twilio.rest import Client


def read_config():
    logging_level = logging.getLevelName('INFO')
    logging_format = '[%(asctime)s] (%(process)d) {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
    logging_datefmt = '%Y-%m-%dT%H:%M:%SZ'

    logging.basicConfig(format=logging_format, datefmt=logging_datefmt)
    logger = logging.getLogger('__hey_you__')
    logger.setLevel(logging_level)  # Setting the level now will avoid getting logs from other libraries

    env = Env()
    return {
        'logger': logger,
        'watch_url': env.str('WATCH_URL'),
        'twilio_account_sid': env.str('TWILIO_ACCOUNT_SID'),
        'twilio_auth_token': env.str('TWILIO_AUTH_TOKEN'),
        'twilio_to': env.str('TWILIO_TO'),
        'twilio_from': env.str('TWILIO_FROM')
    }


def main(config):
    html = None
    while True:
        html_new = urlopen(config['watch_url']).read().decode('utf-8')

        if html is None:
            html = html_new
            config['logger'].info('First iteration')

        elif html != html_new:
            html = html_new
            config['logger'].info('Gotcha!')
            hey_you(config)

        else:
            config['logger'].info('No luck :(')

        time.sleep(30)


def hey_you(config):
    account_sid = config['twilio_account_sid']
    auth_token = config['twilio_auth_token']
    to = config['twilio_to']
    from_ = config['twilio_from']

    client = Client(account_sid, auth_token)
    call = client.calls.create(url='http://demo.twilio.com/docs/voice.xml', to=to, from_=from_)

    config['logger'].info(f'Calling: {call.sid}')


if __name__ == '__main__':
    config = read_config()
    main(config)
