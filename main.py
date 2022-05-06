import telegram
import requests
import time
import logging
import logging.handlers

logging.basicConfig(
    level=logging.INFO,
    filename='price.log',
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
)

logger = logging.getLogger('priceLogger')
timehandler = logging.handlers.TimedRotatingFileHandler(
    'price.log',
    when='D',
    interval=1,
    backupCount=10
)
logger.addHandler(timehandler)

priceChannel = "-1001772797262"
groupIds = ["-1001501807639", "-1001228775770"]  # dpal wallet group id
priceUrl = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT"  # "https://chain.so/api/v2/get_price/DOGE/USD"
timeout = 60
bot = telegram.Bot(token=botToken)

msgTokens = {}
try:
    while True:
        try:
            rs = dict(requests.get(priceUrl).json())
            price = float(rs.get("price", 0))
            logger.info(f">>>>>>>>>>>>>>>>>> current price:{price}")

            if price > 0:
                bot.send_message(chat_id=priceChannel, text=f"当前价格: {price}")

                for gId in groupIds:
                    newMsgObj = bot.send_message(chat_id=gId, text=f"当前价格: {price}")

                    oldMsg = dict(msgTokens).get(gId, None)
                    if oldMsg is not None:
                        oldMsg.delete()
                    msgTokens[gId] = newMsgObj

        except BaseException as e:
            logger.error(">>>>>>>>>>>>>>>>>> error:")
            logger.error(e)
        time.sleep(timeout)
except SystemExit as f:
    for cmsg in msgTokens.values():
        if cmsg is not None:
            cmsg.delete()
