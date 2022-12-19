
import os
from tqdm import tqdm
from pixivpy3 import *
from typing import *
import time
import csv
from datetime import datetime, timezone

from private.my_users import *
from pxdata.utils import *
from pxdata.class_illust import *
import statistics


def get_recover_token(user:str="yada"):
    """实际获取token:
    https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde
    """
    if user.lower() == "yada":
        with open("private/recover_token_yada.txt") as fd:
            line = fd.readline()
            return line
    elif user.lower() == "ada":
        with open("private/recover_token_ada.txt") as fd:
            line = fd.readline()
            return line


def get_user_illusts(api: AppPixivAPI, user_tup: Tuple) -> List[Dict]:
    """返回pixiv id=<user>的所有illust json
    """
    user=user_tup[0]

    all_illusts = []

    json_result = api.user_illusts(user)
    all_illusts += json_result['illusts']

    pbar = tqdm(desc="collecting info for user %s: "%user)
    while json_result["next_url"]:
        time.sleep(0.5)
        next_qs = api.parse_qs(json_result.next_url)
        json_result = api.user_illusts(**next_qs)
        all_illusts += json_result['illusts']
        pbar.update(30)

    return all_illusts



def get_user_insights(illust_class_list:List[Illust]):
    """返回有效信息
    :param illust_class_list:
    """
    views_list = [i.total_view for i in illust_class_list]
    pages_list = [i.page_count for i in illust_class_list]
    view_per_hour_list =  [i.view_per_hour for i in illust_class_list]


    results_dict_CN = {
        "总页数": sum(pages_list),
        "总访问": sum(views_list),
        "每小时平均阅读量": statistics.mean(view_per_hour_list)




    }

    print("D")



def illusts_to_csv_single_day(illust_list:List, user_tup:Tuple):
    """
    :param illust_list: 获取到的illusts
    :return: csv文件
    """
    # Get the current datetime with the timezone set to the past_date timezone
    current_date = datetime.now(timezone.utc)
    illust_class_list = [Illust(i, current_date) for i in illust_list]
    file_prefix = user_tup[1]  # "name"

    filename= file_prefix + "_"+ get_time_string() + '.csv'
    out_dir = "./private/csv"
    mkdir_if_not_exist(out_dir)
    out_path = os.path.join(out_dir, filename)

    get_user_insights(illust_class_list)

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


def do_stats(user_tup: Tuple):
    """工厂模式; 用user string对应实际方案
    """
    api = AppPixivAPI()
    token = get_recover_token()
    api.auth(refresh_token=token)  # ada

    i_liust = get_user_illusts(api, user_tup)
    illusts_to_csv_single_day(i_liust, user_tup)
    print("%d post data exported"%len(i_liust))


if __name__ == '__main__':
    user_ada = (88213414, "ada")
    user_ion = (12361723, "ion")

    # do_stats("yada")
    do_stats(user_ion)
