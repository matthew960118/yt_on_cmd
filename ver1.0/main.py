import cv2
import os
import time
import pygame

###############################################
# 此為比較複雜的版本                            #
# 可以讓字顯示在畫面中                          #
###############################################

BLACK = '\033[40m '
WHITE = '\033[47m '
CLEAR_SCREEN = '\033[3J'
BACK_TO_AHEAD = '\033[H'

# video_file = "output_1.mp4" #'output.mp4'
# audio_file = "aaa.mp3"#'./output.mp3'
video_file = 'output.mp4'
audio_file = './output.mp3'
title = " "
# title = "Bad Apple "
title_counter = -1

mySign = "    created by Matthew"
def pixel(color):
    b, g, r = color
    global title_counter
    title_counter=title_counter+1
    return f'\033[48;2;{r};{g};{b};38;2;{255-r};{255-g};{255-b}m{title[title_counter%len(title)]}'

def print_img(img):
  global title_counter
  for i in range(height):
    print()
    title_counter=-1

    if i!=height-1:
        for j in range(width):
            print(pixel(img[i,j]),end="")
    else:
        for j in range(width-len(mySign)):
            print(pixel(img[i,j]),end="")
        print(mySign,end="")
height = 50
width = 150

video_capture = cv2.VideoCapture(video_file)

if not video_capture.isOpened():
    print("Error: Unable to open video file.")
    exit()

fps = video_capture.get(cv2.CAP_PROP_FPS)
total_frame = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)


all_frame = []

#撥放聲音 音量 0.1
pygame.mixer.init()
pygame.mixer.music.load(audio_file)
volume = 0.1

pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play()

os.system('cls')

#開始時的系統時間
startTime = time.time()
index = 0
while 1:
    success, frame = video_capture.read()
    if not success:
        break
    #畫面渲染
    print(CLEAR_SCREEN,end='')
    print(BACK_TO_AHEAD,end='')
    print_img(frame)
    
    #計算渲染速度快了多少 防止畫面播太快 導致音畫不同步
    sleepTime = index/fps - time.time() +startTime
    if sleepTime >0:
        time.sleep(sleepTime)
    #計算染速度慢了多少 跳過指定數量的幀
    elif sleepTime<0:
        currect_frame = int((time.time()-startTime)*fps)
        for i in range(currect_frame-index):
          success, frame = video_capture.read()
          if not success:
              break
        index = currect_frame
    
    index+=1

video_capture.release()
cv2.waitKey()