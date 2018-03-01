import sys

players = {0:[],1:[]}
matches = []
f = open(sys.argv[1])
for line in f:
    player1 = line.split()[0]
    player2 = line.split()[1]
    if player1 < player2:
        match = '(' + player1 + ', ' + player2 + ')'
    elif player1 > player2:
        match = '(' + player2 + ', ' + player1 + ')'
    else:
        print('ERROR: No player can play with himself! This match has been ignored.')
        continue
    day = 0
    while player1 in players[day] or player2 in players[day]:
        day = day + 1
        if day not in players.keys():
            players[day]=[]
    players[day].append(player1)
    players[day].append(player2)
    matches.append(match + ' ' + str(day))
for k in sorted(matches):
    print(k)
