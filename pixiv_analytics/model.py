import json
import logging

from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


# Local path
COOKIE_PATH = './private/cookies.json'
0
# ======= Header =========

# 通用header, 如果相同会被下面的其他header覆盖
HEADER_UNIVERSAL = {
    'cookie_list': "===CHANGE ME===",
    'connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
}

HEADER_TSDM_WORK = {
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work',
        'content-type': 'application/x-www-form-urlencoded'
}

HEADER_TSDM_SIGN = {
    'accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'referer': 'https://www.tsdm39.net/home.php?mod=space&do=pm',
    'content-type': 'application/x-www-form-urlencoded'
}

HEADER_S1_READ = {
        'referer': 'https://bbs.saraba1st.com/2b/forum-6-1.html',
}

HEADER_EAT_SIGN = {
        'referer': 'https://eatasmr.com/tasks/attendance',
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'content-type': "application/x-www-form-urlencoded",
        'origin': "https://eatasmr.com"
    }


# ====== URL ========

tsdm_sign_url = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign'
sign_url_with_param = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1'

work_url = 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work'
login_url = 'https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net'

s1_frontpage = "https://bbs.saraba1st.com/2b/forum.php"
s1_sample_post = "https://bbs.saraba1st.com/2b/thread-2022232-1-1.html"

# cookie_list domain
tsdm_domain = ".tsdm39.net"
s1_domain = "bbs.saraba1st.com"
eatasmr_domain = "eatasmr.com"

# re相关
re_URL = "(?P<url>https?://[^\s]+)"



# ========= COOKIES =======
def get_cookie_pixiv(username: str, password: str):
    """selenium获取cookie
    """
    driver = get_webdriver()
    profile = webdriver.FirefoxProfile()

    # driver.get(login_url)

    driver.get("https://www.pixiv.net/en/users/88213414")
    # 手动填写信息


    logged_in = input("登陆完后回车")

    new_cookie = driver.get_cookies()
    driver.close()

    write_new_cookie(new_cookie, username)
    return new_cookie

def get_cookies_tsdm_all():
    """从credentials重新获取所有cookie
    """
    try:
        # 多账户刷新
        from private.settings import TSDM_CREDENTIALS
        for i in TSDM_CREDENTIALS:
            get_cookie_pixiv(i[0], i[1])

    except ImportError:
        get_cookie_pixiv("", "")

    return


def get_cookies_all() -> Dict:
    """从文件读取所有cookies
    { username: [cookie_list] }
    """
    try:
        with open(COOKIE_PATH, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        return {}


def get_cookies_by_domain(domain:str):
    """从所有cookie里分离出指定域名的cookie
    domain: cookie_list domain, (".tsdm39.net")
    """
    cookies_all = get_cookies_all() #     { username: [cookie_list] }
    domain_cookies = {}

    for username in cookies_all.keys():
        curr_user_cookies = cookies_all[username]
        curr_user_cookies_domained = []

        # 同一个用户名下可能有多个网站的cookie
        for cookie in curr_user_cookies:
            if cookie['domain'] == domain:
                curr_user_cookies_domained.append(cookie)

        if curr_user_cookies_domained != []:
            domain_cookies[username] = curr_user_cookies_domained

    return domain_cookies

def write_new_cookie(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie_list] }
    """
    simplified_new_cookie = simplify_cookie(new_cookie)
    cookies = get_cookies_all()

    # TODO: 相同名称的直接覆盖, 不同站点的用不同cookie文件, 或者机制检测
    cookies[username] = simplified_new_cookie

    with open(COOKIE_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)



def write_new_cookie_all(new_cookie: List, username: str) -> None:
    """写入所有新的用户cookie
    { username: [cookie_list] }
    """
    cookies = get_cookies_all(COOKIE_PATH)
    # TODO: 相同名称的直接覆盖, 不同站点的用不同cookie文件, 或者机制检测
    cookies[username] = new_cookie

    with open(COOKIE_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)



def simplify_cookie(cookie):
    """只保存登录需要的2个cookie: saltkey, auth
    """
    simplified_cookie = []
    login_word = ['_saltkey', '_auth', 'EATSESSID',
                  'wordpress_logged_in_bbae6ecd47232ff70d42a5fbe3863254']
    for i in cookie:
        if any(word in i['name'] for word in login_word):
            simplified_cookie.append(i)

    return simplified_cookie


# ========= Others =======

def get_webdriver():
    """返回设置好参数的webdriver
    """
    # 进入浏览器设置
    options = webdriver.ChromeOptions()
    # 设置中文

    options = webdriver.ChromeOptions()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    options.add_argument("disable-software-rasterizer")
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument("log-level=3")
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def get_serialized_cookie(cookie_list:List):
    return "; ".join([i['name'] + "=" + i['value'] for i in cookie_list])

def write_error(prefix:str, content:str):
    """保存错误日志
    prefix: 文件名前缀
    content: 错误日志内容
    """
    my_date = prefix + datetime.today().strftime(' %Y-%m-%d %H%M %S.%f.log')
    with open(my_date, "w") as f:
        f.write(content)
    return