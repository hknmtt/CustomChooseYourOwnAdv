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

def look(direction = 'around'):
    if direction in same_room_db:
        play(current_room['id'])
    else:
        try:
            sprint(current_room['look_at_'+ direction], current_room['spd'])
        except:
            print(f" I don't know where {direction} is")

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
        debug_commands(user_input)
    else:
        if user_input.startswith(ir_db): #checa se o usuario digitou o comando ir(qualquer variaçao)
            go_to(remove_prefix(user_input.lower(), ir_db))

        elif user_input.startswith(pegar_db): #checa se o usuario digitou o comando pegar
            take_object(current_room['id'], remove_prefix(user_input.lower(), pegar_db))

        elif user_input.startswith(largar_db): #checa se o usuario digitou o comando dropar
            drop_item(current_room['id'], remove_prefix(user_input.lower(), largar_db))

        elif user_input.startswith('inventario') or user_input.startswith('inv'):
            print("Inventário: " + ','.join(inventory))

        elif user_input.startswith(olhar_db):
            look(remove_prefix(user_input.lower(), olhar_db))

        else:
            print('\nNão entendi o que você quis dizer')

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
same_room_db =('em volta', 'around', 'aqui')
olhar_db = ('ver ', 'olhar ', 'olhar para ', 'olhar pra ', 'espiar ', 'verificar ', 'observar ')

#importa o jogo informado no menu
file = import_module('games.jogo1')
#importa o dict do jogo
rooms = getattr(file, 'rooms')
objects = getattr(file, 'objects')
inventory = getattr(file, 'starterinv')
#executa sala inicial
play()
