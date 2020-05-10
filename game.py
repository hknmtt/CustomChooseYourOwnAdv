import sys
import time
import random
import os
from importlib import import_module


def clear():
    return os.system('clear')


def sprint(text, typing_speed=0):
    """ Takes a text and and speed and prints as a human would."""
    typing_speed = int(typing_speed)
    # Caso tempo for 0 ou não especificado, apenas printa normal
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
    """ Takes an input, and a database of commands, and remove the commands."""
    for word in command[:]:
        if text.startswith(word):
            new_text = text[len(word):]
    return new_text



def print_room_txt(active_look):
    """Takes an boolean, and if True, prints roomtxt+allobjects, if false,
     roomtxt+allplaintsightobjects"""
    sprint(CURRENT_ROOM['txt'], CURRENT_ROOM['spd'])
    if active_look:
        try:
            sprint('\n'.join([objects[x]['txt_in_room']
                              for x in CURRENT_ROOM['objects']]),
                    CURRENT_ROOM['spd'])
        except KeyError:
            # debug pra quando nao tem nada
            print('Object without description in ground')
        if not CURRENT_ROOM['objects']:
            print('nada1')

    else:
        try:
            sprint('\n'.join([objects[x]['txt_in_room']
                          for x in CURRENT_ROOM['objects']
                          if objects[x]['plainsight']]),
                    CURRENT_ROOM['spd'])
        except KeyError:
         # debug pra quando nao tem nada
            print('Object without description in ground')
        if not CURRENT_ROOM['objects']:
            print('nada2')
def change_room_state(room, state):
    rooms[room]['txt'] = rooms[room][state]


def take_object(room, item):
    """ Takes a room id, and an item, and transfers item from room to inv."""
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
    """ Takes a room id, and an item, and transfers the item from inv to room."""
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
    """ Looks to either an item in inv, or a object in room"""
    if direction in SAME_ROOM_DB:
        print_room_txt(True)
    elif (direction in inventory or
          direction in rooms[CURRENT_ROOM['id']]['objects']):
        print(objects[direction]['description'])
    else:
        try:
            sprint(CURRENT_ROOM['look_at_' + direction], CURRENT_ROOM['spd'])
        except KeyError:
            print(f" I don't know where {direction} is")


def use(item):
    """ Tries to use an item from inv or room."""
    if item in inventory or item in rooms[CURRENT_ROOM['id']]['objects']:
        try:
            sprint(rooms[CURRENT_ROOM['id']]['use_txt_' + item])
        except KeyError:
            print("I can't use {item} here")
        try:
            comando(CURRENT_ROOM['use_' + item])
        except KeyError:
            pass

    else:
        print(f"I don't see {item} anywhere")


def go_to(roomid):
    """ Takes a room id and tries to go there from the current room."""
    roomid = ''.join(e for e in roomid if e.isalnum())
    try:
        if roomid in CURRENT_ROOM['connections_dict'].keys():
            roomid = CURRENT_ROOM['connections_dict'][roomid]
    except KeyError:
        pass


    if roomid in CURRENT_ROOM['connections'] and rooms[roomid]['locked']:
        try:
            print(rooms[roomid]['locked_txt'])
        except KeyError:
            print('The way is blocked')
    elif roomid in CURRENT_ROOM['connections'] and not rooms[roomid]['locked']:
        return roomid #sets current_room to roomid and replays gameloop
    else:
        print(f"I can't go to {roomid} from here, or i don't know asdasdasd it is")


def comando(user_input):
    """ Takes a string and executes it."""
    if user_input.startswith('debug'):
        return debug(user_input)
    elif user_input.startswith(tuple(CUSTOM_COMMANDS)):
        for x in CURRENT_ROOM['custom_' + user_input].split(' && '):
            y = comando(x)
        return y
    else:
        if user_input.startswith(IR_DB):
            return go_to(remove_prefix(user_input, IR_DB))

        elif user_input.startswith(PEGAR_DB):
            return take_object(CURRENT_ROOM['id'],
                               remove_prefix(user_input, PEGAR_DB))

        elif user_input.startswith(LARGAR_DB):
            return drop_item(CURRENT_ROOM['id'],
                             remove_prefix(user_input, LARGAR_DB))

        elif (user_input.startswith('inventario') or
              user_input.startswith('inv')):
            print("Inventário: " + ', '.join(inventory))

        elif user_input.startswith(OLHAR_DB):
            return look(remove_prefix(user_input, OLHAR_DB))

        elif user_input.startswith(USAR_DB):
            return use(remove_prefix(user_input, USAR_DB))

        else:
            print('Não entendi o que você quis dizer')


def debug(user_input):
    """ Equivalent to comando() but with more powerful commands."""
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
        return CURRENT_ROOM['id'] #replays same room

    elif user_input.startswith('debug_tp '):
        return rooms[user_input[9:]]['id'] #set current room to informed tp

    elif user_input.startswith('debug_unlock '):
        rooms[user_input[13:]]['locked'] = False

    elif user_input.startswith('debug_lock '):
        rooms[user_input[11:]]['locked'] = True



# Contants of equivalent commands terms
IR_DB = ('ir ', 'ir para', 'go ', 'go to', 'ir pra', 'goto')
PEGAR_DB = ('pegar ', 'take ', 'tomar ', 'get ')
LARGAR_DB = ('largar ', 'dropar ', 'drop ', 'place ', 'colocar ')
SAME_ROOM_DB = ('em volta', 'around', 'aqui')
OLHAR_DB = ('ver ', 'olhar ', 'olhar para ', 'olhar pra ', 'espiar ',
            'verificar ', 'observar ', 'inspecionar ', 'analisar ',
            'look ', 'look at', 'inspect ', 'examine ', 'observe ')
USAR_DB = ('usar ', 'use ', 'utilizar ', 'utilize ')

# importa o jogo informado no menu
file = import_module('games.jogo1')
# importa os dicts do jogo
rooms = getattr(file, 'rooms')
objects = getattr(file, 'objects')
inventory = getattr(file, 'starterinv')
# executa sala inicial
CURRENT_ROOM = rooms['inicial']

while 'Brasil' != 'Ditadura':
    clear()
    CUSTOM_COMMANDS = [x.replace('custom_', '')
                       for x in CURRENT_ROOM.keys() if x.startswith('custom_')]

    # printa o texto da sala
    print_room_txt(False)

    #checa se é uma sala de apenas texto
    if 'skip_room' in CURRENT_ROOM:
        input(CURRENT_ROOM['choicetxt'])
        CURRENT_ROOM = rooms[rooms[CURRENT_ROOM['id']]['skip_room']]
    else:
        while True:
            user_input = input(CURRENT_ROOM['choicetxt'])
            user_input = user_input.lower()  # formatação do input do usuario

            foo = comando(user_input)
            if foo != None:
                CURRENT_ROOM = rooms[foo]
                break


