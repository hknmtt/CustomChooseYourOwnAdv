#    'inicial' : {'txt' : 'Bem vindo ao teste 1, mortal.',
#        'spd' : '100',
#        'choicetxt' : 'I will choose... ',
#        '1' : 'roomifchoice1',
#        '2' : 'roomifchoice2',
#        '3' : 'roomifchoice3',
#        '4' : 'roomifchoice4'
#        },
rooms = {
    'inicial' : {'txt' : ('Você é D. T. Tive, e acorda numa manhã chata\n'
        'É um dia chuvoso, e você tem tomar o café para ir trabalhar\n\n\n'
        'Dica: Você pode digitar "ir LUGAR" para andar\n\n'),
        'spd' : 100,
        'choicetxt' : ('Você se levanta da cama e decide ir para...\n'
            '1. Cozinha         2. Banheiro\n>>'),
        'connections' : ('cozinha','banheiro'),
        },
    'cozinha' : {'txt' : 'This is kitchen, you can only go back to inicial or go outsite',
        'spd' : 100,
        'choicetxt' : ('>>'),
        'connections' : ('inicial','rua'),
        },
    'banheiro' : {'txt' : ('this is bathroom, you can only go back to inicial'),
        'spd' : 100,
        'choicetxt' : ('>>'),
        'connections' : ('inicial'),
        },
    'rua' : {'txt' : ('This is outside, you can only go to kitchen'),
        'spd' : 100,
        'choicetxt' : ('>>'),
        'connections' : ('cozinha'),
        },
    }
