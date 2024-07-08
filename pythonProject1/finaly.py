import time

import cv2
import numpy as np
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import cv2

class VideoReader(threading.Thread):
    def __init__(self, src=0, skip_frames=10):
        super(VideoReader, self).__init__()
        self.cap = cv2.VideoCapture(src)
        self.read_lock = threading.Lock()
        self.frame = None
        self.skip_frames = skip_frames
        self.current_frame = 0

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if self.current_frame % self.skip_frames == 0:
                with self.read_lock:
                    self.frame = frame
            self.current_frame += 1

    def get_frame(self):
        with self.read_lock:
            return self.frame

def detect_people(frame, video_time):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    found, _ = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
    for x, y, w, h in found:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if len(found) > 0:
        minutes = int(video_time // 60000)
        seconds = int((video_time % 60000) // 1000)
        with open('detections.txt', 'a') as f:
            time.sleep(1)
            f.write(f'Человек был обнаружен на {minutes}:{seconds} минут видео\n')
    return frame

def select_video():
    global cap
    filepath = filedialog.askopenfilename()
    cap = cv2.VideoCapture(filepath)
    play_video()

def play_video():
    global pause, cap
    if pause:
        return
    ret, frame = cap.read()
    if ret:
        video_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        frame = detect_people(frame, video_time)
        frame = frame.astype('uint8') # преобразование к 8-битному типу
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(10, play_video)

def pause_video():
    global pause
    pause = True

def resume_video():
    global pause
    pause = False
    play_video()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('700x500')

    video_frame = tk.Frame(root)

    lmain = tk.Label(root)
    lmain.pack()

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=select_video)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    btn_pause = tk.Button(root, text="Pause", command=pause_video)
    btn_pause.pack(side='left', padx=10)
    btn_resume = tk.Button(root, text="Resume", command=resume_video)
    btn_resume.pack(side='left')

    root.mainloop()