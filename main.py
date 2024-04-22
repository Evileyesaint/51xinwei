from pycqBot import cqHttpApi, cqLog
from pycqBot.data import Message
import requests

cqLog()

cqapi = cqHttpApi()
bot = cqapi.create_bot()

def openlight(commandData, message: Message):
    message.reply("灯光已经开启")
    try:
        requests.get('http://192.168.137.189/pin?light=on')
    except:
        pass

def closelight(commandData, message: Message):
    message.reply("灯光已经关闭")
    try:
        requests.get('http://192.168.137.189/pin?light=off')
    except:
        pass

bot.command(openlight, "开灯", {"type": "all"})
bot.command(closelight, "关灯", {"type": "all"})

bot.start()