import sys,time,random,os
from importlib import import_module
clear = lambda: os.system('clear')

def sprint(text, typing_speed = 0):
    typing_speed = int(typing_speed)
    # Caso tempo for 0 ou não especificado, apenas printa de forma normal
    if typing_speed == 0:
        print(text)
    #Se nao, printa o texto de uma forma que um humano escreveria de acordo com a velocidade informada
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
    if item in rooms[room]['objects'] and objects[item]['portable']:
        inventory.append(item)
        rooms[room]['objects'].remove(item)
        print(objects[item]['take_txt'])

    elif item in rooms[room]['objects'] and not objects[item]['portable']:
        try:
            print(objects[item]['take_fail_txt'])
        except:
            print("I can't take that object")
    else:
        print(f"I don't see {item} anywhere here")

def drop_item(room, item):
    if item in inventory:
        inventory.remove(item)
        rooms[room]['objects'].append(item)
        print('You dropped the item')
    else:
        k = 1/0

def go_to(arg):
    arg = ''.join(e for e in arg if e.isalnum())
    if arg in current_room['connections']:
        play(arg)
    else:
        k = 1/0

def command(user_input):
    if user_input.startswith('debug'):
        debug_commands(user_input)
    else:
        if user_input.startswith(ir_db): #checa se o usuario digitou o comando ir(qualquer variaçao)
            try:
                go_to(remove_prefix(user_input.lower(), ir_db))
            except ZeroDivisionError:
                print('Não consigo ir pra lá!')

        elif user_input.startswith(pegar_db): #checa se o usuario digitou o comando pegar
            take_object(current_room['id'], remove_prefix(user_input.lower(), pegar_db))

        elif user_input.startswith(largar_db): #checa se o usuario digitou o comando dropar
            try:
                drop_item(current_room['id'], remove_prefix(user_input.lower(), largar_db))
            except ZeroDivisionError:
                print('\nNão consigo largar esse objeto ou não possuo ele')

        elif user_input.startswith('inventario') or user_input.startswith('inv'):
            print("Inventário: " + ','.join(inventory))

        else:
            print('\n Não entendi')

def debug(command):
    return True

def play(room = 'inicial'):
    clear()
    global current_room
    current_room = rooms[room]

    #printa o texto da sala
    sprint(current_room['txt'], current_room['spd'])
    try:
        sprint(''.join([objects[x]['txt_in_room'] for x in current_room['objects']]), current_room['spd']) #printa texto de objetos na sala
    except:
        print('nada') #debug pra quando nao tem nada

    #loop comandos
    while True:
        user_input = input(current_room['choicetxt'])
        user_input = user_input.lower() # formatação do input do usuario

        command(user_input)



ir_db = ('ir ', 'ir para', 'go ', 'go to', 'ir pra', 'goto')
pegar_db = ('pegar ', 'take ', 'tomar ', 'get ')
largar_db = ('largar ', 'dropar ', 'drop ', 'place ', 'colocar')

#importa o jogo informado no menu
file = import_module('games.jogo1')
#importa o dict do jogo
rooms = getattr(file, 'rooms')
objects = getattr(file, 'objects')
inventory = getattr(file, 'starterinv')
#executa sala inicial
play()
