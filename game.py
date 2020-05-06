import sys
import time
import random
import os
from importlib import import_module


def clear():
    return os.system('clear')


def sprint(text, typing_speed=0):
    typing_speed = int(typing_speed)
    # Caso tempo for 0 ou não especificado, apenas printa de forma normal
    if typing_speed == 0:
        print(text)
    # Se nao, printa o texto de uma forma que um humano escreveria de acordo
    # com a velocidade informada
    else:
        for letter in text:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(random.random()*10.0/typing_speed)
        print('')


def remove_prefix(text, command):
    for word in command[:]:
        if text.startswith(word):
            new_text = text[len(word):]
    return new_text


def change_room_state(room, state):
    rooms[room]['txt'] = rooms[room][state]


def take_object(room, item):
    if item in rooms[room]['objects'] and not objects[item]['portable']:
        try:
            print(objects[item]['take_fail_txt'])
        except KeyError:
            print("I can't take that object")
    elif item in rooms[room]['objects']:
        inventory.append(item)
        rooms[room]['objects'].remove(item)
        print(objects[item]['take_txt'])
    else:
        print(f"I don't see {item} anywhere here")


def drop_item(room, item):
    if item in inventory and not objects[item]['portable']:
        try:
            print(objects[item]['drop_fail_txt'])
        except KeyError:
            print(f"I don't want to or i can't drop {item}")
    elif item in inventory:
        inventory.remove(item)
        rooms[room]['objects'].append(item)
        print(f'You dropped the {item}')
    else:
        print(f"I don't want drop {item} or i don't have it")


def look(direction='around'):
    if direction in SAME_ROOM_DB:
        play(CURRENT_ROOM['id'])
    elif (direction in inventory or
          direction in rooms[CURRENT_ROOM['id']]['objects']):
        print(objects[direction]['description'])
    else:
        try:
            sprint(CURRENT_ROOM['look_at_' + direction], CURRENT_ROOM['spd'])
        except KeyError:
            print(f" I don't know where {direction} is")


def use(item):
    if item in inventory or item in rooms[CURRENT_ROOM['id']]['objects']:
        try:
            sprint(rooms[CURRENT_ROOM['id']]['use_txt_' + item])
        except KeyError:
            print("I can't use {item} here")
        try:
            command(CURRENT_ROOM['use_' + item])
        except KeyError:
            pass

    else:
        print(f"I don't see {item} anywhere")


def go_to(arg):
    arg = ''.join(e for e in arg if e.isalnum())
    if arg in CURRENT_ROOM['connections'] and rooms[arg]['locked']:
        try:
            print(rooms[arg]['locked_txt'])
        except KeyError:
            print('The way is blocked')
    elif arg in CURRENT_ROOM['connections'] and not rooms[arg]['locked']:
        play(arg)
    else:
        print(f"I can't go to {arg} from here, or i don't know where it is")


def comando(user_input):
    if user_input.startswith('debug'):
        debug(user_input)
    elif user_input.startswith(tuple(CUSTOM_COMMANDS)):
        comando(CURRENT_ROOM['custom_' + user_input])
    else:
        # checa se o usuario digitou o comando ir(qualquer variaçao)
        if user_input.startswith(IR_DB):
            go_to(remove_prefix(user_input, IR_DB))

        # checa se o usuario digitou o comando pegar
        elif user_input.startswith(PEGAR_DB):
            take_object(CURRENT_ROOM['id'],
                        remove_prefix(user_input, PEGAR_DB))

        # checa se o usuario digitou o comando dropar
        elif user_input.startswith(LARGAR_DB):
            drop_item(CURRENT_ROOM['id'],
                      remove_prefix(user_input, LARGAR_DB))

        elif (user_input.startswith('inventario') or
              user_input.startswith('inv')):
            print("Inventário: " + ', '.join(inventory))

        elif user_input.startswith(OLHAR_DB):
            look(remove_prefix(user_input, OLHAR_DB))

        elif user_input.startswith(USAR_DB):
            use(remove_prefix(user_input, USAR_DB))

        else:
            print('Não entendi o que você quis dizer')


def debug(user_input):
    if user_input.startswith('debug_spawn '):
        rooms[CURRENT_ROOM['id']]['objects'].append(user_input[12:])

    elif user_input.startswith('debug_destroy '):
        try:
            rooms[CURRENT_ROOM['id']]['objects'].remove(user_input[14:])
        except KeyError:
            print('debug no such object in room')
        else:
            print(f'{user_input[14:]} pulverized')
    elif user_input.startswith('debug_add_item '):
        inventory.append(user_input[15:])

    elif user_input.startswith('debug_remove_item '):
        try:
            inventory.remove(user_input[18:])
        except KeyError:
            print('debug no such object in inv')
        else:
            print(f'{user_input[18:]} incinerated')

    elif user_input.startswith('debug_change_state '):
        rooms[CURRENT_ROOM['id']]['txt'] = CURRENT_ROOM[user_input[19:]]
        play(CURRENT_ROOM['id'])

    elif user_input.startswith('debug_tp '):
        play(rooms[user_input[9:]]['id'])

    elif user_input.startswith('debug_unlock '):
        rooms[user_input[13:]]['locked'] = False

    elif user_input.startswith('debug_lock '):
        rooms[user_input[11:]]['locked'] = True


def play(room='inicial'):
    clear()
    global CURRENT_ROOM
    CURRENT_ROOM = rooms[room]
    global CUSTOM_COMMANDS
    CUSTOM_COMMANDS = [x.replace('custom_', '')
                       for x in CURRENT_ROOM.keys() if x.startswith('custom_')]

    # printa o texto da sala
    sprint(CURRENT_ROOM['txt'], CURRENT_ROOM['spd'])
    try:
        sprint('\n'.join([objects[x]['txt_in_room']
                          for x in CURRENT_ROOM['objects']]),
               CURRENT_ROOM['spd'])  # printa texto de objetos na sala
    except KeyError:
        # debug pra quando nao tem nada
        print('Object without description in ground')
    if not CURRENT_ROOM['objects']:
        print('nada1')
    # loop comandos
    while True:
        user_input = input(CURRENT_ROOM['choicetxt'])
        user_input = user_input.lower()  # formatação do input do usuario

        comando(user_input)


IR_DB = ('ir ', 'ir para', 'go ', 'go to', 'ir pra', 'goto')
PEGAR_DB = ('pegar ', 'take ', 'tomar ', 'get ')
LARGAR_DB = ('largar ', 'dropar ', 'drop ', 'place ', 'colocar')
SAME_ROOM_DB = ('em volta', 'around', 'aqui')
OLHAR_DB = ('ver ', 'olhar ', 'olhar para ', 'olhar pra ', 'espiar ',
            'verificar ', 'observar ', 'inspecionar ', 'analisar ',
            'look ', 'look at', 'inspect ', 'examine ', 'observe ')
USAR_DB = ('usar ', 'use ', 'utilizar ', 'utilize ')

# importa o jogo informado no menu
file = import_module('games.jogo1')
# importa o dict do jogo
rooms = getattr(file, 'rooms')
objects = getattr(file, 'objects')
inventory = getattr(file, 'starterinv')
# executa sala inicial
CURRENT_ROOM = 'inicial'
play(CURRENT_ROOM)
