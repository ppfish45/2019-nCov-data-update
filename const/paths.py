import os
import json

root_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + ".."
json_path = os.path.join(root_path, "json")
record_path = os.path.join(root_path, "record")

def validate_json(filepath, map=False):
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            if map:
                json.dump({}, f)
            else:
                json.dump([], f)

    try:
        with open(filepath, "r") as f:
            json.load(f)
    except:
        with open(filepath, "w") as f:
            if map:
                json.dump({}, f)
            else:
                json.dump([], f)

def update_path(idx):

    global unread_post_filepath, read_post_filepath, star_post_filepath
    global mark_filepath, star_filepath, account_filepath
    global baidu_path, weibo_path

    weibo_path = os.path.join(record_path, "downloaded_weibo", idx)
    baidu_path = os.path.join(record_path, "downloaded_baidu", idx)

    unread_post_filepath = os.path.join(record_path, idx, "unread_post.json")
    read_post_filepath = os.path.join(record_path, idx, "read_post.json")
    star_post_filepath = os.path.join(record_path, idx, "star_post.json")

    mark_filepath = os.path.join(record_path, idx, "post_list.json")
    star_filepath = os.path.join(record_path, idx, "star_list.json")
    account_filepath = os.path.join(record_path, idx, "account_list.json")

    os.makedirs(weibo_path, exist_ok=True)
    os.makedirs(baidu_path, exist_ok=True)

    os.makedirs(os.path.join(record_path, idx), exist_ok=True)

    validate_json(unread_post_filepath)
    validate_json(read_post_filepath)
    validate_json(star_post_filepath)

    validate_json(account_filepath)
    validate_json(star_filepath)
    validate_json(mark_filepath)

def clear(idx):

    os.remove(unread_post_filepath)
    os.remove(read_post_filepath)
    os.remove(star_post_filepath)
    os.remove(mark_filepath)
    os.remove(star_filepath)

    update_path(idx)

'''
weibo_path = os.path.join(record_path, "downloaded_weibo")

unread_post_filepath = os.path.join(record_path, "unread_post.json")
read_post_filepath = os.path.join(record_path, "read_post.json")
star_post_filepath = os.path.join(record_path, "star_post.json")

mark_filepath = os.path.join(record_path, "post_list.json")
star_filepath = os.path.join(record_path, "star_list.json")
account_filepath = os.path.join(record_path, "account_list.json")

os.makedirs(weibo_path, exist_ok=True)

validate_json(unread_post_filepath)
validate_json(read_post_filepath)
validate_json(star_post_filepath)

validate_json(account_filepath)
validate_json(star_filepath)
validate_json(mark_filepath)
'''