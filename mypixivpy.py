import os

from pixivpy3 import *
from typing import *
from datetime import datetime
import time
import csv
from datetime import datetime, timezone

user_ada = 88213414
user_yada = 14626152


def get_recover_token_ada():
    """实际获取token:
    https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde
    """
    with open("private/recover_token_ada.txt") as fd:
        line = fd.readline()
        return line


def get_time_string():
    return datetime.now().strftime("%y.%m.%d_%H%M")

def get_user_illusts(api: AppPixivAPI, user: int) -> List[Dict]:
    """返回pixiv id=<user>的所有illust json
    """
    all_illusts = []

    json_result = api.user_illusts(user)
    all_illusts += json_result['illusts']

    while json_result["next_url"]:
        time.sleep(0.5)
        next_qs = api.parse_qs(json_result.next_url)
        json_result = api.user_illusts(**next_qs)
        all_illusts += json_result['illusts']

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


def illusts_to_csv_single_day(art_list, file_prefix):
    """
    :param art_list: 获取到的illusts
    :return: csv文件
    """
    # Get the current datetime with the timezone set to the past_date timezone
    current_date = datetime.now(timezone.utc)
    filename= file_prefix + get_time_string + '.csv'
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

            # pasted_hours = get_hourly_time_difference(c_date, current_date)
            bm_per_hour = '%.2f' % (d['total_bookmarks'] / pasted_hours)  # 每小时书签量
            view_per_hour = '%.2f' % (d['total_view'] / pasted_hours)

            book_view_rate = '%.2f' % (d['total_bookmarks']/ d['total_view'])
            view_book_rate = '%.2f' % (d['total_view'] / d['total_bookmarks'])

            # EXCEL生成URL: =HYPERLINK("http://www.pixiv.net/artworks/"&B5)

            writer.writerow(
                [c_date, d['id'], d['title'], d['total_view'], d['total_bookmarks'], d['width'], d['height'],
                 bm_per_hour, view_per_hour, book_view_rate, view_book_rate])


def get_info(api: AppPixivAPI, user: int):
    ada_details = api.user_detail(user)
    usr_following = api.user_following(user)
    usr_followers = api.user_follower(user)

    print("D")


def demo():
    api = AppPixivAPI()
    token = get_recover_token_ada()
    api.auth(refresh_token=token)  # ada

    i_liust = get_user_illusts(api, user_yada)
    illusts_to_csv_single_day(i_liust)

    # # get origin url
    # json_result = api.illust_detail(59580629)
    # illust = json_result.illust
    # print(">>> origin url: %s" % illust.image_urls['large'])
    #
    # # get ranking: 1-30
    # # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # json_result = api.illust_ranking('day')
    # for illust in json_result.illusts:
    #     print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))
    #
    # # next page: 31-60
    # next_qs = api.parse_qs(json_result.next_url)
    # json_result = api.illust_ranking(**next_qs)
    # for illust in json_result.illusts:
    #     print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))
    #
    # # get all page:
    # next_qs = {"mode": "day"}
    # while next_qs:
    #     json_result = api.illust_ranking(**next_qs)
    #     for illust in json_result.illusts:
    #         print("[%s] %s" % (illust.title, illust.image_urls.medium))
    #     next_qs = api.parse_qs(json_result.next_url)


if __name__ == '__main__':
    demo()
