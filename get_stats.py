import os
from pprint import pprint

from tqdm import tqdm
from pixivpy3 import *
from typing import *
import time
import csv
from datetime import datetime, timezone
from pxdata.utils import *
from pxdata.class_illust import *
from collections import defaultdict
import statistics as st
import argparse


# 如果存在自定义设置, 导入
try:
    from privates.my_users import *
except ImportError:
    print('')


def get_recover_token_usr(user: str = "yada"):
    """实际获取token:
    https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde
    """
    if user.lower() == "yada":
        with open("privates/recover_token_yada.txt") as fd:
            line = fd.readline()
            return line
    elif user.lower() == "ada":
        with open("privates/recover_token_ada.txt") as fd:
            line = fd.readline()
            return line


def get_recover_token():
    """实际获取token:
    https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde
    """
    with open("privates/token.txt") as fd:
        line = fd.readline()
        return line


def get_user_illusts(api: AppPixivAPI, user: int) -> List[Dict]:
    """返回pixiv id=<user>的所有illust json
    """
    all_illusts = []

    json_result = api.user_illusts(user)
    all_illusts += json_result['illusts']

    pbar = tqdm(desc="collecting info for user %s: " % user)
    while json_result["next_url"]:
        time.sleep(0.3)
        next_qs = api.parse_qs(json_result.next_url)
        json_result = api.user_illusts(**next_qs)
        all_illusts += json_result['illusts']
        pbar.update(30)

    return all_illusts


def get_summary_nums(data_list: List[float] | List[int]) -> Tuple:
    """返回tuple格式的mean, med和var
    """
    return st.mean(data_list), st.median(data_list), st.variance(data_list), max(data_list), min(data_list)

def get_summary_str(data_list: List[float] | List[int]) -> str:
    """返回tuple格式的mean, med和var
    """
    nums = get_summary_nums(data_list)

    d = defaultdict(lambda: "...")
    d.update({
        "mean": "%.3f"%nums[0],
        "med": "%.3f"%nums[1],
        "var": "%.3f" % nums[2],
        "max": "%.3f" % nums[3],
        "min": "%.3f" % nums[4],
    })
    return "mean:{mean}  med:{med}  var:{var}  max:{max}  min:{min}".format_map(d)

def get_user_summary(illust_class_list: List[Illust], user, username):
    """返回有效信息
    :param illust_class_list:
    """
    illust_count = len(illust_class_list)
    views_list = [i.total_view for i in illust_class_list]
    bookmarks_list = [i.total_bookmarks for i in illust_class_list]

    pages_list = [i.page_count for i in illust_class_list]
    view_per_hour_list = [float(i.view_per_hour) for i in illust_class_list]
    bm_per_hour_list = [float(i.bm_per_hour) for i in illust_class_list]

    book_view_rate_list = [float(i.book_view_rate) for i in illust_class_list]
    pid_list = [i.id for i in illust_class_list]

    s0 = get_summary_str(book_view_rate_list)

    max_view = max(views_list)
    max_bookmark = max(bookmarks_list)


    d = defaultdict(lambda: "...")
    d.update({"foo": "name"})


    d1 = defaultdict(lambda: "...")
    d1.update(
        {"user": user, "username":username, "ctime":datetime.now().ctime(),
         "i_count":illust_count, "v_count":sum(views_list), "b_count": sum(bookmarks_list), "n_count":sum(pages_list),

         "avg_r": "%.3f"%(sum(views_list)/illust_count), "avg_b": "%.3f"%(sum(bookmarks_list)/illust_count),
         "avg_b/r": "%.3f"%(sum(bookmarks_list)/sum(views_list)),
         "avg_n_count": "%.3f"%(sum(pages_list)/illust_count),

         "top_r":max_view, "top_r_pid": pid_list[views_list.index(max_view)],
         "top_b":max_bookmark, "top_b_pid":pid_list[bookmarks_list.index(max_bookmark)]}
    )

    s1 = "用户: [{user}] {username}  |  {ctime}\n" \
         "\n" \
         "投稿数:{i_count}  总阅读:{v_count}  总收藏:{b_count}  总图片数:{n_count}\n" \
         " 平均阅读:{avg_r}\n" \
         " 平均收藏:{avg_b}\n" \
         " 平均收藏/阅读:{avg_b/r}\n" \
         " 平均图片数:{avg_n_count}\n" \
         "最高阅读:{top_r}  pid={top_r_pid}\n" \
         "最高收藏:{top_b}  pid={top_b_pid}\n".format_map(d1)

    # mean, median, standard deviation
    s3 = "每投稿收藏/阅读比  "+ get_summary_str(book_view_rate_list) + \
         "\n 阅读量/h (每投稿) " + get_summary_str(view_per_hour_list) +\
         "\n 收藏数/h (每投稿) " + get_summary_str(bm_per_hour_list) +\
         "\n 阅读量   (每投稿) " + get_summary_str(views_list) + \
         "\n 收藏数   (每投稿) " + get_summary_str(bookmarks_list)

    summary = (s1 + "\n" + s3 + "\n")
    return summary


def get_data(illust_list: List, user: int, username: str, save_data:bool=True):
    """
    输入pixivpy3得到的illust_list, 导出数据到private目录下的csv和txt文件
    :param illust_list: 获取到的illusts
    :param save_data: 是否保存到文件
    :return: csv文件
    """
    # Get the current datetime with the timezone set to the past_date timezone

    curr_time_str = get_time_string()
    current_date = datetime.now(timezone.utc)
    illust_class_list = [Illust(i, current_date) for i in illust_list]
    file_prefix = username  # "name"

    csv_filename = file_prefix + "_" + curr_time_str + '.csv'
    txt_filename = file_prefix + "_" + curr_time_str + '.txt'

    out_dir = "privates/csv"
    mkdir_if_not_exist(out_dir)
    out_path = os.path.join(out_dir, csv_filename)

    summary = get_user_summary(illust_class_list, user, username)

    if save_data:
        write_data(illust_class_list, out_dir, out_path, summary, txt_filename)
        print("%d post data exported" % len(illust_list))

    print(summary)


def write_data(illust_class_list, out_dir, out_path, summary, txt_filename):
    """
    导出数据到文件
    """
    with open(os.path.join(out_dir, txt_filename), 'w', newline='', encoding='utf-8-sig') as f:
        f.write(summary)
    with open(out_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['create_date', 'id', 'title', 'views', 'bookmarks', 'width', 'height',
                         'bookmark/h', 'view/h', 'book_view_rate', 'view_book_rate', 'comments',
                         'pages'])

        for i in illust_class_list:
            # EXCEL生成URL列: =HYPERLINK("http://www.pixiv.net/artworks/"&B2)
            writer.writerow(
                [i.create_date, i.id, i.title, i.total_view, i.total_bookmarks, i.width, i.height,
                 i.bm_per_hour, i.view_per_hour, i.book_view_rate, i.view_book_rate, i.total_comments,
                 i.page_count])


def do_stats(user: int, token=None, save_data=True):
    """
    工厂模式; 用user string对应实际方案
    :param user: pixiv user id
    :param token: pixiv refresh token
    """
    api = AppPixivAPI()
    if token:
        api.auth(refresh_token=token)
    else:
        api.auth(refresh_token=get_recover_token())  # 从txt读取

    user_info = api.user_detail(user)
    username = user_info['user']['name']

    illust_list = get_user_illusts(api, user)
    get_data(illust_list, user, username, save_data)



def one_line_mode(user_id:int=None):
    if not user_id:
        user_ada = 88213414
        do_stats(user_ada)
    else:
        do_stats(user_id)


def arg_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=int, help="The Pixiv user ID to use")
    args = parser.parse_args()

    user = args.user
    do_stats(user)


def get_info_inf():
    while True:
        uid = input ("> 输入uid: ")
        try:
            uid_int = int(uid)
            do_stats(uid_int, save_data=False)
            print("==========")
        except Exception:
            continue

if __name__ == '__main__':
    # one_line_mode()
    # get_info_inf()
    arg_mode()
