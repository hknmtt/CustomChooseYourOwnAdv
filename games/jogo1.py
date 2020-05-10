"""
rooms = {
    'inicial': {'id': 'inicial',
                'txt': ('Linha 1\n'
                        'Linha 2\n'
                        'Linha 3\n\n'),
                'spd': 0,
                'choicetxt': ('>>'),
                'connections': ['sala1', 'sala2'],
                'objects': ['objeto1', 'objeto2'],
                'locked': False,
                'locked_txt' : ''
                'look_at_porta': 'Texto ao olhar pra porta',
                'look_at_corredor': 'Texto ao olhar para corredor',
                'custom_comando1': 'o que o texto comando1 deve exec',
                'custom_comando2': 'o que o texto comando2 deve exec',
                'use_item': 'o que o item deve executar se executado aqui',
                'use_txt_item': 'o que deve printar quando usar item',
                '0': ('Linha 1\nLinha 2\nLinha 3\n\n'),
                '1': ('estado 1 Linha 1\n estado 2 Linha 2\n estado 3 Linha 3\n\n'),

                },
}
"""
rooms = {
    'inicial': {'id': 'inicial',
                'txt': ('   Por que acordei aqui? Onde estou?\n'
                        '   Preciso sair daqui...\n\n'),
                'spd': 150,
                'choicetxt': ('Pressione ENTER para continuar...'),
                'objects': [],
                'skip_room': 'sala1',
                },
    'sala1': {'id': 'sala1',
                'txt': ('    As paredes são feitas de tijolos de pedra, todos úmidos'
                ' e cheios de musgos verdes. O ar viciado e cheio de poeira declara'
                ' que este lugar não vê o sol a muito tempo\n'
                '   Há uma /passagem/  com teias de aranha\n'
                'Dica: Talvez você possa ***IR*** ou ***OLHAR*** para algo\n\n') ,
                'spd': 150,
                'choicetxt': ('>>'),
                'connections_dict': {
                                    'passagem' : 'sala2'
                                    },
                'connections': ['sala2'],
                'objects': [],
                'locked': False,
                'look_at_passagem': ('Essa passagem é feita de um arco com as mesmas pedras'
                                    ' da parede. Há uma fina camada de teia cobrindo os cantos da passagem.'),
                },
    'sala2': {'id': 'sala2',
                 'txt': ('  Diferente da sala anterior, aqui tem uma /mesa/ com uma gaveta.\n'
                         'Há uma /passagem/ de arco com teia, e uma /porta/ de pedra ao lado'
                         ' oposto da passagem\n\n'),
                 'spd': 150,
                 'choicetxt': ('>>'),
                 'connections_dict': {
                                     'porta': 'sala3'
                                     },
                 'connections': ['sala1','sala3'],
                 'objects': ['chave','porta'],
                 'locked': False,
                 'look_at_passagem': ('Essa passagem é feita de um arco com as mesmas pedras'
                                    ' da parede. Há uma fina camada de teia cobrindo os cantos da passagem.'),
                 'look_at_mesa': 'Na gaveta, há uma .chave.\n Dica: Talvez eu possa ***PEGAR*** algo',
                 'look_at_gaveta': 'Na gaveta, há uma .chave.\n Dica: Talvez eu possa ***PEGAR*** algo',
                 'custom_abrir gaveta':  'olhar mesa',
                 'use_chave': 'debug_unlock sala3 && debug_remove_item chave',
                 'use_txt_chave': "Coloquei a chave na fechadura da porta, e ela se abriu... A chave parece estar presa a porta agora",
                 },
    'sala3': {'id': 'sala3',
                 'txt': ('This is outside, you can only go to kitchen'),
                 'spd': 0,
                 'choicetxt': ('>>'),
                 'connections': ['cozinha'],
                 'objects': [],
                 'locked': True,
                 'locked_txt': 'A porta está fechada, talvez se eu ***USAR*** algo ela abra',
            },
}


objects = {
    'chave': {
        'txt_in_room': 'Uma .chave. se encontra aqui',
        'description': 'Uma .chave. dourada, gelada ao toque',
        'take_txt': 'Peguei a .chave. e guardei em meu bolso',
        'portable': True,
        'plainsight': False,
    },
    'porta': {
        'txt_in_room': 'cu',
        'description': 'Uma porta de pedra, com uma fechadura',
        'portable': False,
        'plainsight': False,
    },

}

starterinv = []
