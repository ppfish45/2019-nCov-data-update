import json
import os

root_dir = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + ".."

with open(os.path.join(root_dir, "crawler", "weibo_config.json"), "r") as f:
    data = json.load(f)
    weibo_list = data["user_id_list"]

wechat_list = [

]