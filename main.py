import sys

import config
from huya_login import HuyaDriver
from start_danmu import start

message = """
    功能列表：                                                                                
    1.获取cookies
    2.开启弹幕
    """
print(message)
choice_function = input('请选择:')

if choice_function == '1':
    room_id = config.get('room_id')
    driver = HuyaDriver(room_id)
    driver.colse()
elif choice_function == '2':
    start()
else:
    print('没有此功能')
    sys.exit(1)
