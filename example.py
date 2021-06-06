from baiduImgSpider import baiduImgDownloader
import json

# f = open("./resources/ak.json","r")
# YourAK = json.load(f)
# f.close()

YourAK = "****"

baiduImgDownloader("resources/example.csv", # CRS: WGS84
                    "resources/downloadPic", # folder
                    ak=YourAK, zoom=3)