import asyncio

import aiohttp

from huya import Huya


class BarrageClient:
    def __init__(self, url: str, q, **kwargs):
        self.__hs = None
        self.__ws = None
        self.__stop = False
        self.__dm_queue = q
        self.__link_status = True
        self.__extra_data = kwargs
        self.__url = url if url.startswith('http') else 'http://' + url
        self.__huya = Huya()
        self.__hs = aiohttp.ClientSession()

    async def init_ws(self):
        ws_url, reg_datas = await self.__huya.shake_hands(self.__url)
        self.__ws = await self.__hs.ws_connect(ws_url)
        for reg_data in reg_datas:
            await self.send_barrage(reg_data)

    async def heartbeats(self):
        while not self.__stop:
            # print('heartbeat')
            await asyncio.sleep(20)
            await self.send_barrage(Huya.heartbeat)

    async def fetch_barrage(self):
        while not self.__stop:
            async for msg in self.__ws:
                command = Huya.decode(msg.data)
                await self.__dm_queue.put(command)
            if not self.__stop:
                await asyncio.sleep(1)
                await self.init_ws()
                await asyncio.sleep(1)

    async def start(self):
        await self.init_ws()
        await self.login()
        await asyncio.gather(self.heartbeats(), self.fetch_barrage())

    async def stop(self):
        self.__stop = True
        await self.__hs.close()

    async def send_barrage(self, message):
        data = Huya.encode(message) if type(message) is str else message
        # print(f"send_barrage = {data}")
        await self.__ws.send_bytes(data)

    async def login(self):
        data = Huya.login()
        print(f'login = {data}')
        await self.send_barrage(data)
