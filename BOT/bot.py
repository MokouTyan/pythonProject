from wechaty import Wechaty
import asyncio

class MyBot(Wechaty):
    async def on_message(self,msg):
        print('receive message event ...')
        print(msg)

async def main():
    bot = MyBot()
    await bot.start()

asyncio.run(main())