from mirai import Mirai, WebSocketAdapter, FriendMessage

if __name__ == '__main__':
    bot = Mirai(
        qq=2270263801, # 改成你的机器人的 QQ 号
        adapter=WebSocketAdapter(
            verify_key='1234567890', host='localhost', port=6700
        )
    )

    @bot.on(FriendMessage)
    def on_friend_message(event: FriendMessage):
        if str(event.message_chain) == '你好':
            return bot.send(event, 'Hello, World!')

    bot.run()