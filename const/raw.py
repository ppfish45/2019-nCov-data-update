from const.paths import json_path

import os
import json

keyword_list = [
    "肺炎", "sari", "SARI", "Sari", "急寻", "寻找", "同行", "患者",
    "冠状", "同程", "同乘", "染病", "nCov", "NCOV", "ncov", "发烧", "发热",
    "紧急", "扩散", "病例", "确诊", "接触", "新型"
]

with open(os.path.join(json_path, "ua_list.json"), "r") as f:
    raw_ua_list = json.load(f)

with open(os.path.join(json_path, "flight_list.json"), "r") as f:
    raw_flight_code = json.load(f)

with open(os.path.join(json_path, "car_list.json"), "r") as f:
    raw_car_code = json.load(f)
