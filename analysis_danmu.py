from tars.models import *


def analysis():
    with open('danmu_data', 'rb') as f:
        data_eof = bytes(';;', encoding='utf-8')
        for data in f.read().split(data_eof):
            stream = tarscore.TarsInputStream(data)
            code = stream.read(tarscore.int64, 1, False)

            msg = stream.read(tarscore.bytes, 2, False)

            print(f'msg = {msg}')

            results = analyze_bytes(msg, 5)
            print(f'解析完成 results = {results}')


def analysis_hb():
    # data = b'\x00\x03\x1d\x00\x00\x69\x00\x00\x00\x69\x10\x03\x2c\x3c\x4c\x56\x08\x6f\x6e\x6c\x69\x6e\x65\x75\x69\x66\x0f\x4f\x6e\x55\x73\x65\x72\x48\x65\x61\x72\x74\x42\x65\x61\x74\x7d\x00\x00\x3c\x08\x00\x01\x06\x04\x74\x52\x65\x71\x1d\x00\x00\x2f\x0a\x0a\x0c\x16\x00\x26\x00\x36\x07\x61\x64\x72\x5f\x77\x61\x70\x46\x00\x0b\x12\x03\xae\xf0\x0f\x22\x03\xae\xf0\x0f\x3c\x42\x6d\x52\x02\x60\x5c\x60\x01\x7c\x82\x00\x0b\xb0\x1f\x9c\xac\x0b\x8c\x98\x0c\xa8\x0c'
    data = b'>\x00\x00\x00#\xba\x0b\x00\xc8\x00\x12\x00chat-10995317528250\x00\x02\x00\xf0\xaf\xfb$\x00\x00\x00\x00,\x95_d\x00\x00\x00\x00\x03\x08\x04\x005000B\x00\x00\x00'
    stream = tarscore.TarsInputStream(data)
    command = WebSocketCommand()
    command.readFrom(stream)

    print(command.__dict__)

    # steam = tarscore.TarsInputStream(data)
    # wup = Wup()
    # wup = wup.readFrom(steam)
    # print(f'wup = {wup.__dict__}')
    #
    # bs = tarscore.TarsInputStream(wup.sBuffer)
    # newdata = bs.read(tarscore.mapclass(tarscore.string, tarscore.bytes), 0, True)
    # print(newdata.get('tRsp'))


def analysis_message_req():
    data = b'\x00\x00\x00\xa6\x10\x03,1\x00\x80LV\x06liveuif\x0bsendMessage}\x00\x00\x0b\x08\x00\x01\x06\x00\x1d\x00\x00\x02\x00\xff\x81\x13\x88\x98\x0c\xa8\x00\x02\x06\x12STATUS_RESULT_DESC\x167require field not exist, tag: 0 headType: 1, headTag: 1\x06\x14STATUS_SETNAME_VALUE\x16\nhuya.sz.32'

    rsplist, unpacklen = Wup.unpackRspList(data)

    for wup in rsplist:
        print(wup.__dict__)
        bs = tarscore.TarsInputStream(wup.sBuffer)
        newdata = bs.read(tarscore.mapclass(tarscore.string, tarscore.bytes), 0, True)
        print(newdata)

        # rsps = tarscore.TarsInputStream(newdata.get('tRsp'))
        # # print(newdata.get('tRsp'))
        #
        # rsp = rsps.read(SendMessageRsp, 0, True)
        # print(f'SendMessageRsp UserInfo ={rsp.tNotice.tUserInfo.__dict__} Content = {rsp.tNotice.__dict__} ')
        # result = analyze_bytes(newdata.get('tRsp'), 3)

    # print(unpacklen)


def send_message():
    send_message = b'\x00\x03\x1d\x00\x01\x04M\x10\x03,<LV\x06liveuif\x0bsendMessage}\x00\x01\x04)\x08\x00\x01\x06\x04tReq\x1d\x00\x01\x04\x1b\n\n\x03\x00\x00\x00\x00\x92\x08i=\x16\x00&\x006\x1awebh5&2004231432&websocketG\x00\x00\x03\xb2h_unt=1610019142;udb_origin=0;udb_passport=qq_bmrrjkjqjdez;udb_uid=2450024765;udb_version=1.0;__yamid_new=C9345513E9100001974EE5D529571D52;_rep_cnt=2;username=qq_bmrrjkjqjdez;_yasids=__rootsid%3DC9345513EDB000013B3F1F1E10301587;udb_status=1;huya_flash_rep_cnt=8;web_qrlogin_confirm_id=424956c1-cf79-43c5-a250-b534c8775b3b;isInLiveRoom=true;__yamid_tt1=0.6880014554750828;huya_web_rep_cnt=16;yyuid=2450024765;udb_accdata=undefined;__yasmid=0.6880014554750828;udb_guiddata=17685ac46dc848848cbb2a8dee8da9cf;udb_passdata=3;guid=0a42cc4538f1f65fa386a583a68370cb;udb_biztoken=AQB1NIz82f9iDc9vk8FED3aPy8FUzsq9KUEjYWYUeppo9YHlfnL_OpW9901VutCJEAUZYqZEQH8mJ9DEf0qLlGiQfhd0o2EnJUsLo3671P8FJXDFg9IBMfoxumjIrxwLghKAaGru5OjogEBtAw7ggVzyn9AHiZxBH8KbHDbPlyrSxQCxbf8772PbJtg_nqDg-ujXCdKdAPPqDob8xukGCEyg7ECnqH15vjsbZ7XFqXXqpLoHSlXQfLXURhPzsUXG1f6NFCtgW2Hb-O6Z91OsJHUXQ5BoprZciO_6wbQQThN8NIwj9bgUqQcVApeN42bdKmCJGIN-ZOfRt_tldNuwZDh5;SoundValue=0.50;alphaValue=0.80\x0b\x12Z\xba\x17\xaf"Z\xba\x17\xaf6\x03666LZ\x00\xff\x10\x04,\x0bj\x00\xff\x10\x04,0\x01L\x0by\x00\x01\n\x0c\x16\x00\x0b\x82Z\xba\x17\xaf\x99\x00\x01\n\x00\x01\x16\x00\x0b\x0b\x8c\x98\x0c\xa8\x0c'
    stream = tarscore.TarsInputStream(send_message)
    command = WebSocketCommand()
    command.readFrom(stream)

    print(command.__dict__)

    steam = tarscore.TarsInputStream(command.vData)
    wup = Wup()
    wup = wup.readFrom(steam)
    print(f'wup = {wup.__dict__}')


def analyze_bytes(data, analysis):
    results = {}
    for i in range(analysis):
        results[i] = try_analyze_data(data, i)
    return results


if __name__ == '__main__':
    # analysis_hb()
    analysis_hb()
