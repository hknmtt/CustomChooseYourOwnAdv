import sys,time,random,os
from importlib import import_module
clear = lambda: os.system('clear')

def sprint(text, typing_speed = 0):
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
    sprint("\n\n        Welcome to the Custom Choose Your Own Adventure\n\n            Please type your desired game!\n        We have by default jogo1, test1, and test2\n\n", 0)
    le_game = input('Enter desired game: ')
    #ajusta o nome do jogo para pasta
    le_game = "games." + le_game
    play_game(le_game)

def play_game(jogo):
    clear()
    #importa o jogo informado no menu
    file = import_module(jogo)
    #importa o dict do jogo
    global rooms
    rooms = getattr(file, 'rooms')
    #printa o menu do jogo e depois executa
    sprint(rooms['menu'][0])
    input("Enter anything to continue: ")
    play()

def play(current_room = '1'):
    clear()
    #printa o texto da sala
    sprint(rooms[current_room][0], 0)
    #permite escolha do jogador
    while True:
        try:
            choice = rooms[current_room][int(input(rooms[current_room][5]))]
        except:
            print('Type a number 1 to 4')
        else:
            if choice != 0: break
            sprint("Choice not recognized, try again")
    #caso vitoria, para o jogo e volta ao menu principal
    if choice == 'win':
        sprint(rooms['wintext'])
        input("Type anything to return to menu")
        menu()
    #vai para sala definida pela escolha
    else:
        play(choice)


menu()


#A resolver: input 5 of dooms
