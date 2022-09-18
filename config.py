__all__ = ["init", "set", "get"]
opts = {}


def init():
    global opts

    opts = {
        'room_id': '937129',
        'danmu_effective': False,
        'noble_effective': False,
        'gift_effective': False,
        'time_effective': False,
        # 'time_danmus': ['666666', '熊哥加油', '进来的兄弟帮熊哥点点订阅', '哈哈哈', '分享一下直播间', '冲冲冲', '熊哥不要怂，往前冲', '这操作行啊', '关注走一走，活到九十九',
        #                 '66666666', '礼物刷一刷，活到一百八', '漂亮', '哈哈哈哈', '狗熊，我永远支持你', '这个主播，爱了爱了', '6', '狗熊，我是你的颜粉',
        #                 '虎牙不倒，陪熊到老', '老色熊了', '66', '感谢大家的虎粮', '卡卡牌子不迷路', '感谢大哥的礼物', '免费虎粮送一送，升升牌子'],
        'time_danmus': ['卡牌子进群联系我哈', '动动你的小手点个订阅，省的下次回来会迷路'],
        'match_danmus': {
            '铭文': '点完订阅右下角一直右滑可以查看',
            '下分': '下分快联系我啊～',
            '粉丝群': '9，11，13级牌子联系贵宾榜小芒果',
        },
        'match_danmu_tick': 10,
        'time_danmu_tick': 60,
        'cookie_path': './cookie/cookies.pkl',
        'cookie': '',
        'yyuid': 0,
        'udb_n': '',
        'illegal_danmu': ['王者', '.com', '.cn', '奶', '爱', '房管'],
        'filter_sender': ['黑白小调', '晴宝【浣熊下分私】', '小芒果【进浣熊群】'],
        'headers': {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'}
    }


def get(key):
    return opts.get(key)


def set(key, value):
    opts[key] = value


init()
