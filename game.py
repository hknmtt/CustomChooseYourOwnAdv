import sys,time,random,os
from importlib import import_module
clear = lambda: os.system('clear')

class Room:
    def __init__(self, room):
        self.txt = rooms[room]['txt']
        self.spd = rooms[room]['spd']
        self.choicetxt = rooms[room]['choicetxt']
        self.connections = rooms[room]['connections']
        self.objects = rooms[room]['objects']

    def change_room_state(room, state):
        rooms[room]['txt'] = rooms[room][state]

    def take_object(room, item):
        if item in Room(room).objects:
            inventory.append(item)
            rooms[room]['objects'].remove(item)
            print(Objeto(item).take_txt)
        else:
            k = 1/0

    def drop_item(room, item):
        if item in inventory:
            inventory.remove(item)
            rooms[room]['objects'].append(item)
            print('You dropped the item')
        else:
            k = 1/0

class Objeto:
    def __init__(self, item):
        self.text_in_room = objects[item]['txt_in_room']
        self.description = objects[item]['description']
        self.take_txt = objects[item]['take_txt']


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

def menu():
    clear()
    sprint(('\n\nBem vindo ao Txtgame\n'
    'Por favor digite o jogo desejado\n'
    'Temos por padrão jogo1\n\n\n'), 0)
    le_game = input('Enter desired game: ')
    #ajusta o nome do jogo para pasta
    le_game = "games." + le_game
    start(le_game)

def start(jogo):
    clear()
    #importa o jogo informado no menu
    file = import_module(jogo)
    #importa o dict do jogo
    global rooms
    rooms = getattr(file, 'rooms')
    global objects
    objects = getattr(file, 'objects')
    global inventory
    inventory = getattr(file, 'starterinv')
    #executa sala inicial
    play()

def play(room = 'inicial'):
    clear()
    global current_room
    current_room = Room(room)
    #printa o texto da sala
    sprint(current_room.txt, current_room.spd)
    try:
        sprint(''.join([objects[x]['txt_in_room'] for x in current_room.objects]), current_room.spd) #printa texto de objetos na sala
    except:
        print('nada') #debug pra quando nao tem nada


    #loop comandos
    while True:
        user_input = input(current_room.choicetxt)
        user_input = user_input.lower() # formatação do input do usuario

        if user_input.startswith(ir_db): #checa se o usuario digitou o comando ir(qualquer variaçao)
            try:
                go_to(remove_prefix(user_input.lower(), ir_db))
            except:
                print('Não consigo ir pra lá!')

        elif user_input.startswith(pegar_db): #checa se o usuario digitou o comando pegar
            try:
                Room.take_object(room, remove_prefix(user_input.lower(), pegar_db))
            except:
                print('\nNão consigo encontrar esse objeto')

        elif user_input.startswith(largar_db): #checa se o usuario digitou o comando dropar
            try:
                Room.drop_item(room, remove_prefix(user_input.lower(), largar_db))
            except:
                print('\nNão consigo largar esse objeto ou não possuo ele')

        elif user_input.startswith('inventario') or user_input.startswith('inv'):
            print(inventory)

        elif user_input.startswith('debug_state '): # comando debug para forçar mudança de estado da sala
            Room.change_room_state(room, int(user_input[12]))
            play(current_room)

        elif user_input.startswith('debug_goto '): #comando debug para ir para sala mesmo sem conexão
            play(user_input[11:])


        else:
            print('Comando não reconhecido')

def go_to(user_input):
    user_input = ''.join(e for e in user_input if e.isalnum())
    if user_input in current_room.connections:
        play(user_input)
    else:
        k = 1/0

ir_db = ('ir ', 'ir para', 'go ', 'go to', 'ir pra', 'goto')
pegar_db = ('pegar ', 'take ', 'tomar ', 'get ')
largar_db = ('largar ', 'dropar ', 'drop ', 'place ', 'colocar ')

menu()
