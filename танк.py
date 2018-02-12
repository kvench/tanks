from random import choice
from tkinter import Tk, Canvas, mainloop, NW
from PIL import Image, ImageTk

# размер карты в пикселях
window_width = 600
window_height = 600

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

# создаем холст
tk = Tk()
c = Canvas(tk, width=window_width, height=window_height, bg='white')
c.pack()

# картинки со стеной и травой
brick = ImageTk.PhotoImage((Image.open("brick.jpg").resize((block_width, block_height))))
grass = ImageTk.PhotoImage((Image.open("grass.jpg").resize((block_width, block_height))))

# рисуем карту
for i in range(12):
    for j in range(12):
        if game_map[i][j] == 0:
            c.create_image(i * block_width, j * block_height, image=grass, anchor=NW)
        if game_map[i][j] == 1:
            c.create_image(i * block_width, j * block_height, image=brick, anchor=NW)

# картинка с игроком
player_image_up = ImageTk.PhotoImage((Image.open("tank.gif").resize((block_width, block_height))))
player_image_right = ImageTk.PhotoImage((Image.open("tank.gif").resize((block_width, block_height))).rotate(270))
player_image_down = ImageTk.PhotoImage((Image.open("tank.gif").resize((block_width, block_height))).rotate(180))
player_image_left = ImageTk.PhotoImage((Image.open("tank.gif").resize((block_width, block_height))).rotate(90))
bullet_image_up = ImageTk.PhotoImage(
    (Image.open("bullet.png").convert('RGBA').resize((block_width, block_height))).rotate(90))
bullet_image_right = ImageTk.PhotoImage((Image.open("bullet.png").convert('RGBA').resize((block_width, block_height))))
bullet_image_down = ImageTk.PhotoImage(
    (Image.open("bullet.png").convert('RGBA').resize((block_width, block_height))).rotate(270))
bullet_image_left = ImageTk.PhotoImage(
    (Image.open("bullet.png").convert('RGBA').resize((block_width, block_height))).rotate(180))
# координаты игрока
x = 6
y = 6
# создаем игрока
player_up = c.create_image(x * block_width, y * block_height, image=player_image_up, anchor=NW)
player_right = c.create_image(x * block_width, y * block_height, image=player_image_right, anchor=NW)
player_down = c.create_image(x * block_width, y * block_height, image=player_image_down, anchor=NW)
player_left = c.create_image(x * block_width, y * block_height, image=player_image_left, anchor=NW)

c.itemconfigure(player_left, state='hidden')
c.itemconfigure(player_up, state='hidden')
c.itemconfigure(player_down, state='hidden')
c.itemconfigure(player_right, state='hidden')
c.itemconfigure(choice([player_up, player_down, player_left, player_right]), state='normal')

bullets = []


# проверка доступности клетки
def is_available(i, j):
    if i < 0 or i >= 12 or j < 0 or j >= 12:
        return False
    if game_map[i][j] == 1:
        return False
    return True


def moveBullets():
    for bullet in bullets:
        c.move(bullet, 10, 0)
    c.after(moveBullets)


# нажатие клавиши
def keyDown(key):
    global x, y, player_up, player_down, player_left, player_right, bullet_up, bullet_down, bullet_right, bullet_left
    if key.char == 'a':
        c.itemconfigure(player_left, state='normal')
        c.itemconfigure(player_up, state='hidden')
        c.itemconfigure(player_down, state='hidden')
        c.itemconfigure(player_right, state='hidden')

        if is_available(x - 1, y):
            x -= 1

    if key.char == 'd':
        c.itemconfigure(player_left, state='hidden')
        c.itemconfigure(player_up, state='hidden')
        c.itemconfigure(player_down, state='hidden')
        c.itemconfigure(player_right, state='normal')

        if is_available(x + 1, y):
            x += 1
    if key.char == 'w':
        c.itemconfigure(player_left, state='hidden')
        c.itemconfigure(player_up, state='normal')
        c.itemconfigure(player_down, state='hidden')
        c.itemconfigure(player_right, state='hidden')

        if is_available(x, y - 1):
            y -= 1
    if key.char == 's':
        c.itemconfigure(player_left, state='hidden')
        c.itemconfigure(player_up, state='hidden')
        c.itemconfigure(player_down, state='normal')
        c.itemconfigure(player_right, state='hidden')

        if is_available(x, y + 1):
            y += 1
    if key.char == ' ':
        bullets.append(c.create_image(x * block_width, y * block_height, image=bullet_image_left, anchor=NW))

    c.coords(player_up, x * block_width, y * block_height)
    c.coords(player_down, x * block_width, y * block_height)
    c.coords(player_left, x * block_width, y * block_height)
    c.coords(player_right, x * block_width, y * block_height)


# при нажатии любой клавишы вызываем keyDown

tk.bind("<KeyPress>", keyDown)
c.after(50, moveBullets)
mainloop()