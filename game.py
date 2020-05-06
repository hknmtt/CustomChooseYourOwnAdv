import sys
import time
import random
import os
from importlib import import_module


def clear(): return os.system('clear')


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
        except:
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
        except:
            print(f"I don't want to or i can't drop {item}")
    elif item in inventory:
        inventory.remove(item)
        rooms[room]['objects'].append(item)
        print(f'You dropped the {item}')
    else:
        print(f"I don't want drop {item} or i don't have it")


def look(direction='around'):
    if direction in same_room_db:
        play(current_room['id'])
    elif (direction in inventory or
          direction in rooms[current_room['id']]['objects']):
        print(objects[direction]['description'])
    else:
        try:
            sprint(current_room['look_at_' + direction], current_room['spd'])
        except:
            print(f" I don't know where {direction} is")


def use(item):
    if item in inventory or item in rooms[current_room['id']]['objects']:
        try:
            sprint(rooms[current_room['id']]['use_txt_' + item])
        except:
            print("I can't use {item} here")
        try:
            command(current_room['use_' + item])
        except:
            pass

    else:
        print(f"I don't see {item} anywhere")


def go_to(arg):
    arg = ''.join(e for e in arg if e.isalnum())
    if arg in current_room['connections'] and rooms[arg]['locked']:
        try:
            print(rooms[arg]['locked_txt'])
        except:
            print('The way is blocked')
    elif arg in current_room['connections'] and not rooms[arg]['locked']:
        play(arg)
    else:
        print(f"I can't go to {arg} from here, or i don't know where it is")


def command(user_input):
    if user_input.startswith('debug'):
        debug(user_input)
    elif user_input.startswith(tuple(custom_commands)):
        command(current_room['custom_' + user_input])
    else:
        # checa se o usuario digitou o comando ir(qualquer variaçao)
        if user_input.startswith(ir_db):
            go_to(remove_prefix(user_input, ir_db))

        # checa se o usuario digitou o comando pegar
        elif user_input.startswith(pegar_db):
            take_object(current_room['id'],
                        remove_prefix(user_input, pegar_db))

        # checa se o usuario digitou o comando dropar
        elif user_input.startswith(largar_db):
            drop_item(current_room['id'],
                      remove_prefix(user_input, largar_db))

        elif (user_input.startswith('inventario') or
              user_input.startswith('inv')):
            print("Inventário: " + ', '.join(inventory))

        elif user_input.startswith(olhar_db):
            look(remove_prefix(user_input, olhar_db))

        elif user_input.startswith(usar_db):
            use(remove_prefix(user_input, usar_db))

        else:
            print('Não entendi o que você quis dizer')


def debug(command):
    if command.startswith('debug_spawn '):
        rooms[current_room['id']]['objects'].append(command[12:])

    elif command.startswith('debug_destroy '):
        try:
            rooms[current_room['id']]['objects'].remove(command[14:])
        except:
            print('debug no such object in room')
        else:
            print(f'{command[14:]} pulverized')
    elif command.startswith('debug_add_item '):
        inventory.append(command[15:])

    elif command.startswith('debug_remove_item '):
        try:
            inventory.remove(command[18:])
        except:
            print('debug no such object in inv')
        else:
            print(f'{command[18:]} incinerated')

    elif command.startswith('debug_change_state '):
        rooms[current_room['id']]['txt'] = current_room[command[19:]]
        play(current_room['id'])

    elif command.startswith('debug_tp '):
        play(rooms[command[9:]]['id'])

    elif command.startswith('debug_unlock '):
        rooms[command[13:]]['locked'] = False

    elif command.startswith('debug_lock '):
        rooms[command[11:]]['locked'] = True


def play(room='inicial'):
    clear()
    global current_room
    current_room = rooms[room]
    global custom_commands
    custom_commands = [x.replace('custom_', '')
                       for x in current_room.keys() if x.startswith('custom_')]

    # printa o texto da sala
    sprint(current_room['txt'], current_room['spd'])
    try:
        sprint('\n'.join([objects[x]['txt_in_room']
                          for x in current_room['objects']]),
               current_room['spd'])  # printa texto de objetos na sala
    except:
        # debug pra quando nao tem nada
        print('Object without description in ground')
    if not current_room['objects']:
        print('nada1')
    # loop comandos
    while True:
        user_input = input(current_room['choicetxt'])
        user_input = user_input.lower()  # formatação do input do usuario

        command(user_input)


ir_db = ('ir ', 'ir para', 'go ', 'go to', 'ir pra', 'goto')
pegar_db = ('pegar ', 'take ', 'tomar ', 'get ')
largar_db = ('largar ', 'dropar ', 'drop ', 'place ', 'colocar')
same_room_db = ('em volta', 'around', 'aqui')
olhar_db = ('ver ', 'olhar ', 'olhar para ', 'olhar pra ', 'espiar ',
            'verificar ', 'observar ', 'inspecionar ', 'analisar ',
            'look ', 'look at', 'inspect ', 'examine ', 'observe ')
usar_db = ('usar ', 'use ', 'utilizar ', 'utilize ')

# importa o jogo informado no menu
file = import_module('games.jogo1')
# importa o dict do jogo
rooms = getattr(file, 'rooms')
objects = getattr(file, 'objects')
inventory = getattr(file, 'starterinv')
# executa sala inicial
play()
