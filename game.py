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

def menu():
    clear()
    sprint("\n\n        Welcome to the Custom Choose Your Own Adventure\n\n            Please type your desired game!\n        We have by default jogo1, test1, and test2\n\n", 100)
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
    #executa sala inicial
    play()

class Room:
    def __init__(self, current_room):
        self.txt = rooms[current_room]['txt']
        self.spd = rooms[current_room]['spd']
        self.choicetxt = rooms[current_room]['choicetxt']
        self.one = rooms[current_room]['1']
        self.two = rooms[current_room]['2']
        self.three = rooms[current_room]['3']
        self.four = rooms[current_room]['4']

def play(current_room = 'inicial'):
    clear()
    room = Room(current_room)
    #printa o texto da sala
    sprint(room.txt, room.spd)

    while True:
        choice = input(room.choicetxt)
        if choice in ['1','2','3','4']:
            break
        print('Invalid choice, please input a number between 1 and 4')
    if choice == '1':
        play(room.one)
    elif choice == '2':
        play(room.two)
    elif choice == '3':
        play(room.three)
    elif choice == '4':
        play(room.four)



menu()
