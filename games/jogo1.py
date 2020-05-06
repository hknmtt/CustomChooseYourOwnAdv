#    'cozinha' : {'txt' : 'Aqui tem café',
#        'spd' : 0,
#        'choicetxt' : ('>>'),
#        'connections' : ('inicial','rua'),
#        0 : 'Aqui tem café',
#        1 : 'Aqui não tem mais café',
#        2 : 'Aqui ta fazendo café',
#        },
rooms = {
    'inicial': {'id': 'inicial',
                'txt': ('Você é D. T. Tive, e acorda numa manhã chata\n'
                        'Está muito escuro aqui no quarto\n'
                        'Dica: talvez você possa ACENDER algo\n\n'),
                'spd': 0,
                'choicetxt': ('>>'),
                'connections': ['cozinha', 'banheiro'],
                'objects': [],
                'locked': False,
                'look_at_porta': 'A porta está trancada, a chave deve estar na cozinha',
                'look_at_corredor': 'O corredor da cozinha está escuro, talvez eu deva acender a luz antes',
                'custom_acender': 'debug_change_state 1',
                'custom_apagar': 'debug_change_state 0',
                'use_chave': 'debug_unlock banheiro',
                'use_txt_chave': "I've unlocked the bathroom",
                '0': ('Está muito escuro aqui no quarto\nDica: talvez você possa ACENDER algo\n\n'),
                '1': ('É um dia chuvoso, e você tem tomar o café para ir trabalhar\n'
                      'A /porta/ do *banheiro* está trancada\n'
                      'Do corredor da *cozinha* você sente um cheiro delicioso de panquecas\n\n'
                      'Dica: Você pode digitar "ir LUGAR" para andar'),

                },
    'cozinha': {'id': 'cozinha',
                'txt': 'Aqui tem café',
                'spd': 0,
                'choicetxt': ('>>'),
                'connections': ['inicial', 'rua'],
                'objects': ['chave'],
                'locked': False,
                'custom_spam': 'debug_spawn spam',
                '0': 'Aqui tem café',
                '1': 'Aqui não tem mais café',
                '2': 'Aqui ta fazendo café',
                },
    'banheiro': {'id': 'banheiro',
                 'txt': ('this is bathroom, you can only go back to inicial'),
                 'spd': 0,
                 'choicetxt': ('>>'),
                 'connections': ['inicial'],
                 'objects': [],
                 'locked': True,
                 'locked_txt': 'The bathroom is locked',
                 },
    'rua': {'id': 'rua',
            'txt': ('This is outside, you can only go to kitchen'),
            'spd': 0,
            'choicetxt': ('>>'),
            'connections': ['cozinha'],
            'objects': [],
            'locked': True,
            },
}


objects = {
    'spam': {
        'txt_in_room': 'A spam can is here, from monty python',
        'description': 'The spam can is really cool',
        'take_txt': 'You kneel and take the spam',
        'portable': True,
    },
    'ham': {
        'txt_in_room': 'A ham is here, from monty python',
        'description': 'The ham can is really cool',
        'take_txt': 'You kneel and take the ham',
        'portable': False,
        'take_fail_txt': "The ham is way too heavy",
    },
    'arma': {
        'portable': False,
        'description': 'My trusty colt m1911',
        'drop_fail_txt': 'It would be unwise to leave my gun here',
    },
    'chave': {
        'txt_in_room': 'There is a key lying around here',
        'description': 'A golden key',
        'take_txt': 'I took the key',
        'portable': True,
    },


}

starterinv = ['arma']
