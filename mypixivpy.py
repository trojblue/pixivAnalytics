from pixivpy3 import *
def demo():
    api = AppPixivAPI()
    # api.login("username", "password")   # Not required

    api.auth(refresh_token="EnKyQ-5m2BhPVD-nMl6i6aIZL6Ww1AzC7xwULOYNic4")
    # get origin url
    json_result = api.illust_detail(59580629)
    illust = json_result.illust
    print(">>> origin url: %s" % illust.image_urls['large'])

    # get ranking: 1-30
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    json_result = api.illust_ranking('day')
    for illust in json_result.illusts:
        print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))

    # next page: 31-60
    next_qs = api.parse_qs(json_result.next_url)
    json_result = api.illust_ranking(**next_qs)
    for illust in json_result.illusts:
        print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))

    # get all page:
    next_qs = {"mode": "day"}
    while next_qs:
        json_result = api.illust_ranking(**next_qs)
        for illust in json_result.illusts:
            print("[%s] %s" % (illust.title, illust.image_urls.medium))
        next_qs = api.parse_qs(json_result.next_url)

if __name__ == '__main__':

    demo()