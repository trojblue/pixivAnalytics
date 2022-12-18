import os
from pixivpy3 import *
from typing import *
import time
import csv
from datetime import datetime, timezone
from .private.my_users import *
from tqdm import tqdm




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

def get_time_string():
    return datetime.now().strftime("%y.%m.%d_%H%M")

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


def get_hourly_time_difference(past_date, current_date):
    """计算投稿时间和爬虫开始时间之间的小时差
    past_date: string
    current_date: datetime object
    """
    # Parse the past_date string into a datetime object
    past_date = datetime.fromisoformat(past_date)

    # Calculate the difference in hours between the past_date and the current time
    difference_in_hours = (current_date - past_date).total_seconds() / 3600

    return difference_in_hours


def illusts_to_csv_single_day(art_list:List, user_tup:Tuple):
    """
    :param art_list: 获取到的illusts
    :return: csv文件
    """
    file_prefix = user_tup[1]  # "name"

    # Get the current datetime with the timezone set to the past_date timezone
    current_date = datetime.now(timezone.utc)
    filename= file_prefix + "_"+ get_time_string() + '.csv'
    out_dir = "./private/csv"
    out_path = os.path.join(out_dir, filename)

    with open(out_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['create_date', 'id', 'title', 'views', 'bookmarks', 'width', 'height',
                         'bookmark/h', 'view/h', 'book_view_rate', 'view_book_rate'])

        for d in art_list:
            c_date = d['create_date']

            post_date = datetime.fromisoformat(c_date)
            current_date = current_date.astimezone(post_date.tzinfo)
            pasted_hours = (current_date - post_date).total_seconds() / 3600

            bm_per_hour = '%.2f' % (d['total_bookmarks'] / pasted_hours)  # 每小时书签量
            view_per_hour = '%.2f' % (d['total_view'] / pasted_hours)

            book_view_rate = '%.2f' % (d['total_bookmarks']/ d['total_view'])
            view_book_rate = '%.2f' % (d['total_view'] / d['total_bookmarks'])

            # EXCEL生成URL列: =HYPERLINK("http://www.pixiv.net/artworks/"&B2)

            writer.writerow(
                [c_date, d['id'], d['title'], d['total_view'], d['total_bookmarks'], d['width'], d['height'],
                 bm_per_hour, view_per_hour, book_view_rate, view_book_rate])


def do_stats(user_tup: Tuple):
    """工厂模式; 用user string对应实际方案
    """
    api = AppPixivAPI()
    token = get_recover_token()
    api.auth(refresh_token=token)  # ada

    i_liust = get_user_illusts(api, user_tup)
    illusts_to_csv_single_day(i_liust, user_tup)


if __name__ == '__main__':
    user_ada = (88213414, "ada")

    # do_stats("yada")
    do_stats(user_ada)
