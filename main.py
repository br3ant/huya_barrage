import argparse
import sys

import config
from huya_login import HuyaDriver
from start_danmu import start

parser = argparse.ArgumentParser()

parser.add_argument("--login", "-l", default=False, action="store_true",
                    help="login for cookies")

options = parser.parse_args(sys.argv[1:])
if options.login:
    room_id = config.get('room_id')
    driver = HuyaDriver(room_id)
    driver.close()
else:
    start()
