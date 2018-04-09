import json
from tkinter import Tk, Canvas, mainloop, NW

import time
from PIL import Image, ImageTk
import socket

# размер карты в пикселях
window_width = 600
window_height = 600

# создаем холст
tk = Tk()
c = Canvas(tk, width=window_width, height=window_height, bg='white')
c.pack()
# карта
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# размеры блока
block_width = window_width // 12
block_height = window_height // 12

bullets = []
tanks = []

images = {
    "brick": ImageTk.PhotoImage(Image.open("brick.jpg").resize((block_width, block_height))),
    "grass": ImageTk.PhotoImage(Image.open("grass.jpg").resize((block_width, block_height))),
    "bullet_up": ImageTk.PhotoImage((Image.open("bullet.gif").convert('RGBA').resize((10, 30)))),
    "bullet_down": ImageTk.PhotoImage((Image.open("bullet.gif").convert('RGBA').resize((10, 30)).rotate(180))),
    "bullet_left": ImageTk.PhotoImage((Image.open("bullet.gif").convert('RGBA').resize((10, 30)).rotate(90))),
    "bullet_right": ImageTk.PhotoImage((Image.open("bullet.gif").convert('RGBA').resize((10, 30)).rotate(270))),
    "tank_up": ImageTk.PhotoImage((Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)))),
    "tank_down": ImageTk.PhotoImage(
        (Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)).rotate(180))),
    "tank_left": ImageTk.PhotoImage(
        (Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)).rotate(90))),
    "tank_right": ImageTk.PhotoImage(
        (Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)).rotate(270)))
}

# рисуем карту
for i in range(12):
    for j in range(12):
        if game_map[i][j] == 0:
            c.create_image(i * block_width, j * block_height, image=images['grass'], anchor=NW)
        if game_map[i][j] == 1:
            c.create_image(i * block_width, j * block_height, image=images['brick'], anchor=NW)

def rotate(object, direction):
    # TODO: поворот объекта
    for d in ['up', 'down', 'left', 'right']:
        c.itemconfigure(object[d], state='hidden')
    c.itemconfigure(object[direction], state='normal')
    object['direction'] = direction
    pass

def delete(object):
    # TODO: удаление объекта
    c.delete(object['up'])
    c.delete(object['down'])
    c.delete(object['left'])
    c.delete(object['right'])
    pass

# создаем танк в заданной клетке
def get_tank(x, y, direction):
    tank = {
        "direction": direction,
        "up": c.create_image(x * block_width, y * block_height, image=images['tank_up'], anchor=NW, state='normal'),
        "down": c.create_image(x * block_width, y * block_height, image=images['tank_down'], anchor=NW, state='hidden'),
        "left": c.create_image(x * block_width, y * block_height, image=images['tank_left'], anchor=NW, state='hidden'),
        "right": c.create_image(x * block_width, y * block_height, image=images['tank_right'], anchor=NW, state='hidden')
    }
    rotate(tank, direction)
    return tank

# создаем пулю в заданной точке, которая летит в заданном направлении
def get_bullet(rx, ry, direction):
    bullet = {
        "direction": 'up',
        "up": c.create_image(rx, ry, image=images['bullet_up'], state='normal'),
        "down": c.create_image(rx, ry, image=images['bullet_down'],
                               state='hidden'),
        "left": c.create_image(rx, ry, image=images['bullet_left'],
                               state='hidden'),
        "right": c.create_image(rx, ry, image=images['bullet_right'],
                                state='hidden')
    }
    rotate(bullet, direction)
    return bullet

def loop():
    try:
        # TODO: удалить все танки и пули
        for tank in tanks[:]:
            delete(tank)
            tanks.remove(tank)
        for bullet in bullets[:]:
            delete(bullet)
            bullet.remove(bullet)
        # TODO: отправить команду map
        s.send("map".encode('utf-8'))
        # TODO: подождать
        time.sleep(0.025)
        # TODO: получить ответ
        a = s.recv(10000)
        # TODO: десериализовать ответ
        result_string = a.decode('utf-8')
        # десериализация
        game_state = json.loads(result_string)

        # TODO: разместить на карте пули и танки из ответа
        for tank_record in game_state["tanks"]:
            get_tank(tank_record['x'],tank_record["y"], tank_record["direction"] )
        for bullet_record in game_state["bullet"]:
            get_bullet(bullet_record["rx"],bullet_record["ry"],bullet_record['direction'])

        c.after(10, loop)

    except Exception as e:
        # если возникла ошибка - закрыть окно
        print(e)
        try:
            s.close()
        except:
            pass
        tk.destroy()

# обработка нажатия клавиши
def keyDown(key):
    try:
        

        # в зависимости от нажатой клавиши, отправить команду на сервер
        pass
    except:
        try:
            s.close()
        except:
            pass
        tk.destroy()

try:
    # подключаемся к серверу
    s = socket.socket()
    s.connect(('localhost', 8082))
    print('connected')
    c.after(10, loop)

    # при нажатии любой клавишы вызываем keyDown
    tk.bind("<KeyPress>", keyDown)
    mainloop()
except:
    tk.destroy()
