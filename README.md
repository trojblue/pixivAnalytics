# Pixiv-Analytics

功能目前只有两个 (三个: 爬取某个作者的所有投稿, 导出数据到csv, 导出总结数据到txt. 基于[pixivpy](https://github.com/upbit/pixivpy)


## Crawler

见crawl_data.py



## Analytics

包含项:
![img.png](img.png)

txt总结: (手动打码了部分信息)
```
用户: [***26152] ***A  |  Tue May 16 10:25:57 2023

投稿数:95  总阅读:366685  总收藏:97099  总图片数:149
 平均阅读:3859.842
 平均收藏:1022.095
 平均收藏/阅读:0.265
 平均图片数:1.568
最高阅读:24749  pid=****70240
最高收藏:8946  pid=****70240

每投稿收藏/阅读比  mean:0.228  med:0.230  var:0.005  max:0.434  min:0.016
 阅读量/h (每投稿) mean:1.661  med:1.050  var:2.934  max:9.000  min:0.020
 收藏数/h (每投稿) mean:0.435  med:0.230  var:0.249  max:2.430  min:0.000
 阅读量   (每投稿) mean:3859.842  med:2882.000  var:9587557.113  max:24749.000  min:966.000
 收藏数   (每投稿) mean:1022.095  med:670.000  var:1386737.789  max:8946.000  min:15.000
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

1. 用`pixiv_auth.py`获取refresh token: 见 [pixivpy](https://github.com/upbit/pixivpy) →  [selenium](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)
2. 在private文件夹下创建*.txt, 里面放你的refresh token
3. 开爬
