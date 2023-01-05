import calendar
import json
import re
import random
import time

import sdtools.txtops as txtops
from pathlib import Path
from pixivpy3 import *
from get_stats import *
from datetime import datetime, timedelta


def get_debug_data(api, debug=False, date:str=None, min_fav=3000):
    monthly_list = []
    # get all page:
    next_qs = {"mode": "month"}
    json_result = api.illust_ranking(**next_qs)
    for illust in json_result.illusts:
        if illust['type'] == 'illust' and illust['total_bookmarks'] > min_fav:
            monthly_list.append(illust)
    return monthly_list


def get_monthly_data_by_day(api, date:str, min_fav=3000):
    """
    P站月榜illusts
    :param api: pixivpy3
    :param date:    '2022-01-13'
    :param min_fav:  含入return的最少favorite数量
    :return:
    """
    monthly_list = []
    next_qs = {"mode": "month",
               "date": date}

    while next_qs:
        json_result = api.illust_ranking(**next_qs)
        for illust in json_result.illusts:

            # illust; bookmark > 3000
            if illust['type'] == 'illust' and illust['total_bookmarks'] > min_fav:
                monthly_list.append(illust)

        next_qs = api.parse_qs(json_result.next_url)
        time.sleep(random.uniform(0.6, 2))

    return monthly_list


def set_name(illust, url, index=10000):
    """
    设置名称
    :param illust:
    :param url:
    :param index:
    :return:
    """
    extension = os.path.splitext(url)[1]
    creator = illust.user.name
    ctime = illust.create_date[:10].replace("-", '')

    # px_20221207_lack_pid103399446.png
    name = "px_%s_%s_pid%s_%d" % (ctime, creator, illust.id, index) + extension
    name = re.sub(r'_10000', '', name)

    name = txtops.remove_emojis(name)
    name = txtops.recursive_replace(name, "\\", ".")  # check sdtools package for details
    name = txtops.recursive_replace(name, "/", ".")
    name = txtops.recursive_replace(name, "\"", ".")

    return name


def get_single_illust(api, dst_path, illust):
    """
    :param api:
    :param dst_path:
    :param illust:
    :return:
    """

    image_url = illust.meta_single_page.original_image_url  # 单页
    true_image_url = image_url

    if not image_url:  # 多页
        if not illust.meta_pages:
            print("image_url 获取失败: pid%s" % illust.id)
            return
        else:
            image_url_multi = illust.meta_pages[0].image_urls.original  # todo: 多页图只保留了一张
            true_image_url = image_url_multi

    # 下载图片
    img_name = set_name(illust, true_image_url)
    try:
        api.download(true_image_url, path=dst_path, fname=img_name)
    except Exception as e:
        print("下载失败: pid%s \n" % illust.id, e)
        return

    # 保存tag
    px_tags = []
    for tag in illust.tags:
        if tag.translated_name:
            px_tags.append(tag.translated_name)

    # 写入tag到txt
    txt_name = Path(img_name).stem + ".txt"
    txt_path = os.path.join(dst_path, txt_name)

    with open(txt_path, "w", encoding="utf-8") as f:
        px_tag_str = ', '.join(px_tags) + ", [by %s]" % (illust.user.name)

        px_tag_str = px_tag_str.replace('(', '\\(')  # bracket escape
        px_tag_str = px_tag_str.replace(')', '\\)')
        px_tag_str = px_tag_str.replace('+', 'plus')

        f.write(px_tag_str)


def do_crawl_data(date:str):
    """

    :param date:  '2022-12-4'
    :return:
    """
    api = AppPixivAPI()
    # api.login("username", "password")   # Not required
    api.auth(refresh_token=get_recover_token())  # 从txt读取

    download_path = os.path.join("D:\CSC3\pixivAnalytics\privates\px_out", date)
    mkdir_if_not_exist(download_path)

    illusts = get_monthly_data_by_day(api, date=date)

    # 保存json
    time_str = get_time_string()
    json_path = os.path.join(download_path, "crawl_" + time_str + ".json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(illusts, f, indent=2)

    # 下载图片
    pbar = tqdm(illusts)
    for illust in pbar:
        pbar.set_description("downloading pid%s: " % illust.id)
        get_single_illust(api, download_path, illust)

        delay_time = random.uniform(0.5, 1.6)
        time.sleep(delay_time)

    print("%s images downloaded"%len(illusts))

def crawl_biweekly():

    # 2022 双周
    dates = []
    for i in range (1, 11):
        dates.append("2022-%s-19"%i)

    for curr_date in dates:
        print(curr_date)
        do_crawl_data(curr_date)


def get_gapped_days(year:int, month:int, gap_days:int)->List[str]:
    """
    给出年月和gap, 列出所有从1号开始间隔gap_days的日期
    :param year:
    :param month:
    :param gap_days:  The gap in days between each date.
    :return:  ['YYYY-MM-DD']
    """
    num_days = calendar.monthrange(year, month)[1]
    dates = []
    for day in range(1, num_days+1, gap_days):
        date = datetime(year, month, day).date()
        dates.append(date.strftime("%Y-%m-%d"))
    return dates

def get_monthly_illusts(year:int, month:int, min_fav:int=2500, gap_days:int=3) ->Dict:
    """
    爬取<year>年<month>月 上过P站月榜且至少有<min_fav>收藏的插画
    :param year:
    :param month:
    :param fav_limit: 最少多少favorite
    :param gap_days: 每隔几天采集一次
    :return:
    """
    api = AppPixivAPI()
    # api.login("username", "password")   # Not required
    api.auth(refresh_token=get_recover_token())  # 从txt读取

    seen_id_list = []
    monthly_illusts = {}

    dates = get_gapped_days(year, month, gap_days)
    pbar = tqdm(dates)

    for date in pbar:
        monthly_illusts[date] = []
        pbar.set_description("updating %s"%date)
        illusts = get_monthly_data_by_day(api, date=date, min_fav=min_fav)

        for illust in illusts:
            if illust.id not in seen_id_list:
                monthly_illusts[date].append(illust)
                seen_id_list.append(illust.id)

        time.sleep(random.uniform(2, 5))


    return monthly_illusts


def dump_json(dir, filename, json_file):
    full_path = os.path.join(dir, filename)
    with open(full_path, "w", encoding='utf-8') as f:
        json.dump(json_file, f, indent=2)


def get_monthly_ranking_jsons(year:int):

    for month in [1]:
        json_name = f"pixiv_rank_monthly_{year}{month:02d}.json"
        monthly_illusts = get_monthly_illusts(year, month)
        dump_json(os.getcwd(), json_name, monthly_illusts)
        time.sleep(60)



if __name__ == '__main__':

    get_monthly_ranking_jsons(2022)


    # date = '2022-11-4'
    # do_crawl_data(date=date)

    # crawl_biweekly()

    # dates = []
    # for i in range (1, 11):
    #     dates.append("2022-%s-4"%i)
    #
    # for curr_date in dates:
    #     print(curr_date)
    #     do_crawl_data(curr_date)

