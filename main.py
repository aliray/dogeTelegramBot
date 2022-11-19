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

groupIds = ["-1001501807639", "-1001228775770"]  # dpal wallet group id
priceUrl = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT"  # "https://chain.so/api/v2/get_price/DOGE/USD"
botToken = ""
timeout = 60
bot = telegram.Bot(token=botToken)


def deleteMsg(_msg):
    try:
        if _msg is not None:
            _msg.delete()
    except BaseException as e:
        logger.error(">>>>>>>>>>>>>>>>>> msg delete error", e)
        logger.error(e)


msgTokens = {}
try:
    while True:
        try:
            rs = dict(requests.get(priceUrl).json())
            price = float(rs.get("price", 0))
            logger.info(f">>>>>>>>>>>>>>>>>> current price:{price}")

            if price > 0:
                for gId in groupIds:
                    newMsgObj = bot.send_message(chat_id=gId, text=f"当前价格: {price}")
                    oldMsg = dict(msgTokens).get(gId, None)
                    deleteMsg(oldMsg)
                    msgTokens[gId] = newMsgObj

        except BaseException as e:
            logger.error(">>>>>>>>>>>>>>>>>> error:")
            logger.error(e)
        time.sleep(timeout)
except SystemExit as f:
    for cmsg in msgTokens.values():
        if cmsg is not None:
            deleteMsg(cmsg)
