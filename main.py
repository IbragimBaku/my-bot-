import discord
import random
import time
import asyncio

# Инициализация клиента Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Игровые параметры
WIDTH = 10
HEIGHT = 5
trash_count = 5
score = 0
player_symbol = 'P'  # Символ для игрока (женский по умолчанию)
player_x = 0
player_y = 0

# Игровое поле
field = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Мусор на поле
for _ in range(trash_count):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    field[y][x] = 'X'

# Функция для отображения поля
def display_field():
    global field, score
    field_display = ""
    for row in field:
        field_display += ' '.join(row) + '\n'
    return field_display + f"Очки: {score}"

# Функция для перемещения игрока
def move_player(direction):
    global player_x, player_y, score
    field[player_y][player_x] = ' '  # Очищаем текущее место игрока

    if direction == "w" and player_y > 0:  # Вверх
        player_y -= 1
    elif direction == "s" and player_y < HEIGHT - 1:  # Вниз
        player_y += 1
    elif direction == "a" and player_x > 0:  # Влево
        player_x -= 1
    elif direction == "d" and player_x < WIDTH - 1:  # Вправо
        player_x += 1

    # Проверка, если игрок оказался на мусоре
    if field[player_y][player_x] == 'X':  # Мусор
        score += 1
        field[player_y][player_x] = 'O'  # Убираем мусор
        return "Вы убрали мусор!"
    
    field[player_y][player_x] = player_symbol  # Устанавливаем игрока на новое место
    return "Вы переместились."

# Событие при запуске бота
@client.event
async def on_ready():
    print(f'Мы вошли как {client.user}')

# Событие при получении сообщения
@client.event
async def on_message(message):
    global score, player_x, player_y, player_symbol, field, trash_count

    # Игнорируем сообщения от самого себя
    if message.author == client.user:
        return

    # Если сообщение - это команда для начала игры
    if message.content.lower() == "!start":
        await message.channel.send("Добро пожаловать в игру уборки мусора!\nВыберите ваш пол (Ж/М):")
        
        # Ожидаем ответа
        def check(msg):
            return msg.author == message.author

        try:
            response = await client.wait_for("message", check=check, timeout=30)
            if response.content == "Ж":
                player_symbol = 'G'
                await message.channel.send("Вы выбрали пол женский")
            elif response.content == "М":
                player_symbol = 'B'
                await message.channel.send("Вы выбрали пол мужской")
            else:
                await message.channel.send("Неверный выбор, используем символ по умолчанию.")
                player_symbol = 'P'

            # Инициализируем начальные координаты и поле
            player_x = 0
            player_y = 0
            score = 0
            field = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

            # Мусор на поле
            for _ in range(trash_count):
                x = random.randint(0, WIDTH - 1)
                y = random.randint(0, HEIGHT - 1)
                field[y][x] = 'X'

            await message.channel.send("Игра началась! Для управления используйте команды: w - вверх, a - влево, s - вниз, d - вправо.\nЦель игры: собрать весь мусор.")
            await message.channel.send(display_field())

        except asyncio.TimeoutError:
            await message.channel.send("Время выбора пола истекло. Игра не началась.")

    # Если сообщение - это команда для перемещения
    elif message.content.lower() in ['w', 'a', 's', 'd']:
        result = move_player(message.content.lower())
        await message.channel.send(display_field())
        await message.channel.send(result)

        if score == trash_count:
            await message.channel.send("Поздравляем! Вы убрали весь мусор!")
            # Закрываем игру
            return

# Запуск бота
client.run('MTMyMjMyMjE5OTE4NDY3NDkyNg.GUUcUL.pgBk-9hSX9hC3lRkzX41IRwJw241G4q3FtzEpc')
