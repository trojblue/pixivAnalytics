from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# https://learnku.com/python/t/56814

class Browser():

    def __init__(self):

        driver_path = "D:/Python/Project/chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.login()

    def close(self):

        self.browser.close()

    def login(self):

        login_url = (
            "https://accounts.pixiv.net/login?"
            "return_to=https%3A%2F%2Fwww.pixiv.net%2F&"
            "lang=zh_cn&source=pc&view_type=page")

        username = "你的帐号名称"
        password = "你的帐号密码"

        self.browser.get(login_url)
        # element = self.browser.find_element_by_xpath("// input [@ autocomplete ='username']")
        # element.send_keys(username)
        # element = self.browser.find_element_by_xpath("// input [@ autocomplete ='current-password']")
        # element.send_keys(password)
        # element.send_keys(Keys.ENTER)
        # element = element.find_element_by_xpath("// button [@ type ='submit']").click
        a = input("好了回车")

        sleep (10)

    def get(self, url):
        self.browser.get(url)
        return self.browser.page_source


if __name__ == '__main__':
    url = "https://www.pixiv.net/ajax/user/432332/profile/all?lang=zh"
    browser = Browser()
    content = browser.get(url)
    browser.close()

    print(content)