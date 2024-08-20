# yt_on_cmd
Youtube streaming on windows cmd


此程式需要pip安裝
  yt-dlp
  opencv-python
  python-vlc
  numpy

建議使用Python 3.10以上的版本執行(本人的執行環境為 Python 3.10.2 64bit, Windows11)
好像過低的版本無法在字串使用 '\033' 或是舞法在終端機輸出此字元

此外還得去vlc的官網下載vlc撥放器(請注意電腦裡python的位元是32 or 64)
https://www.videolan.org/vlc/download-windows.html
(請注意!!! 官網預設是32位元)
載完之後重開VScode 或者 終端機

開一個新的終端機 執行此命令
wt --size 187,51 --pos 1,1  -window python yt_on_cmd_full.py -v 50
要是畫面怪怪的可以適度調整終端機的視窗大小

也可以直接執行檔案
不過需要自己將視窗拉至合適的大小
