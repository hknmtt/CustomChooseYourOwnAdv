#    'cozinha' : {'txt' : 'Aqui tem café',
#        'spd' : 0,
#        'choicetxt' : ('>>'),
#        'connections' : ('inicial','rua'),
#        0 : 'Aqui tem café',
#        1 : 'Aqui não tem mais café',
#        2 : 'Aqui ta fazendo café',
#        },
rooms = {
    'inicial' : {'id' : 'inicial',
        'txt' : ('Você é D. T. Tive, e acorda numa manhã chata\n'
        'É um dia chuvoso, e você tem tomar o café para ir trabalhar\n'
        'A cortina do *banheiro* balança com o vento\n'
        'Do corredor da *cozinha* você sente um cheiro delicioso de panquecas\n\n'
        'Dica: Você pode digitar "ir LUGAR" para andar'),
        'spd' : 0,
        'choicetxt' : ('>>'),
        'connections' : ['cozinha','banheiro'],
        'objects' : ['spam', 'ham'],
        'locked' : False,
        'look_at_norte': 'Ao norte não tem porra nenhuma',
        },
    'cozinha' : { 'id' : 'cozinha',
        'txt' : 'Aqui tem café',
        'spd' : 0,
        'choicetxt' : ('>>'),
        'connections' : ['inicial','rua'],
        'objects' : ['ham'],
        'locked' : False,
        0 : 'Aqui tem café',
        1 : 'Aqui não tem mais café',
        2 : 'Aqui ta fazendo café',
        },
    'banheiro' : { 'id' : 'banheiro',
        'txt' : ('this is bathroom, you can only go back to inicial'),
        'spd' : 0,
        'choicetxt' : ('>>'),
        'connections' : ['inicial'],
        'objects' : [],
        'locked' : True,
        'locked_txt' : 'The bathroom is locked'
        },
    'rua' : { 'id' : 'rua',
        'txt' : ('This is outside, you can only go to kitchen'),
        'spd' : 0,
        'choicetxt' : ('>>'),
        'connections' : ['cozinha'],
        'objects' : [],
        'locked' : True,
        },
    }


objects = {
    'spam' : {
    'txt_in_room' : '\nA spam can is here, from monty python',
    'description' : 'The spam can is really cool',
    'take_txt' : 'You kneel and take the spam',
    'portable' : True,
    },
    'ham' : {
    'txt_in_room' : '\nA ham is here, from monty python',
    'description' : 'The ham can is really cool',
    'take_txt' : 'You kneel and take the ham',
    'portable' : False,
    'take_fail_txt' : "The ham is way too heavy",
    },
    'arma' : {
    'portable' : False,
    'drop_fail_txt' : 'It would be unwise to leave my gun here',
    }


}

starterinv = ['arma', 'badge']
