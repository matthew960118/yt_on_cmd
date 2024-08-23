import cv2
import os
import subprocess

width = 150
height = 50 

file_name = "./Myomyomyomyomyomyomyon.mp4"

cap = cv2.VideoCapture(file_name)
fourcc = cv2.VideoWriter.fourcc(*'mp4v')         
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width,  height)) 
if not cap.isOpened():
    print("Cannot open camera")
    exit()

counter = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("\nsuccess resize!")
        break
    img_1 = cv2.resize(frame,(width,height))  
    # img_2 = cv2.flip(img_1, 0)             
    out.write(img_1)
    counter+=1

    #Progress bar
    bar_length = 20
    x = (counter/frame_count)*100
    bar_unit = "\033[47m "
    defult = '\033[0m '
    print(f'{bar_unit*int(x/100*bar_length)+defult*(bar_length-int(x/100*bar_length))}{defult} {x:<.1f}%',end="\r") 



    # cv2.imshow('oxxostudio', frame)
    # if cv2.waitKey(1) == ord('q'):
    #     break                              
cap.release()
out.release()      # 釋放資源
cv2.destroyAllWindows()

def convert_to_mp3(file_name):
    output_file = "output.mp3"
    # 使用 subprocess 调用 ffmpeg
    command = [
        'ffmpeg', 
        '-i', file_name,     # 输入文件
        '-q:a', '0',         # 最高音质
        '-map', 'a',         # 只提取音频
        output_file          # 输出文件
    ]
    
    try:
        # 使用 subprocess 执行命令
        subprocess.run(command, check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
convert_to_mp3(file_name)
