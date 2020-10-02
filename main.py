from tkinter import *
import pygame
from tkinter import filedialog
import tkinter.ttk as ttk
import time
from mutagen.mp3 import MP3

root = Tk()
root.title('Mp3 Player')
root.iconbitmap('C:/Users/Иван/Desktop/gui/mp3player.ico')
root.geometry('600x500')

pygame.mixer.init()


# Получить информацию о длительности песни
def duration():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    #slider_label.config(text=f'Слайдер:{int(slider.get())} и позиция песни: {int(current_time) }')
    converted_time = time.strftime('%M:%S', time.gmtime(current_time))


    # current_song = song_list.curselection()
    song = song_list.get(ACTIVE)
    song = f'C:/Users/Иван/Desktop/music/{song}.mp3'
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_length = time.strftime('%M:%S', time.gmtime(song_length))
    current_time += 1

    if int(slider.get()) == int(song_length):
        status_bar.config(text=f'Прошло времени: {converted_length}/{converted_length}')
    elif paused:
        pass
    elif int(slider.get()) == int(current_time):
        slider_pos = int(song_length)
        slider.config(to=slider_pos, value=int(current_time))
    else:
        slider_pos = int(song_length)
        slider.config(to=slider_pos, value=int(slider.get()))
        converted_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
        status_bar.config(text=f'прошло времени: {converted_time}/{converted_length}')
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)
    #status_bar.config(text=f'Прошло времени: {converted_time}/{converted_length} ')
    #slider.config(value=int(current_time))



    status_bar.after(1000, duration)


# Функция добавления песни
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/Иван/Desktop/music/', title='Выберите песню', filetypes=(('mp3 Files', '*.mp3'),))
    song = song.replace('C:/Users/Иван/Desktop/music/', '')
    song = song.replace('.mp3', '')
    song_list.insert(END, song)


# Добавить несколько песен в плейлист
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/Иван/Desktop/music/', title='Выберите песню', filetypes=(('mp3 Files', '*.mp3'),))
    for song in songs:
        song = song.replace('C:/Users/Иван/Desktop/music/', '')
        song = song.replace('.mp3', '')
        song_list.insert(END, song)


# Воспроизвести выбранную песню
def play():
    global stopped
    stopped = False
    song = song_list.get(ACTIVE)
    song = f'C:/Users/Иван/Desktop/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    duration()

    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume*100)


   # slider_pos = int(song_length)
   # slider.config(to=slider_pos, value=0)


# Остановить текущую песню
global stopped
stopped = False


def stop():
    # Сбросить слайдер
    status_bar.config(text='')
    slider.config(value=0)
    # Остановить песню
    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    status_bar.config(text='')

    global stopped
    stopped = True


global paused
paused = False


# Поставить на паузу текущую песню
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


# Включить следующую песню
def next_song():
    status_bar.config(text='')
    slider.config(value=0)
    next = song_list.curselection()
    next = next[0]+1
    song = song_list.get(next)
    song = f'C:/Users/Иван/Desktop/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
# Убрать активное выделение
    song_list.selection_clear(0, END)
# Включить активное выделение следующей песни
    song_list.activate(next)
    song_list.select_set(next, last=None)


def prev_song():
    status_bar.config(text='')
    slider.config(value=0)
    prev = song_list.curselection()
    prev = prev[0] - 1
    song = song_list.get(prev)
    song = f'C:/Users/Иван/Desktop/music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Убрать активное выделение
    song_list.selection_clear(0, END)
    # Включить активное выделение следующей песни
    song_list.activate(prev)
    song_list.select_set(prev, last=None)


# Удалить песню
def delete_song():
    stop()
    song_list.delete(ANCHOR)
    pygame.mixer.music.stop()


# Удалить все песни
def delete_all_songs():
    stop()
    song_list.delete(0, END)
    pygame.mixer.music.stop()


# Функция слайдера
def slide(x):
    #slider_label.config(text=f'{int(slider.get())} / {int(song_length)}')
    song = song_list.get(ACTIVE)
    song = f'C:/Users/Иван/Desktop/music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume*100)


master_frame = Frame(root)
master_frame.pack(pady=20)


# Создать плейлист
song_list = Listbox(master_frame, bg='black', fg='green', width=80, selectbackground='gray', selectforeground='black')
song_list.grid(row=0, column=0)

# Объявляем картинки кнопок управления
back_img = PhotoImage(file='C:/Users/Иван/Desktop/gui/backward.png')
forward_img = PhotoImage(file='C:/Users/Иван/Desktop/gui/forward.png')
play_img = PhotoImage(file='C:/Users/Иван/Desktop/gui/play.png')
pause_img = PhotoImage(file='C:/Users/Иван/Desktop/gui/pause.png')
stop_img = PhotoImage(file='C:/Users/Иван/Desktop/gui/stop.png')


# Создаём фрейм управления плеером
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady= 30)


# Создать фрейм для звука
volume_frame = LabelFrame(master_frame, text='Звук')
volume_frame.grid(row=0, column=1, padx=15)


# Создаём кнопки управления
back_btn = Button(controls_frame, image=back_img, borderwidth=0, command=prev_song)
forward_btn = Button(controls_frame, image=forward_img, borderwidth=0, command=next_song)
play_btn = Button(controls_frame, image=play_img, borderwidth=0, command=play)
pause_btn = Button(controls_frame, image=pause_img, borderwidth=0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image=stop_img, borderwidth=0, command=stop)

back_btn.grid(row=0,column=0)
forward_btn.grid(row=0,column=1)
play_btn.grid(row=0,column=2)
pause_btn.grid(row=0,column=3)
stop_btn.grid(row=0,column=4)


#Создать меню
my_menu = Menu(root)
root.config(menu=my_menu)

# Меню добавления песни
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Добавить песни', menu=add_song_menu)
add_song_menu.add_command(label='Добавить одну песню в плейлист', command=add_song)

# Добавить несколько песен
add_song_menu.add_command(label='Добавить несколько песен в плейлист', command=add_many_songs)

# Создать меню удаления песни
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label='Удалить песни', menu=remove_song_menu)
remove_song_menu.add_command(label='Удалить песню из плейлиста', command=delete_song)
remove_song_menu.add_command(label='Удалить все песни из плейлиста', command=delete_all_songs)


# Создадим строку статуса
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=1)


# Создать слайдер для перемотки
slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.grid(row=2, column=0, pady=10)


# Создать слайдер для звука
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

#slider_label = Label(root, text='0')
#slider_label.pack(pady=10)



root.mainloop()