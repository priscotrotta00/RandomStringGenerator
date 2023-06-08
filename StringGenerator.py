from player import Player
from server import Server
from table import Table

server = Server()
table = Table(server)
num_players = 3

players = []
for i in range(num_players):
    player = Player()
    players.append(player)
    table.add_player(player)

table.generate_players_keys()

table.send_signed_public_keys_to_server()
table.send_signed_public_keys_to_players()

table.send_public_keys_set_signs_to_server()
table.send_public_keys_set_signs_to_players()

table.generate_contributes()

table.send_signed_committed_contributes_to_server()
table.send_signed_committed_contributes_to_players()

table.send_openings_to_server()
table.send_openings_to_players()

table.compute_random_string()

################################################## CHECKS #####################################################

verbose = 1
if(verbose): 
    signed_public_keys = server.get_signed_public_keys()
    for player in players:
        if(player.get_signed_public_keys() != signed_public_keys):
            print('check signed public keys                 failed')
            exit()
    print('check signed public keys                 passed')

    
    sign_sets = server.get_public_keys_set_signs()
    for player in players:
        if(player.get_public_keys_set_signs() != sign_sets):
            print('check signs sets                         failed')
            exit()
    print('check signs sets                         passed')
    
    
    signed_committed_contributes = server.get_signed_committed_contributes()
    for player in players:
        if(player.get_signed_committed_contributes() != signed_committed_contributes):
            print('check signed committed contributes       failed')
            exit()
    print('check signed committed contributes       passed')


    signed_openings = server.get_signed_openings()
    for player in players:
        if(player.get_signed_openings() != signed_openings):
            print('check openings                           failed')
            exit()
    print('check openings                           passed')


    game_contributes = server.get_game_contributes()
    for player in players:
        if(player.get_game_contributes() != game_contributes):
            print('check contributes game                   failed')
            exit()
    print('check contributes game                   passed')


    random_string = server.get_random_string()
    for player in players:
        if(player.get_random_string() != random_string):
            print('check random string                      failed')
            exit()
    print('check random string                      passed')
    

print('\nLa stringa casuale generata e\':')
print(server.get_random_string())#.decode('latin1')