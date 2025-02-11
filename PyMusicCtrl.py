# PyMediaCtrl
# 2023~2025 by rgzz666
# Modified in 2025, removed cover art and fixed basic function, made some small changes and translated UI into English
# Do not try to learn from this piece of sh*t or change/fix anything
# Fixed it only because it is at least useful
# For more info, see the original post: https://www.cnblogs.com/TotoWang/p/py_music_ctrl.html
# Original post Archived @ 2025/02/09: http://web.archive.org/save/https://www.cnblogs.com/TotoWang/p/py_music_ctrl.html

# List of changes made on this program:
# - Fixed basic function (Use winrt-*(pywinrt on GitHub) instead of Microsoft official deprecated winrt).
# - Removed cover art.
# - Added white tray icon (for dark taskbar theme).
# - Use system dark mode flag instead of apps dark mode flag when detecting the appearance of the taskbar.
# - Added the ability to auto choose dark / light icon.
# - Changed change_icon() and moved part of it into set_icon().
# - Added text scrolling when the text is too long.
# - Changed the text to left-aligned which was centered before.
# - Translated the program into English.
# - Changed font to English Arial instead of Chinese 等线(Deng Xian).
# - Made the controls window topmost.
# - Added the ability to hide the controls when clicking the tray icon while the window is opened.
# - Changed the content of play / pause button to an image.
# - Removed unecessary imports.


import asyncio
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionPlaybackControls as GetCanDo
import tkinter as tk
from winrt.windows.storage.streams import \
    InputStreamOptions
from PIL import Image, ImageTk
import time
import threading
import winreg
import pystray
import os


async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)

async def get_media_name():
    """Get the name and artist information of the currently playing media"""
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        #if current_session.source_app_user_model_id == TARGET_ID:
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != "_" ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != "_"}

        # converts winrt vector to list
        info_dict["genres"] = list(info_dict["genres"])

        name=info_dict["title"]
        if info_dict["artist"]!="":
            artist=info_dict["artist"]
        else:
            artist="Unknown singer"
        if info_dict["album_title"]!="":
            artist+="   —   "+info_dict["album_title"]
        else:
            artist+="   —   "+"Unknown Album"

        return name,artist
    else:
        return "Not Playing","N / A"
    # It could be possible to select a program from a list of current
    # available ones. I just haven"t implemented this here for my use case.
    # See references for more information.
    # raise Exception("歌曲信息获取函数未按计划结束")

async def stop():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    info = await current_session.try_toggle_play_pause_async()

async def nextm():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    info = await current_session.try_skip_next_async()

async def prem():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    info = await current_session.try_skip_previous_async()

def refresh():
    global rft,winw,winh,scr_w,scr_h,win
    while True:
        try:
            #print("刷新")
            #名称
            mname,mar=asyncio.run(get_media_name())
            nametxt["text"]=mname
            artxt["text"]=mar
            #专辑图（PART1）
            # cover=asyncio.run(get_media_info())["thumbnail"]
            if rft%50==0:#此处表示每刷新5次才会刷新部分信息，这样可以避免大量读写导致专辑图加载（读取）错误，也可以节省性能
                #专辑图（PART2）
                #cover="NO_DATA"
                #if cover!="NO_DATA":
                #    # create the current_media_info dict with the earlier code first
                #    thumb_stream_ref = cover

                #    # 5MB (5 million byte) buffer - thumbnail unlikely to be larger
                #    thumb_read_buffer = Buffer(5000000)

                #    # copies data from data stream reference into buffer created above
                #    asyncio.run(read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer))

                #    # reads data (as bytes) from buffer
                #    buffer_reader = DataReader.from_buffer(thumb_read_buffer)
                #    byte_buffer = buffer_reader.read_bytes(thumb_read_buffer)

                #    with open("media_thumb.jpg", "wb+") as fobj:
                #        fobj.write(bytearray(byte_buffer))
                #    imgf=Image.open("media_thumb.jpg")
                #    imgf = imgf.resize((250, 250))
                #    img=ImageTk.PhotoImage(imgf)
                #    imgt["image"]=img
                #else:
                #    imgf=Image.open("media_thumb_none.jpg")
                #    imgf = imgf.resize((250, 250))
                #    img=ImageTk.PhotoImage(imgf)
                #    imgt["image"]=img
                #亮暗模式
                set_appearance()
            #强制大小
            win.geometry(str(winw)+"x"+str(winh))
            #刷新间隔，避免循环过于紧凑导致无法控制时间以及产生未知的BUG
            time.sleep(0.01)
            #print(win.state())
            rft+=1
        except Exception as e:
            print(e)
            #raise Exception("信息刷新错误："+str(e))

def get_dark(taskbar=False): 
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            keyname="SystemUsesLightTheme" if taskbar else "AppsUseLightTheme"
            if value_name == keyname:
                return value == 0
        except OSError:
            break
    return False

def set_appearance():
    if get_dark():
        win.configure(background="#101010")
        nametxt["bg"]="#101010"
        name_row["bg"]="#101010"
        nametxt["fg"]="#FFFFFF"
        artxt["bg"]="#101010"
        ar_row["bg"]="#101010"
        #artxt["fg"]="#FFFFFF"
        #imgt["bg"]="#101010"
        prembtn["bg"]="#101010"
        prembtn["fg"]="#FFFFFF"
        nextmbtn["bg"]="#101010"
        nextmbtn["fg"]="#FFFFFF"
        stopbtn["bg"]="#0078D7"
        stopbtn["fg"]="#FFFFFF"
    else:
        win.configure(background="#FFFFFF")
        nametxt["bg"]="#FFFFFF"
        name_row["bg"]="#FFFFFF"
        nametxt["fg"]="#000000"
        artxt["bg"]="#FFFFFF"
        ar_row["bg"]="#FFFFFF"
        #artxt["fg"]="#000000"
        #imgt["bg"]="#FFFFFF"
        prembtn["bg"]="#FFFFFF"
        prembtn["fg"]="#000000"
        nextmbtn["bg"]="#FFFFFF"
        nextmbtn["fg"]="#000000"
        stopbtn["bg"]="#A6D8FF"
        stopbtn["fg"]="#000000"

def close(icon=None,item=None):
    os._exit(0)
 
def show_window(icon=None,item=None):
    win.geometry(str(winw)+"x"+str(winh)+"+"+str(int(scr_w-winw-10))+"+"+str(int(scr_h-winh-75)))
    win.deiconify()

def set_icon(icona=None,item=None,start=False):
    global use_color_icon,icon,iconimg,menu
    #print(use_color_icon)
    if use_color_icon:
        #use_color_icon=True
        iconimg = Image.open("./imgs/icon_colorful.png")
    else:
        #use_color_icon=False
        if get_dark(taskbar=True):
            iconimg = Image.open("./imgs/icon_dark.png")
        else:
            iconimg = Image.open("./imgs/icon_light.png")
    if not start:
        icon.stop()
    icon = pystray.Icon("PyMediaCtrl",iconimg,"Media Controls",menu)
    icon.run_detached()

def change_icon():
    global use_color_icon
    use_color_icon=not use_color_icon
    set_icon()

def toggle_win(icon=None,item=None):
    global win
    if win.state()=="withdrawn":
        show_window()
    elif win.state()=="normal":
        win.withdraw()
    else:
        print("Unknown window state, it will be set to withdrawn.")
        win.withdraw()

def scroll_txt(target,target_index):
    global win,txt_scroll_reverse
    last_txt=target["text"]
    while True:
        if target["text"]!=last_txt: #文本内容头变化，重新归位从头开始
            target.place(x=5,y=0)
            last_txt=target["text"]
        if target.winfo_width()>win.winfo_width():
            if not txt_scroll_reverse[target_index]: #正向滚动
                for i in range((target.winfo_width()-win.winfo_width()+10)):
                    target.place_configure(x=-i+5,y=0)
                    win.update()
                    time.sleep(0.05)
                for i in range(10):
                    win.update()
                    time.sleep(0.05)
                txt_scroll_reverse[target_index]=True
            else: #反向滚动
                reverse_start_x=target.winfo_x()
                for i in range((target.winfo_width()-win.winfo_width()+10)//5):
                    target.place_configure(x=(reverse_start_x+i*5)+5,y=0)
                    win.update()
                    time.sleep(0.05)
                for i in range(40):
                    win.update()
                    time.sleep(0.05)
                txt_scroll_reverse[target_index]=False
        else: #如果文本不够长无需滚动则使其归位
            target.place(x=5,y=0)


txt_scroll_reverse=[False,False] #文本是否正在反向滚动
# ↑以上非配置项，勿改动！！！！

#界面
win=tk.Tk()
win.title("Media Controls")
win.resizable(0,0)
win.protocol("WM_DELETE_WINDOW",win.withdraw)
win.attributes("-toolwindow", True)
win.attributes("-topmost", True)

#imgf=Image.open("media_thumb_none.jpg")
#imgf = imgf.resize((250, 250))
#img=ImageTk.PhotoImage(imgf)
#imgt=tk.Label(win,image=img)
#imgt.pack()

name_row=tk.Frame(win)
nametxt=tk.Label(name_row,text="Loading",font=("Arial",20))
nametxt.place(x=5,y=0)
name_row.pack(fill=tk.X,)
name_row["height"]=35

ar_row=tk.Frame(win)
artxt=tk.Label(ar_row,text="Loading",font=("Arial",12),fg="#909090")
artxt.place(x=5,y=0)
ar_row.pack(fill=tk.X)
ar_row["height"]=25

btnpt=tk.Frame(win)
btnpt.pack(fill=tk.X)

stop_img=Image.open("./imgs/play_pause.png")
stop_img_resized=stop_img.resize((int(stop_img.width*(30/stop_img.height)),30))
stop_img_tk=ImageTk.PhotoImage(stop_img_resized)

prembtn=tk.Button(btnpt,text="9",command=lambda:asyncio.run(prem()),font=("webdings",25),bd=0)
prembtn.pack(side=tk.LEFT,fill=tk.X)
nextmbtn=tk.Button(btnpt,text=":",command=lambda:asyncio.run(nextm()),font=("webdings",25),bd=0)
nextmbtn.pack(side=tk.RIGHT,fill=tk.X)
stopbtn=tk.Button(btnpt,image=stop_img_tk,command=lambda:asyncio.run(stop()),bd=0,bg="#A6D8FF",width=80)
stopbtn.pack(fill=tk.BOTH,expand=True)

#获取窗口默认大小
win.update()
winw=win.winfo_width()
winh=win.winfo_height()

#屏幕尺寸
scr_w=win.winfo_screenwidth()
scr_h=win.winfo_screenheight()

#窗口大小与位置
win.geometry(str(winw)+"x"+str(winh)+"+"+str(int(scr_w-winw-10))+"+"+str(int(scr_h-winh-75)))

#先进行一次外观刷新
set_appearance()

#启动多线程
# 歌曲信息、UI外观刷新线程
rft=0#ReFresh Time
refresh_t=threading.Thread(target=refresh)
refresh_t.start()
# 文本滚动线程
name_scrolling_t=threading.Thread(target=lambda:scroll_txt(nametxt,0))
name_scrolling_t.start()
ar_scrolling_t=threading.Thread(target=lambda:scroll_txt(artxt,1))
ar_scrolling_t.start()

win.withdraw()

#托盘
use_color_icon=False
menu = (pystray.MenuItem("Show / Hide media controls",toggle_win,default=True),
        pystray.MenuItem("Exit",close),
        pystray.MenuItem("Use colored tray icon",lambda icona,item:change_icon(),checked=lambda item: use_color_icon))
set_icon(start=True)

win.mainloop()
