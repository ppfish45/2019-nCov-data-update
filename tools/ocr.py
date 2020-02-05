from urllib.parse import urlencode
from tools.common import highlight

import time
import base64
import random
import string
import hashlib
import requests

app_id = 2127865759
app_key = "A3BAiScFjpIW4bDf"

def get_sign_str(form_data):

    dic = sorted(form_data.items(), key=lambda d: d[0])
    sign = urlencode(dic) + '&app_key=' + app_key
    m = hashlib.md5()
    m.update(sign.encode('utf8'))
    return m.hexdigest().upper()

def ocr_text(image_path):

    with open(image_path, "rb") as image_file:
        enc = base64.b64encode(image_file.read())

    data = {
        "app_id" : app_id,
        "image" : enc,
        "nonce_str" : ''.join(random.sample(string.digits + string.ascii_letters, 32)),
        "time_stamp" : int(time.time()),
    }

    sign = get_sign_str(data)

    data["sign"] = sign

    ret_str = ""

    for i in range(5):

        url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr"
        r = requests.post(url, data=data)

        if r.json()["ret"] == 0:
            print(highlight("识别图片成功。"))
            result = r.json()["data"]["item_list"]
            last = result[0]["itemcoord"][0]["y"]
            for item in result:
                if item["itemcoord"][0]["y"] - last > 9:
                    last = item["itemcoord"][0]["y"]
                    ret_str += "\n"
                ret_str += item["itemstring"] + " "
            break
        else:
            print(highlight(f"识别图片失败，原因：{r.json()['msg']}"))

        time.sleep(1)

    return ret_str

def main():
    ocr_text("test.png")

if __name__ == "__main__":
    main()