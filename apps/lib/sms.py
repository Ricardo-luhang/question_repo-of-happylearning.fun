import urllib.request
import urllib
import json
import logging

logger = logging.getLogger('sms')


def send_sms(mobile, captcha):
    flag = True
    # 这个是短信API地址
    url = 'https://open.ucpaas.com/ol/sms/sendsms'

    # 准备一下头,声明body的格式
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    # 还有我们准备用Post传的值，这里值用字典的形式
    values = {
        "sid": "88a2d067248f084b98c4594f0c696e9d",
        "token": "e41bedc41e6cdb83e19e199ca4ca038d",
        "appid": "afa273bf826f4edb9eca7ebd43045c29",
        "templateid": "354098",
        "param": str(captcha),
        "mobile": mobile,
    }

    try:
        # 将字典格式化成bytes格式
        data = json.dumps(values).encode('utf-8')
        logger.info(f"即将发送短信: {data}")
        # 创建一个request,放入我们的地址、数据、头
        request = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        code = json.loads(html)["code"]
        if code == "000000":
            logger.info(f"短信发送成功：{html}")
            flag = True
        else:
            logger.info(f"短信发送失败：{html}")
            flag = False
    except Exception as ex:
        logger.info(f"出错了,错误原因：{ex}")
        flag = False
    return flag


if __name__ == "__main__":
    send_sms('15811564298', '1234')
