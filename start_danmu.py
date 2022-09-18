import asyncio
import os
import pickle
import re
from datetime import datetime

import requests

from analysis_danmu import analyze_bytes
from client import BarrageClient
from tars.models import *
from utils.barrage_logger import logger
from utils.print_log import print_red

last_send_s = time.time()
is_login = False
last_danmu = ''


# 平滑发动弹幕
async def send_barrage(dmc: BarrageClient, barrage_queue):
    while True:
        barrage = await barrage_queue.get()
        await dmc.send_barrage(barrage)
        await asyncio.sleep(2)


async def time_danmu(barrage_queue):
    if not config.get('time_effective'):
        return
    time_danmus = config.get('time_danmus')
    time_tick = config.get('time_danmu_tick')
    print(f'启动定时处理弹幕 content = {time_danmus} time_tick = {time_tick}')
    if time_danmus:
        # 休息1min再发
        await asyncio.sleep(10)
        for index in range(10000):
            if is_login:
                print(f'定时发送弹幕 time = {datetime.now().strftime("%y-%m-%d %I:%M:%S")}')
                danmu = time_danmus[index % len(time_danmus)]
                if danmu:
                    await barrage_queue.put(danmu)
            else:
                print('定时发送弹幕失败，未登录')
            await asyncio.sleep(int(time_tick))


async def receive_danmu(q, barrage_queue):
    while True:
        command = await q.get()

        if command.iCmdType == 7:
            await process_danmu(command, barrage_queue)
            # download_danmu(command)
            # analysis_danmu(command)
        elif command.iCmdType == 4:
            try:
                rsplist, unpacklen = Wup.unpackRspList(command.vData)

                for wup in rsplist:
                    print(f'wup = {wup.sFuncName}')
                    if wup.sFuncName == 'sendMessage':
                        bs = tarscore.TarsInputStream(wup.sBuffer)
                        newdata = bs.read(tarscore.mapclass(tarscore.string, tarscore.bytes), 0, True)
                        rsps = tarscore.TarsInputStream(newdata.get('tRsp'))
                        rsp = rsps.read(SendMessageRsp, 0, True)
                        print_red(
                            f'SendMessageRsp iStatus = {rsp.iStatus} sToast={rsp.sToast} UserInfo = {rsp.tNotice.tUserInfo.sNickName} Content = {rsp.tNotice.sContent} ')
            except:
                with open('log.txt', 'a+') as f:
                    print(f'sendMessage error = {command.vData}', file=f)
                print(f'sendMessage error = {command.vData}')

        elif command.iCmdType == 11:
            message = WSVerifyCookieRsp()
            cos = tarscore.TarsInputStream(command.vData)
            message.readFrom(cos)
            global is_login
            if message.iValidate == 0:
                print('登录成功')
                is_login = True
            else:
                logger.info('登录失败,请重新启动获取token')
                is_login = False
                try:
                    os.remove(config.get('cookie_path'))
                except:
                    pass
                return


def download_danmu(command):
    if command.iCmdType:
        print(command.iCmdType)

    data_eof = bytes(';;', encoding='utf-8')
    with open('danmu_data', 'ab') as f:
        f.write(command.vData)
        f.write(data_eof)


def analysis_danmu(command):
    stream = tarscore.TarsInputStream(command.vData)
    code = stream.read(tarscore.int64, 1, False)

    msg = stream.read(tarscore.bytes, 2, False)

    print(f'解析 code ={code} msg =  {analyze_bytes(msg, 10)}')


async def process_danmu(command, barrage_queue):
    message = WSPushMessage()
    steam = tarscore.TarsInputStream(command.vData)
    message.readFrom(steam)

    # print(f'process_danmu code = {message.iUri}')

    if message.iUri == 1400:
        await handle_message(message, barrage_queue)
    elif message.iUri == 6501:
        handle_gift(message)
    elif message.iUri == 1001 or message.iUri == 1002 or message.iUri == 1005:
        await handle_noble(message, barrage_queue)
    # elif message.iUri == 8006:
    #     handle_attendee_count(message)
    # else:
    #     handle_else(message)


async def handle_message(data, barrage_queue):
    # print(f'处理弹幕')

    stream = tarscore.TarsInputStream(data.sMsg)
    msg = MessageNotice()
    msg = msg.readFrom(stream)

    nick_name = msg.tUserInfo.sNickName
    content = msg.sContent
    print(f'弹幕 = name ={nick_name} content = {content}')

    if not is_login:
        return

    # 处理弹幕
    if not config.get('danmu_effective'):
        return

    global last_danmu
    last_danmu = get_last_danmu(nick_name, content)

    # 防钓鱼
    global last_send_s
    if time.time() - last_send_s < int(config.get('match_danmu_tick')):
        return
    last_send_s = time.time()

    if last_danmu:
        print(f'模拟发送弹幕 last_danmu = {last_danmu}')
        await barrage_queue.put(last_danmu)
        last_danmu = ''

    # for k, v in config.get('match_danmus').items():
    #     if k in content:
    #         await dmc.send_message(v)
    #         break


def get_last_danmu(nick_name, content):
    if is_source_danmu(nick_name):
        return
    if is_illegal_danmu(content):
        return

    return last_danmu if last_danmu else content[0:min(10, len(content))]


def is_source_danmu(nick_name):
    return nick_name in config.get('filter_sender')


def is_illegal_danmu(content):
    for illegal in config.get('illegal_danmu'):
        if illegal in content:
            return True
    return False


def handle_gift(data):
    # 处理礼物
    if not config.get('gift_effective'):
        return

    stream = tarscore.TarsInputStream(data.sMsg)
    gift = MessageGift()
    gift.readFrom(stream)

    print(f'礼物 = name ={gift.sSenderNick} content ={gift.sSendContent}')


async def handle_noble(data, barrage_queue):
    # 处理贵族消息
    if not config.get('noble_effective'):
        return

    stream = tarscore.TarsInputStream(data.sMsg)
    noble = NobleOpenNotice()
    noble.readFrom(stream)

    message = f'感谢{noble.tNobleInfo.sNickName}{"开通" if noble.tNobleInfo.iOpenFlag == 1 else "续费"}{noble.tNobleInfo.sName}'

    if noble.tNobleInfo.lRoomId == config.get('room_id'):
        print(f'贵族消息 = message ={message}')
        await barrage_queue.put(message)


def handle_attendee_count(data):
    print(f'出席人数通知')

    stream = tarscore.TarsInputStream(data.sMsg)
    notice = AttendeeCountNotice()
    notice.readFrom(stream)

    print(f'出席人数通知 = notice ={notice.iAttendeeCount} ')


def handle_else(data):
    print(f'处理未知消息')

    stream = tarscore.TarsInputStream(data.sMsg)
    unknow = MessageUnKnow()

    try:
        unknow.readFrom(stream)
        print(f'未知消息 = name ={unknow.tUserInfo.sNickName} content =')
    except:
        print(f'未知消息 解析失败 msg = {data.sMsg}')


async def block_when_room_open(room_id):
    while True:
        if is_room_open(room_id):
            return
        else:
            print('主播未上线')
            await asyncio.sleep(5 * 60)


async def stop_when_room_close(room_id, dmc: BarrageClient):
    while True:
        await asyncio.sleep(5 * 60)
        if not is_room_open(room_id):
            logger.info('退出')
            await dmc.stop()


def is_room_open(room_id):
    room_page = requests.get(f'https://m.huya.com/{room_id}', headers=config.get('headers')).text

    m = re.search(r"lYyid\":([0-9]+)", room_page, re.MULTILINE)
    ayyuid = m.group(1)
    m = re.search(r"lChannelId\":([0-9]+)", room_page, re.MULTILINE)
    tid = m.group(1)
    m = re.search(r"lSubChannelId\":([0-9]+)", room_page, re.MULTILINE)
    sid = m.group(1)

    return ayyuid is not None and tid is not None and sid is not None


def read_cookies():
    try:
        with open(config.get('cookie_path'), "rb") as cookiefile:
            cookies = pickle.load(cookiefile)
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookiestr = ';'.join(item for item in cookie)
            print(f'cookiestr={cookiestr}')

            for c in cookie:
                if 'yyuid' in c:
                    yyuid = c.split('=')[1]
                    config.set('yyuid', yyuid)
                    print(f'yyuid={yyuid}')
                if 'udb_n' in c:
                    udb_n = c.split('=')[1]
                    config.set('udb_n', udb_n)
                    print(f'udb_n = {udb_n}')
            config.set('cookie', cookiestr)
            return True
    except Exception as e:
        logger.info(f"read_cookies error = {repr(e)}")
        return False


async def main():
    room_id = config.get('room_id')
    await block_when_room_open(room_id)
    print("开播啦")

    if not config.get('cookie') or not config.get('yyuid'):
        if not os.path.exists(config.get('cookie_path')):
            logger.info("没有找到cookie_path")
            return
        if not read_cookies():
            print('读取cookie 失败')
            return

    q = asyncio.Queue()
    barrage_queue = asyncio.Queue()

    dmc = BarrageClient(f'https://www.huya.com/{room_id}', q)
    asyncio.create_task(receive_danmu(q, barrage_queue))
    asyncio.create_task(time_danmu(barrage_queue))
    asyncio.create_task(send_barrage(dmc, barrage_queue))
    asyncio.create_task(stop_when_room_close(room_id, dmc))

    await dmc.start()


def start():
    asyncio.run(main())
