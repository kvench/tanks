import json, time, random, select, socket, sys, queue
from threading import Thread
# размеры поля у клиента
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

# список пуль
bullets = []

# список танков
tanks = []

# ищем пустую клетку
def get_empty_place():
    while True:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        if is_available(x, y):
            return x, y

# узнаем позицию клетки с объектом
def coords(object):
    x, y = object['x'], object['y']
    return (int(x // block_width), int(y // block_height))

# поворот объекта
def rotate(object, direction):
    object['direction'] = direction
# передвижение объекта
def move(object, dx, dy):
    object['x'] += dx
    object['y'] += dy

# удаление объекта
def delete(object):
    if object in tanks:
        tanks.remove(object)
    if object in bullets:
        bullets.remove(object)

# создает танк в заданной точке
def get_tank(x, y, direction):
    tank = {
        "direction": direction,
        "x": x,
        "y": y,
        "life": 5
    }
    return tank

# выпускает пулю из указанной клетки в заданном направлении
def get_bullet(x, y, direction):
    if direction == 'left':
        rx = block_width * x - 10
        ry = block_height * y + block_height // 2
    elif direction == 'right':
        rx = block_width * (x + 1) + 10
        ry = block_height * y + block_height // 2
    elif direction == 'up':
        rx = block_width * x + block_width // 2
        ry = block_height * y - 10
    else:
        rx = block_width * x + block_width // 2
        ry = block_height * (y + 1) + 10

    bullet = {
        "direction": direction,
        "x": rx,
        "y": ry
    }
    return bullet

# проверяем, пересекается ли танк и пуля
def is_collided(tank, bullet):
    # TODO: вернуть true, если танк и пуля пересекается
    pass

# проверяем, свободна ли клетка
def is_available(i, j):
    if i < 0 or i >= 12 or j < 0 or j >= 12:
        return False
    if game_map[i][j] == 1:
        return False
    for tank in tanks:
        x, y = tank['x'], tank['y']
        if x == i and y == j:
            return False
    return True

# игровой цикл
def loop():
    while True:
        for bullet in bullets:
            x, y = coords(bullet)

            for tank in tanks:
                # TODO: если танк пересекается с пулей, уменьшить жизнь
                # TODO: если жизнь закончилась - удалить танк
                pass

            # TODO: если пуля врезалась в стену - удалить пулю
            # TODO: иначе - передвинуть пулю в нужном направлении

        time.sleep(0.05)

# обработка команды от танка
def process_command(tank, command):
    # TODO: обработать команду от игрока, варианты: go_right, go_left, go_up, go_down, fire_right, fire_left, fire_down, fire_up
    pass

# безопасное закрытие соединения
def safe_close(connection):
    if connection in inputs:
        inputs.remove(connection)
    if connection in outputs:
        outputs.remove(connection)
    try:
        del tank_connections[connection]
    except:
        pass
    try:
        s.close()
    except:
        pass

server = socket.socket()
server.setblocking(0)
server.bind(('localhost', 8082))
server.listen(5)

inputs = [server]
outputs = []
tank_connections = {}

# запускаем цикл передвижения в отдельном потоке
thread = Thread(target=loop)
thread.start()

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is server:
            # когда к нам поключаются:
            connection, client_address = s.accept()
            print("New connection from ", client_address)
            inputs.append(connection)

            # найти свободную клетку и поставить туда танк
            x, y = get_empty_place()
            new_tank = get_tank(x, y, 'up')
            tanks.append(new_tank)

            # запоминаем, что этому подключению соответствует этот танк
            tank_connections[connection] = new_tank
        else:
            try:
                data = s.recv(1024)
                if data:
                    command = data.decode('utf-8')
                    print("Received new command:", command)
                    tank = tank_connections[connection]

                    # если запросили карту - добавить в получатели
                    if command == 'map':
                        outputs.append(s)
                    # иначе - обрабатываем клавиатурную команду
                    else:
                        process_command(tank, command)

                else:
                    safe_close(s)
            except:
                safe_close(s)

    for s in writable:
        try:
            tank = tank_connections[connection]

            # если танк умер - закрываем соединение
            if tank not in tanks:
                s.close()

            # собираем в одну кучу состояние игры
            game_state = {
                "me": tank,
                "tanks": tanks,
                "bullets": bullets
            }

            # сериализуем
            response = json.dumps(game_state)
            # отправляем
            s.send(response.encode('utf-8'))
            # после отправки - врменно удаляем из получателей
            outputs.remove(s)
        except:
            safe_close(s)

    for s in exceptional:
        safe_close(s)
