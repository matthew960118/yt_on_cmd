import vlc,cv2
import yt_dlp
import time
import os
import argparse
import numpy as np

#------------------------自定義參數------------------------#

##請不要從這裡修改預設值!!

parser = argparse.ArgumentParser()

parser.add_argument('url',type=str,nargs='?', help="Youtube 影片的url")
parser.add_argument("--width", type=int, default=187, help="視窗寬(太寬可能會超出螢幕範圍)")
parser.add_argument("--height", type=int, default=50, help="視窗高(太高可能會超出螢幕範圍)")
parser.add_argument('-t',"--title", type=str, default=" ", help="畫面填充的文字 (預設空白)")
parser.add_argument("-v","--volume", type=int, default=20, help="音量")
#---------------------------------------------------------#

args = parser.parse_args()
if args.url==None:
    args.url = input("請輸入Youtube網址:\n")
youtube_url = args.url # 撥放的url
width = args.width # 影片寬
height = args.height # 影片高
title = args.title # 畫面要用甚麼詞填充 (預設空白)
volume = args.volume # 音量
aspect_ratio = 19/9 # 字的長寬比 Windows11終端機預設是19:9(H:w)

CLEAR_SCREEN = '\033[3J'
BACK_TO_AHEAD = '\033[H'
mySign = "    created by Matthew"

title_counter = -1

# 定義單個像素
def pixel(color):
    b, g, r = color
    global title_counter
    title_counter=title_counter+1
    return f'\033[48;2;{r};{g};{b};38;2;{255-r};{255-g};{255-b}m{title[title_counter%len(title)]}'
# 渲染畫面
# def print_img(img):
#     global title_counter
#     a = ''
#     for i in range(height):
#         # print()
#         title_counter=-1
#         # if i!=height-1:
#         #     a = ''
#         #     for j in range(width):
#         #         a+=pixel(img[i,j])
#         #     print(a,end="")
            
#         # else:
#         #     for j in range(width-len(mySign)):
#         #         print(pixel(img[i,j]),end="")
#         #     print(mySign,end="")
#         for j in range(width):
#             a+=pixel(img[i,j])
#         a+='\n'
#     print(a,end="")

## 渲染畫面 優化板
def print_img(img):
    lines = []
    for i in range(height):
        line = ''.join(pixel(img[i, j]) for j in range(width))
        lines.append(line)
    
    print('\n'.join(lines))
# 獲得串流url (影片)
def get_stream_url(url):
    ydl_opts = {
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        print(info_dict['title'])
        return info_dict
info = get_stream_url(youtube_url)

stream_url = info['url']

#vlc不輸出畫面
instance = vlc.Instance('--no-video', '--aout=directx')
player = vlc.MediaPlayer(instance)

player.set_media(vlc.Media(stream_url))
player.audio_set_volume(volume)

cap = cv2.VideoCapture(stream_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

fps = cap.get(cv2.CAP_PROP_FPS)
# total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

os.system("cls")
startTime = time.time()
w = info['width']
h = info['height']

#計算縮放比例
scale_W = width/w
scale_H = height/h
scale = min(scale_H,scale_W)
new_H = int(h*scale)
new_W = int(w*scale*(aspect_ratio))#調整長寬比

#調整至中
x_offset = (width - new_W) // 2
y_offset = (height - new_H) // 2

black_background = np.zeros((height, width, 3), dtype=np.uint8)
index=0
player.play()
while True:
    #讀取幀 並 resize
    ret, frame = cap.read()
    if not ret:
        # print("\nsuccess resize!")
        break

    img_1 = cv2.resize(frame, (new_W,new_H), interpolation=cv2.INTER_AREA)
    black_background[y_offset:y_offset+new_H,x_offset:x_offset+new_W] = img_1

    #畫面渲染
    print(CLEAR_SCREEN,end='')
    print(BACK_TO_AHEAD,end='')
    print_img(black_background)
    
    #計算渲染速度快了多少 防止畫面播太快 導致音畫不同步
    sleepTime = index/fps - time.time() +startTime
    if sleepTime >0:
        time.sleep(sleepTime)
    #計算染速度慢了多少 跳過指定數量的幀
    elif sleepTime<0:
        currect_frame = int((time.time()-startTime)*fps)
        for i in range(currect_frame-index):
          success, frame = cap.read()
          if not success:
              break
        index = currect_frame
    
    index+=1



