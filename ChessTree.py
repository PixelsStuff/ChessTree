import requests
import re
import chess
import chess.pgn
import io
useragent = '[put your email or chess.com username here, this is for the API request only]'
player = '[player username]'
color = 'W'
allowedtcs = ["300",'600'] #keep this as a string, for time controls with increment such as 3+2 use 180 + 2
visuallimiter = 5 #This is just for visualzation purposes with the print_tree method ONLY, this does not change or limit the structure of the tree
def installarchrives(agent=useragent,player = None):
    if useragent is None:
        headers = {
            "User-Agent": "unknown"
        }
    else:
        headers = {
            "User-Agent": str(useragent)
        }
    try:
            #print("https://api.chess.com/pub/player/" + player + "/games/archives")
            response = requests.get("https://api.chess.com/pub/player/" + player + "/games/archives", headers=headers)
            response.raise_for_status()
            archrives = response.json()
            archrives = list(archrives["archives"])
            archrives.reverse()
            return archrives
    except:
        pass
def installgamesfromarchrive(agent=useragent,archrive=[],maxarchrives = 120):
     iforgothenumberationsyntax = 0
     print(len(archrives))
     if useragent is None:
        headers = {
            "User-Agent": "unknown"
        }
     else:
        headers = {
            "User-Agent": str(useragent)
        }
     games = []
     for month in archrive:
          try:
            response = requests.get(month, headers=headers)
            for game in response.json()["games"]:
                #game = dict(game)
                try:
                    pgn = game['pgn']
                    games.append(pgn)
                except:
                    print("one game failed to load")
            # print(game)
            iforgothenumberationsyntax += 1
            print(str(iforgothenumberationsyntax) + "/" + str(len(archrive)))
            if iforgothenumberationsyntax >= maxarchrives:
                break
          except:
            print("I have no clue why this happens.")
     return games

def getpgninfo(pgn_string):
    fields_to_extract = [
        "White", "Black", "WhiteElo", "BlackElo",
        "Date", "StartTime", "Result", "UTCDate", "UTCTime",
        "EndDate", "EndTime", "Termination", "ECO", "Event","TimeControl"
    ]

    metadata = {}

    for field in fields_to_extract:
        match = re.search(rf'\[{field} "(.*?)"\]', pgn_string)
        if match:
            metadata[field.lower()] = match.group(1)
        else:
            metadata[field.lower()] = "Unknown"

    return metadata

class ChessTree():
    def __init__(self,value = None):
        self.value = value
        self.wins = 0
        self.draws = 0
        self.losses = 0 
        self.count = 0
        self.examplegames = []
        self.children = {}
        self.parent = None

    def add_sequence(self, sequence,result = None):
        node = self
        for thing in sequence:
            if thing not in node.children:
                node.children[thing] = ChessTree(thing)
            node = node.children[thing]
            node.count += 1
            if len(self.examplegames) < 5:
                node.examplegames.append(sequence)
            if result == 1:
                node.wins += 1
            elif result == -1:
                node.losses += 1
            else:
                node.draws += 1

    def print_tree(self, level=0):
        if level > 1:
            indent = ' ' * level * 2 + '|__ '
        else:
            indent = ' ' * level * 2
        if (self.value is not None) and level < visuallimiter:
            print(indent ,self.value ,'games:',self.count,',wins:',self.wins,'losses:',self.losses,'draws',self.draws)
        for child in self.children.values():
            child.print_tree(level + 1)

def getpgn(pgn_text):
    pgn_file = io.StringIO(pgn_text)

    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break

        board = game.board()
        move_list = []

        for move in game.mainline_moves():
            san = board.san(move)
            move_list.append(san)
            board.push(move)


    return move_list

def filtergamesplayercolor(games,player=player,color=color,allowedtcs = allowedtcs):
    passed= []
    for game in games:
        info = getpgninfo(game)
        if info['white'] == player:
            pc = 'W'
        else:
            pc = 'B'
        if pc == color and info['timecontrol'] in allowedtcs:
            passed.append(game)
    return passed

archrives = installarchrives(player=player)
games = installgamesfromarchrive(archrive=archrives,maxarchrives=120) #allows for up to games in the past 100 months
games = filtergamesplayercolor(games)
print(len(games))

root = ChessTree()
for game in games:
    moves = getpgn(game)
    res = getpgninfo(game)['result']
    if res == "1-0":
        if color == 'W':
            res = 1
        else:
            res = -1
    elif res == "0-1":
            if color == 'B':
                res = 1
            else:
                res = -1
    else:
        res = 0.5
    
    root.add_sequence(moves,res)

root.print_tree()

