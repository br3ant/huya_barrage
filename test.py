import html
import pickle
import re
import sys
import urllib.parse

from huya_login import HuyaDriver
from tars.models import *


def get_cookies():
    driver = HuyaDriver('520667')
    driver.colse()


def read_cookies():
    with open("./cookie/cookies.pkl", "rb") as cookiefile:
        cookies = pickle.load(cookiefile)
        cookie = [item["name"] + "=" + item["value"] for item in cookies]
        cookiestr = ';'.join(item for item in cookie)
        for c in cookie:
            if 'yyuid' in c:
                yyuid = c.split('=')[1]
        print(cookie)
        print(yyuid)


def unescape(string):
    string = urllib.parse.unquote(string)
    quoted = html.unescape(string).encode(sys.getfilesystemencoding()).decode('utf-8')
    # 转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), quoted)


if __name__ == '__main__':
    text = "哈哈哈999"
    # print(text)
    #
    # print(html.unescape(urllib.parse.quote("哈哈哈")))
    # text = "哈哈哈".encode('unicode-escape').decode()
    # print(len(text))
    # print(text)
    print(str.encode(text))
    # print(str.encode(text).decode('utf-8'))

    out_steam = tarscore.TarsOutputStream()
    out_steam.write(tarscore.string, 0, text)
    print(out_steam.getBuffer())

    in_steam = tarscore.TarsInputStream(out_steam.getBuffer())
    result = in_steam.read(tarscore.string, 0, True)

    print(result)
