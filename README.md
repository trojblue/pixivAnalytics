# Pixiv-Analytics

功能目前只有两个: 爬取某个作者的所有投稿, 导出数据到csv, 导出总结数据到txt. 基于[pixivpy](https://github.com/upbit/pixivpy)

包含项:
![img_1.png](img_1.png)

txt总结:
```
用户:[88213414] Ada   | Mon Dec 19 05:24:51 2022 

投稿数:131  总阅读:72110  总收藏:26202  总页数:186
 平均阅读/投稿:550.458
 平均收藏/投稿:200.015
 平均收藏/阅读:0.363
 
平均收藏/阅读比:0.320
 阅读量/h (每投稿) mean:2.733  med:1.77000  var:5.92623 
 收藏数/h (每投稿) mean:0.868  med:0.68000  var:0.56453
 阅读量   (每投稿) mean:2.733  med:1.77000  var:5.92623
```
## 使用
```bash
git clone https://github.com/trojblue/pixivAnalytics
cd pixivAnalytics

# 下载chromedriver, 放在pixiv_auth.py 同目录下
...

# 获取refresh token
python pixiv_auth.py login

# 创建txt文件存储refresh token
echo "YOUR TOKEN HERE" > ./privates/token.txt

# 传入用户UID: 如 www.pixiv.net/users/1039353
python get_stats.py -u 1039353
```

1. 用`pixiv_auth.py`获取refresh token: 见[pixivpy](https://github.com/upbit/pixivpy) →  [selenium](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)
2. 在private文件夹下创建*.txt, 里面放你的refresh token
3. 开爬