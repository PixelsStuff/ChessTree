# ChessTree
Creates a Trie from your chess moves. 
The tree contains infromation with their Win/Draw/Loss ratio, number of games, and includes 5 (by default) example games played by the target.

#example
the program includes a function to print the tree with options to limit how many layers to print, in order to reduce visual clutter.

With 5 layers and games within the past month (maxarchrives = 1), trees look somthing like:
'''
   Nf3 games: 6 ,wins: 3 losses: 2 draws 1
    |__  c5 games: 2 ,wins: 0 losses: 1 draws 1
      |__  c4 games: 2 ,wins: 0 losses: 1 draws 1
        |__  e6 games: 1 ,wins: 0 losses: 1 draws 0
        |__  g6 games: 1 ,wins: 0 losses: 0 draws 1
    |__  Nf6 games: 2 ,wins: 2 losses: 0 draws 0
      |__  c4 games: 1 ,wins: 1 losses: 0 draws 0
        |__  d6 games: 1 ,wins: 1 losses: 0 draws 0
      |__  g3 games: 1 ,wins: 1 losses: 0 draws 0
        |__  g6 games: 1 ,wins: 1 losses: 0 draws 0
    |__  d5 games: 1 ,wins: 1 losses: 0 draws 0
      |__  c4 games: 1 ,wins: 1 losses: 0 draws 0
        |__  c6 games: 1 ,wins: 1 losses: 0 draws 0
    |__  c6 games: 1 ,wins: 0 losses: 1 draws 0
      |__  c4 games: 1 ,wins: 0 losses: 1 draws 0
        |__  g6 games: 1 ,wins: 0 losses: 1 draws 0
'''
