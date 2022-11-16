import pygame as pyg, os
from tkinter import *
from tkinter.filedialog import askdirectory
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
startedCount = False
isPaused = False
isActive = False
count=0
print("booting 'app'")
app = Tk()
app.title("Soptify")
app.geometry("400x380")
app.config(bg="black")
photo1 = ImageTk.PhotoImage(Image.open("play.png").resize((60, 60), Image.ANTIALIAS))
photo2 = ImageTk.PhotoImage(Image.open("pause.png").resize((60, 60), Image.ANTIALIAS))
photo3= ImageTk.PhotoImage(Image.open("Spotify.png").resize((300, 100), Image.ANTIALIAS))
print('tkinter boot finished')
directory = askdirectory()
os.chdir(directory)
songList = os.listdir()
playList = Listbox(app, font="Calibri 12 bold", bg="black", selectmode=SINGLE, width=45, borderwidth=0, border=0)
for item in songList:
    pos = 0
    playList.insert(pos, item)
    pos += 1
print("booting pygame.mixer")
pyg.init()
pyg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)

def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)
def pause():
    global isPaused
    if isActive is not False:
        isPaused = True
        pyg.mixer.music.pause()
        print("paused")
    else:
        isPaused = False
        print("unable to pause")
def _start():
    global count, startedCount
    if startedCount is True:
        print("startedCount = True")
        count += 1
        print(count)
        return convert(count)
    else:
        print("startedCount = False")
    app.after(ms=1000, func=_start)

def play():
    global isPaused, running, song, isActive
    if isPaused is False:
        isActive = True
        songTitle.config(font="Calibri 32")
        app.geometry("400x380")
        song = playList.get(ACTIVE)
        print(f"loading {song}")
        if len(str(song)) > 35:
            songTitle.config(font="Calibri 13")
            app.geometry("400x360")
            print("ERROR: length above limit\nALTERNATIVE: setting geometry to 400x262")
        elif len(str(song)) > 24:
            songTitle.config(font="Calibri 28")
            app.geometry("400x380")
            print("ERROR: length above limit\nALTERNATIVE: setting geometry to 400x262")
        pyg.mixer.music.load(song)
        print(f"loaded {song}")
        l.set(f"Around {convert(int(MP3(song).info.length))} minutes long.")
        var.set(str(playList.get(ACTIVE)).split(".")[0])
        pyg.mixer.music.play(0)
        print(f"playing {song}")
    elif isPaused is True:
        if playList.get(ACTIVE) != song:
            isActive = True
            songTitle.config(font="Calibri 32")
            app.geometry("400x380")
            song = playList.get(ACTIVE)
            print(f"loading {song}")
            if len(str(song)) > 35:
                songTitle.config(font="Calibri 13")
                app.geometry("400x360")
                print("ERROR: length above limit\nALTERNATIVE: setting geometry to 400x262")
            elif len(str(song)) > 24:
                songTitle.config(font="Calibri 28")
                app.geometry("400x380")
                print("ERROR: length above limit\nALTERNATIVE: setting geometry to 400x262")
            pyg.mixer.music.load(song)
            print(f"loaded {song}")
            l.set(f"Around {convert(int(MP3(song).info.length))} minutes long.")
            var.set(str(playList.get(ACTIVE)).split(".")[0])
            pyg.mixer.music.play(0)
            print(f"playing {song}")
        else:
            pyg.mixer.music.unpause()
            isPaused = False
            print("resumed")
Play = Button(app, image=photo1,command=play, border=0, borderwidth=0, width=56, height=56)
Pause = Button(app, image=photo2,command=pause, border=0, borderwidth=0, width=56, height=56)
var = StringVar()
l = StringVar()
songTitle = Label(app, font="Calibri 32", textvariable=var, bg="black", fg="white", border=0, borderwidth=0)
songLength = Label(app, font="Calibri 16",textvariable=l,bg="black", fg="white", border=0, borderwidth=0)
logo = Label(app, image=photo3, border=0, borderwidth=0)
logo.grid(row=0, columnspan=2)
songTitle.grid(row=2, column=0, columnspan=2)
songLength.grid(row=3, column=0, columnspan=2)
Play.grid(row=4, column=1)
Pause.grid(row=4, column=0)
playList.grid(row=1, column=0, columnspan=2)
app.mainloop()
