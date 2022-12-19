# Pixiv-Analytics

功能目前只有两个: 爬取某个作者的所有投稿, 导出数据到csv, 导出总结数据到txt. 基于[pixivpy](https://github.com/upbit/pixivpy)

包含项:
![img.png](img.png)

txt总结:
```
用户: [Ada] 88213414  |  Mon Dec 19 08:30:31 2022

投稿数:131  总阅读:72721  总收藏:26462  总图片数:186
 平均阅读:555.122
 平均收藏:202.000
 平均收藏/阅读:0.364
 平均图片数:1.420
 
最高阅读:2292  pid=102916847
最高收藏:1007  pid=102916847

每投稿收藏/阅读比  mean:0.321  med:0.301  var:0.010  max:0.550  min:0.106
 阅读量/h (每投稿) mean:2.673  med:1.770  var:5.406  max:10.010  min:0.000
 收藏数/h (每投稿) mean:0.859  med:0.680  var:0.551  max:3.580  min:0.000
 阅读量   (每投稿) mean:555.122  med:431.000  var:145188.108  max:2292.000  min:2.000
 收藏数   (每投稿) mean:202.000  med:129.000  var:36620.308  max:1007.000  min:1.000

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