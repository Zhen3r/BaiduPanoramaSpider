import requests,json
from PIL import Image
from io import BytesIO
from math import ceil
import pandas as pd
import time
import os


def getImageID(x,y):
	# input: x, y (bd09mc) 
	# output: sid (imgID)
	url = f"https://mapsv0.bdimg.com/?qt=qsdata&x={x}&y={y}"
	h = requests.get(url).text
	return json.loads(h)

def getImageBytesList(sid,z=2):
	# input: sid (imgID)
	# output: List of imgBytes
	if z==2:
		xrange,yrange=1,2
	elif z==3:
		xrange,yrange=2,4
	elif z==1:
		xrange,yrange=1,1
	elif z==4:
		xrange,yrange=4,8
	imgBytes=[]
	for x in range(xrange):
		for y in range(yrange):
			url = f"https://mapsv0.bdimg.com/?qt=pdata&sid={sid}&pos={x}_{y}&z={z}"
			b = requests.get(url).content
			imgBytes.append(b)
	return imgBytes

def bytes2Img(imgByte):
	# input: imgByte
	# output: PIL.Image
	return Image.open(BytesIO(imgByte))

def bytesList2ImgList(x):
	# input: List of imgBytes
	# output: List of PIL.Image
	return [bytes2Img(_) for _ in x]

def mergeImage(imgList,imgNumPerRow):
	# input: List of PIL.Image, imgNumPerRow
	# output: merged image
	assert isinstance(imgList[0],Image.Image)
	w,h = imgList[0].size
	rowNum = ceil(len(imgList)/imgNumPerRow)
	width = w * imgNumPerRow
	height = h * rowNum
	newImg = Image.new("RGB",(width,height))
	for i,img in enumerate(imgList):
		x = i//imgNumPerRow
		y = i%imgNumPerRow
		newImg.paste(img,(y*h,x*w,))
	return newImg

def download(x,y,zoom,fp):
	# input: x, y (bd09mc)
	# output: None
	# saves the picture
	imgPerRow = {1:1,2:2,3:4,4:8}
	imgId = getImageID(x,y)["content"]['id']
	imgBytes = getImageBytesList(imgId,z=zoom)
	imgList = bytesList2ImgList(imgBytes)
	img = mergeImage(imgList,imgPerRow[zoom])
	img.save(fp)
	
def inputPoints(fp):
	# input: WGS84 points csv file
	# output: list of str which consists 100 points
	points = pd.read_csv(fp,encoding="utf8")
	points = points.to_numpy().tolist()
	points100 =[]
	for i,(x,y) in enumerate(points):
		n = i//100
		if len(points100)==n:
			points100 += [f"{x},{y}"]
		else:
			points100[n] += f";{x},{y}"
	return points100	

def convertWGStoBD09MC(coords,ak):
	# input: list of str which consists 100 points, baiduapi ak
	# output: list of BD09MC points
	url = f"http://api.map.baidu.com/geoconv/v1/?coords={coords}&from=1&to=6&ak={ak}"
	h = requests.get(url)
	points = json.loads(h.text)
	points = [[x["x"],x["y"]] for x in points['result']]
	return points

def baiduImgDownloader(pointsCsvPath,toFolderPath,ak,zoom=3):
	# input: WGS84 points csv file, toFolderPath, baiduapi ak, zoom
	# output: None
	points100 = inputPoints(pointsCsvPath)
	points = []
	for p in points100:
		points += convertWGStoBD09MC(p,ak)
	for i,(x,y) in enumerate(points):
		fp = os.path.join(toFolderPath,f"{i:0>5d}.jpg")
		download(x,y,zoom,fp)
		time.sleep(3)
		print(fp)
