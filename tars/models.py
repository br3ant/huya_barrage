import struct
import time

import config
from .core import tarscore


class base_struct(tarscore.struct):
    __tars_class__ = 'base_struct'

    def __init__(self):
        self.var0 = None
        self.var1 = None
        self.var2 = None
        self.var3 = None
        self.var4 = None
        self.var5 = None
        self.var6 = None
        self.var7 = None
        self.var8 = None
        self.var9 = None
        self.var10 = None

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        var = base_struct()
        var.var0 = try_analyze_base(t, 0)
        var.var1 = try_analyze_base(t, 1)
        var.var2 = try_analyze_base(t, 2)
        var.var3 = try_analyze_base(t, 3)
        var.var4 = try_analyze_base(t, 4)
        var.var5 = try_analyze_base(t, 5)
        var.var6 = try_analyze_base(t, 6)
        var.var7 = try_analyze_base(t, 7)
        var.var8 = try_analyze_base(t, 8)
        var.var9 = try_analyze_base(t, 9)
        var.var10 = try_analyze_base(t, 10)
        # var.var0 = t.read(tarscore.int64, 0, False)
        # var.var1 = t.read(tarscore.int64, 1, False)
        # var.var2 = t.read(tarscore.string, 2, False,)
        # var.var3 = t.read(tarscore.int32, 3, False)
        return var


class WebSocketCommand:
    def __init__(self):
        self.iCmdType = 0
        self.vData = b''

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int32, 0, self.iCmdType)
        t.write(tarscore.bytes, 1, self.vData)

    def readFrom(self, t: tarscore.TarsInputStream):
        self.iCmdType = t.read(tarscore.int32, 0, False, self.iCmdType)
        self.vData = t.read(tarscore.bytes, 1, False, self.vData)

    def bin_buffer(self):
        cos = tarscore.TarsOutputStream()
        self.writeTo(cos)
        return cos.getBuffer()


class WSPushMessage:
    def __init__(self):
        self.ePushType = 0
        self.iUri = 0
        self.sMsg = b''
        self.iProtocolType = 0

    def readFrom(self, t: tarscore.TarsInputStream):
        self.ePushType = t.read(tarscore.int32, 0, False, self.ePushType)
        self.iUri = t.read(tarscore.int64, 1, False, self.iUri)
        self.sMsg = t.read(tarscore.bytes, 2, False, self.sMsg)
        self.iProtocolType = t.read(tarscore.int32, 3, False, self.iProtocolType)


class MessageNotice(tarscore.struct):
    def __init__(self):
        self.tUserInfo = None
        self.lTid = 0
        self.lSid = 0
        self.sContent = ""
        self.iShowMode = 0
        self.tFormat = None
        self.tBulletFormat = None
        self.iTermType = 0
        self.vDecorationPrefix = None
        self.vDecorationSuffix = None
        self.vAtSomeone = None
        self.lPid = 0

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        notice = MessageNotice()
        notice.tUserInfo = t.read(SenderInfo, 0, False, notice.tUserInfo)
        notice.lTid = t.read(tarscore.int64, 1, False, notice.lTid)
        notice.lSid = t.read(tarscore.int64, 2, False, notice.lSid)
        notice.sContent = t.read(tarscore.string, 3, False, notice.sContent)
        notice.iShowMode = t.read(tarscore.int32, 4, False, notice.iShowMode)
        # notice.tFormat = t.read(tarscore.struct, 5, False, notice.tFormat)
        # notice.tBulletFormat = t.read(tarscore.struct, 6, False, notice.tBulletFormat)
        notice.iTermType = t.read(tarscore.int32, 7, False, notice.iTermType)
        # notice.vDecorationPrefix = t.read(tarscore.vctclass, 8, False, notice.vDecorationPrefix)
        # notice.vDecorationSuffix = t.read(tarscore.vctclass, 9, False, notice.vDecorationSuffix)
        # notice.vAtSomeone = t.read(tarscore.vctclass, 10, False, notice.vAtSomeone)
        notice.lPid = t.read(tarscore.int64, 11, False, notice.lPid)
        return notice


class SenderInfo(tarscore.struct):
    def __init__(self):
        self.lUid = 0
        self.lImid = 0
        self.sNickName = ""
        self.iGender = 0

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        var = SenderInfo()
        var.lUid = t.read(tarscore.int64, 0, False, var.lUid)
        var.lImid = t.read(tarscore.int64, 1, False, var.lImid)
        var.sNickName = t.read(tarscore.string, 2, False, var.sNickName)
        var.iGender = t.read(tarscore.int32, 3, False, var.iGender)
        return var


class MessageGift:
    def __init__(self):
        self.iItemType = 0
        self.strPayId = ""
        self.iItemCount = 0
        self.lPresenterUid = 0
        self.lSenderUid = 0
        self.sPresenterNick = ""
        self.sSenderNick = ""
        self.sSendContent = ""
        self.iItemCountByGroup = 0
        self.iItemGroup = 0
        self.iSuperPupleLevel = 0
        self.iComboScore = 0
        self.iDisplayInfo = 0
        self.iEffectType = 0
        self.iSenderIcon = ""
        self.iPresenterIcon = ""
        self.iTemplateType = 0
        self.sExpand = ""
        self.bBusi = False
        self.iColorEffectType = 0
        self.sPropsName = ""
        self.iAccpet = 0
        self.iEventType = 0
        self.userInfo = None
        self.lRoomId = 0
        self.lHomeOwnerUid = 0
        self.streamerInfo = None
        self.iPayType = -1,
        self.iNobleLevel = 0
        self.tNobleLevel = None
        self.tEffectInfo = None
        self.vExUid = None
        self.iComboStatus = 0
        self.iPidColorType = 0

    def readFrom(self, t: tarscore.TarsInputStream):
        self.sSenderNick = t.read(tarscore.string, 6, False, self.sSenderNick)
        self.sSendContent = t.read(tarscore.string, 7, False, self.sSendContent)


class NobleOpenNotice:
    def __init__(self):
        self.tNobleInfo = None

    def readFrom(self, t: tarscore.TarsInputStream):
        self.tNobleInfo = t.read(NobleBase, 0, False, self.tNobleInfo)


class AttendeeCountNotice:
    def __init__(self):
        self.iAttendeeCount = 0

    def readFrom(self, t: tarscore.TarsInputStream):
        self.iAttendeeCount = t.read(tarscore.int32, 0, False, self.iAttendeeCount)


class NobleBase(tarscore.struct):
    def __init__(self):
        self.lUid = 0
        self.sNickName = ""
        self.iLevel = 0
        self.sName = ""
        self.iPet = 0
        self.lPid = 0
        self.lTid = 0
        self.lSid = 0
        self.lStartTime = 0
        self.lEndTime = 0
        self.iLeftDay = 0
        self.iStatus = 0
        self.iOpenFlag = 0
        self.iMonths = 0
        self.sPNickName = ""
        self.lShortSid = 0
        self.iSourceType = 0
        self.iPayType = 0
        self.sLogoUrl = ""
        self.vDecorationPrefix = None
        self.vDecorationSuffix = None
        self.iScreenType = 0
        self.tLevel = None
        self.lRoomId = 0

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        noble = NobleBase()
        noble.sNickName = t.read(tarscore.string, 1, False, noble.sNickName)
        noble.iLevel = t.read(tarscore.int32, 2, False, noble.iLevel)
        noble.sName = t.read(tarscore.string, 3, False, noble.sName)
        noble.iMonths = t.read(tarscore.int32, 13, False, noble.iMonths)
        noble.sPNickName = t.read(tarscore.string, 14, False, noble.sPNickName)
        noble.iSourceType = t.read(tarscore.int32, 16, False, noble.iSourceType)
        noble.iPayType = t.read(tarscore.int64, 17, False, noble.iPayType)
        noble.sLogoUrl = t.read(tarscore.string, 18, False, noble.sLogoUrl)
        # self.tLevel = t.readStruct(22, False, self.tLevel)
        noble.lRoomId = t.read(tarscore.int32, 23, False, noble.lRoomId)
        return noble


class MessageUnKnow:
    def __init__(self):
        self.tUserInfo = None

    def readFrom(self, t: tarscore.TarsInputStream):
        self.tUserInfo = t.read(SenderInfo, 0, False, self.tUserInfo)


class WSVerifyCookieReq:
    def __init__(self):
        self.lUid = int(config.get('yyuid'))
        self.sUA = "webh5&2004231432&websocket"
        self.sCookie = config.get('cookie')

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int64, 0, self.lUid)
        t.write(tarscore.string, 1, self.sUA)
        t.write(tarscore.string, 2, self.sCookie)

    def bin_buffer(self):
        os = tarscore.TarsOutputStream()
        self.writeTo(os)
        return os.getBuffer()


class WSVerifyCookieRsp:
    def __init__(self):
        self.iValidate = 0

    def readFrom(self, t: tarscore.TarsInputStream):
        self.iValidate = t.read(tarscore.int32, 0, False, self.iValidate)


class Wup(tarscore.struct):

    def __init__(self):
        self.iVersion = 3
        self.cPacketType = 0
        self.iMessageType = 0
        self.iRequestId = int(time.time())
        self.sServantName = "liveui"
        self.sFuncName = "sendMessage"
        self.sBuffer = b''
        self.iTimeout = 0
        self.context = {}
        self.status = {}
        self.newdata = None

    def writeTo(self, t: tarscore.TarsOutputStream):
        # t.write(tarscore.mapclass(tarscore.string, tarscore.bytes), 0, self.newdata)
        # t.write(tarscore.int32, 0, len(self.sBuffer) + 4)
        t.write(tarscore.int16, 1, self.iVersion)
        t.write(tarscore.int8, 2, self.cPacketType)
        t.write(tarscore.int32, 3, self.iMessageType)
        t.write(tarscore.int32, 4, self.iRequestId)
        t.write(tarscore.string, 5, self.sServantName)
        t.write(tarscore.string, 6, self.sFuncName)
        t.write(tarscore.bytes, 7, self.sBuffer)
        t.write(tarscore.int32, 8, self.iTimeout)
        t.write(tarscore.mapclass(tarscore.string, tarscore.string), 9, self.context)
        t.write(tarscore.mapclass(tarscore.string, tarscore.string), 10, self.status)

    def set_Req(self, req):
        os = tarscore.TarsOutputStream()
        os.write(SendMessageReq, 0, req)
        self.newdata = {'tReq': os.getBuffer()}

        obs = tarscore.TarsOutputStream()
        obs.write(tarscore.mapclass(tarscore.string, tarscore.bytes), 0, self.newdata)
        self.sBuffer = obs.getBuffer()

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        var = Wup()
        var.iRequestId = t.read(tarscore.int32, 4, False)
        var.sServantName = t.read(tarscore.string, 5, False)
        var.sFuncName = t.read(tarscore.string, 6, False)
        var.sBuffer = t.read(tarscore.bytes, 7, False)
        var.context = t.read(tarscore.mapclass(tarscore.string, tarscore.string), 9, False)
        var.status = t.read(tarscore.mapclass(tarscore.string, tarscore.string), 10, False)
        return var

    def bin_buffer(self):
        wos = tarscore.TarsOutputStream()
        self.writeTo(wos)

        reqpkt = wos.getBuffer()
        plen = len(reqpkt) + 4
        reqpkt = struct.pack('!i', plen) + reqpkt
        return reqpkt

    @staticmethod
    def unpackRspList(buf):
        '''
        @brief: 解码响应报文
        @param buf: 多个序列化后的响应报文数据
        @type buf: str
        @return: 解码出来的响应报文和解码的buffer长度
        @rtype: rsplist: 装有ResponsePacket的list
                unpacklen: int
        '''
        rsplist = []
        if not buf:
            return rsplist

        unpacklen = 0

        while True:
            if len(buf) - unpacklen < 4:
                break
            packsize = buf[unpacklen: unpacklen + 4]
            packsize, = struct.unpack_from('!i', packsize)
            if len(buf) < unpacklen + packsize:
                break

            ios = tarscore.TarsInputStream(buf[unpacklen + 4: unpacklen + packsize])
            rsp = Wup.readFrom(ios)
            rsplist.append(rsp)
            unpacklen += packsize

        return rsplist, unpacklen


class SendMessageReq(tarscore.struct):
    def __init__(self, message, ayyuid):
        self.tUserId = UserId()
        self.lTid = ayyuid
        self.lSid = ayyuid
        self.sContent = message
        self.iShowMode = 0
        self.tFormat = ContentFormat()
        self.tBulletFormat = BulletFormat()
        self.vAtSomeone = [UidNickName()]
        self.lPid = ayyuid
        self.vTagInfo = [MessageTagInfo()]

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.struct, 0, self.tUserId)
        t.write(tarscore.int64, 1, self.lTid)
        t.write(tarscore.int64, 2, self.lSid)
        t.write(tarscore.string, 3, self.sContent)
        t.write(tarscore.int32, 4, self.iShowMode)
        t.write(tarscore.struct, 5, self.tFormat)
        t.write(tarscore.struct, 6, self.tBulletFormat)
        t.write(tarscore.vctclass(UidNickName), 7, self.vAtSomeone)
        t.write(tarscore.int64, 8, self.lPid)
        t.write(tarscore.vctclass(MessageTagInfo), 9, self.vTagInfo)

    def bin_buffer(self):
        sos = tarscore.TarsOutputStream()
        self.writeTo(sos)
        return sos.getBuffer()


class SendMessageRsp(tarscore.struct):

    def __init__(self):
        self.iStatus = 0
        self.tNotice = None
        self.sToast = ""

    @staticmethod
    def readFrom(t: tarscore.TarsInputStream):
        rsp = SendMessageRsp()
        rsp.iStatus = t.read(tarscore.int32, 0, False)
        rsp.tNotice = t.read(MessageNotice, 1, False)
        rsp.sToast = t.read(tarscore.string, 2, False)
        return rsp


class ContentFormat(tarscore.struct):
    def __init__(self):
        self.iFontColor = -1
        self.iFontSize = 4
        self.iPopupStyle = 0

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int32, 0, self.iFontColor)
        t.write(tarscore.int32, 1, self.iFontSize)
        t.write(tarscore.int32, 2, self.iPopupStyle)


class BulletFormat(tarscore.struct):
    def __init__(self):
        self.iFontColor = -1
        self.iFontSize = 4
        self.iTextSpeed = 0
        self.iTransitionType = 1
        self.iPopupStyle = 0

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int32, 0, self.iFontColor)
        t.write(tarscore.int32, 1, self.iFontSize)
        t.write(tarscore.int32, 2, self.iTextSpeed)
        t.write(tarscore.int32, 3, self.iTransitionType)
        t.write(tarscore.int32, 4, self.iPopupStyle)


class UidNickName(tarscore.struct):
    def __init__(self):
        self.lUid = 0
        self.sNickName = ""

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int64, 0, self.lUid)
        t.write(tarscore.string, 1, self.sNickName)


class MessageTagInfo(tarscore.struct):
    def __init__(self):
        self.iAppId = 1
        self.sTag = ""

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int32, 0, self.iAppId)
        t.write(tarscore.string, 1, self.sTag)


class UserId(tarscore.struct):
    def __init__(self):
        self.lUid = int(config.get('yyuid'))
        self.sGuid = ""
        self.sToken = ''
        self.sHuYaUA = "webh5&2004231432&websocket"
        self.sCookie = config.get('cookie')
        self.iTokenType = 0
        self.sDeviceInfo = "Chrome"

    def writeTo(self, t: tarscore.TarsOutputStream):
        t.write(tarscore.int64, 0, self.lUid)
        t.write(tarscore.string, 1, self.sGuid)
        t.write(tarscore.string, 2, self.sToken)
        t.write(tarscore.string, 3, self.sHuYaUA)
        t.write(tarscore.string, 4, self.sCookie)


types = [tarscore.int64, tarscore.double,
         tarscore.string, tarscore.bytes,
         tarscore.mapclass(tarscore.string, tarscore.string),
         tarscore.mapclass(tarscore.string, tarscore.bytes), base_struct]

base_types = [tarscore.int64, tarscore.double,
              tarscore.string, tarscore.bytes,
              tarscore.mapclass(tarscore.string, tarscore.string),
              tarscore.mapclass(tarscore.string, tarscore.bytes)]


def try_analyze_data(data, tag):
    input_is = tarscore.TarsInputStream(data)
    for coder in types:
        try:
            position = input_is.get_position()
            result = input_is.read(coder, tag, True)
            if result:
                if coder.__tars_class__ == 'string':
                    return result
                elif coder.__tars_class__ == 'base_struct':
                    return result.__dict__
                else:
                    return result
        except:
            input_is.set_position(position)
            pass
    return None


def try_analyze_base(input_is, tag):
    for coder in base_types:
        try:
            position = input_is.get_position()
            result = input_is.read(coder, tag, True)
            if result:
                if coder.__tars_class__ == 'string':
                    return result
                else:
                    return result
        except:
            input_is.set_position(position)
    return None
