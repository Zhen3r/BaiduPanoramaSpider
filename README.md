# BaiduPanoramaSpider

![GitHub](https://img.shields.io/badge/license-MIT-green)
![GitHub](https://img.shields.io/badge/python-3.6-blue)

百度全景/街景图爬虫 Baidu Panorama Spider / Baidu Street View spider / BSV

**免责声明：本项目旨在学习python的一点实践，不可使用于商业和个人其他意图。若使用不当，均由个人承担。**

Disclaimer: This project is intended to learn Python and should not be used for commercial or personal purposes. Any improper use shall be borne by the individual.

## Usage

```python
from baiduImgSpider import baiduImgDownloader

baiduImgDownloader(pointsCsvPath, toFolderPath, baiduApiKey, zoom=3)
```

**pointsCsvPath**: WGS84 points csv file

| X        | Y        |
| -------- | -------- |
| 121.4 | 31.2 |
| 121.5 | 31.2 |
| 121.6 | 31.2 |
| ...      | ...      |

**toFolderPath**: folder to store the pictures

**baiduApiKey**: api key to project wgs84 to bd09mc

**zoom**: 

|zoom| 1       | 2        | 3         | 4         |
| -  | ------- | -------- | --------- | --------- |
|img | 512*256 | 1024*512 | 2048*1024 | 4096*2048 |



## Dependency

```
pandas
pillow
requests
```



## Technical Route

wgs84 points => bd09mc points => getImageID => getImage => mergeImage => saveImage

## Problems

网络上找到的方法还无法实现高精度的wgs84 => bd09mc，只有借助baiduApi，不是特别爽。

如果有知道解决方法的大佬请赐教！


