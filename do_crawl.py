def do_crawl():
    import pixiv_crawler as pc

    pc.set_value('username', 'your account name')
    pc.set_value('password', 'your account password')
    # pc.set_value('socks','127.0.0.1:8388')
    # pc.set_value("local_save_root","./%y.%m.%d")
    # pc.set_value("cookies_file","./cookies.txt") # cookies in json format
    # pc.set_value("garage_file","./garage.txt")
    pc.set_value("phantomjs",
                 "/usr/local/bin/phantomjs")  # for simulating log in process. the path will be (bala...)/phantomjs.exe on Windows
    pc.login()

    pc.dl_rank_daily(20)
    pc.dl_bookmark(20)
    pc.dl_artist(4187518, pic_num=-1, deep_into_manga=False)
    pc.dl_tag('azur lane', 20)
    pc.dl_diy_urls(['https://www.pixiv.net/ranking.php?mode=weekly'], 20)

    
if __name__ == '__main__':
    do_crawl()