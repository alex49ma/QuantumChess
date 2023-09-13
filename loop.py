import Game
import re
import Move

myGame = Game.Game()
pattern = r'^[a-h][1-8][a-h][1-8][qrbn]?$'
patternQ = r'^[a-h][1-8][a-h][1-8], [a-h][1-8][a-h][1-8][qrbn]?$'
retry = "yes"
helpLine = "To write a move, write the UCI notation for the movement:\nI.e. To move any piece from the square b5 to the square d3 write 'b5d3'.\nIf you want to move it quantic, to d3 and e2 write 'b5d3, b5e2'\n\nWrite 'Rules' to display the set of rules for Quantum Chess\nWrite 'Over' anytime to finish the game, or 'Reset' to restart it\n\nYou can use Stockfish engine to help you move, rate your position, etc.\nTyping 'Evaluate', you will receive an evaluation of the current position, \nas a number that can be positive or negative\nHigher number means white is winning, and lower (negative) numbers mean black is winning\nType 'Evaluate move', and after type your move, to receive a number telling how good the move is\nType 'Hint' to ask Stockfish what to move in the current position\n"
rules = "Quantum Chess is a variant of the classical chess game adding some Quantum propperties. \nIn the game, sometimes pieces can be two places at once, the known as quantum superposition. \nThis happens when you make a quantum move. Quantum moves are the result of two classical \nmoves at once, so we no longer know the precise position of this piece. Piece's position \nis defined when an observation happens. In this case, when someone captures a quantum \npiece or when a quantum piece captures another. Then we have 50% chance to be on each \ndifferent position. This allows quantum entanglement. If a quantum piece has a certain \nprobability to be at one place, means that there is a probability that it is not there and \nI can pass through it with a slide move. In this case the piece may have done the movement \nor not, it depends on the final position of the previous quantum piece. It is entangled.\nTo win, you must capture the enemy king."

while(retry == "yes"):
    rival = input("Insert H to play Human vs Human. Insert C to play Human versus machine.\n")
    rival = rival.lower()
    if rival == "h" or rival == "c":
        colour = ""
        if rival in "Cc":
            while colour != "b" and colour != "w":
                colour = input("Insert W to play white or B to play black\n")
                colour = colour.lower()
        print("Type 'Help' + Intro for command details\n\n")
        while (myGame.over == False):
            try:
                print(myGame.position.strOpt2())
                msg = ""
                if rival == "h" or myGame.flagList[0] == colour:
                    if myGame.flagList[0] == "w":
                        msg = "White to move\nInsert a valid move:\n"
                    else:
                        msg = "Black to move\nInsert a valid move:\n"
                    move = input(msg)
                else:
                    print("\nThinking...\n\n")
                    hint = myGame.moveHint()  
                    hintIndex = 0 
                    move = Move.Move(hint[hintIndex][0], myGame.flagList)
                    flag = True
                    while move.isQuantic() and flag:
                        if Game.ChessUtils.isCapture(move.move0) or Game.ChessUtils.isCapture(move.move1):
                            hintIndex += 1
                            move = Move.Move(hint[hintIndex][0], myGame.flagList)
                        else:
                            flag = False
                    if move.isQuantic():
                        move = move.move0.move, ", ", move.move1.move
                    else:
                        move = move.move
                if move.lower() == "help":
                    print(helpLine)
                if move.lower() == "rules":
                    print(rules)
                if move.lower() == "evaluate":
                    print(myGame.evaluate())
                if move.lower() == "evaluate move":
                    moveEval = input("Insert move to evaluate:\n")
                    if re.search(pattern, moveEval) is not None:
                        myGame.evaluate(moveEval)

                    if re.search(patternQ, moveEval) is not None:
                        moves = moveEval.split(", ")
                        myGame.evaluate(moves[0], moves[1])

                    print(myGame.evaluate())
                if move.lower() == "hint":
                    print(myGame.moveHint())
                if move.lower() == "over":
                    sure = input("Are you sure? ")
                    if sure == "yes":
                        myGame.over = "Game ended by player"
                        break
                if move == "reset":
                    sure = input("Are you sure? ")
                    if sure == "yes":
                        myGame = Game.Game()
                        break
                if re.search(pattern, move) is not None:
                    myGame.move(move)

                if re.search(patternQ, move) is not None:
                    moves = move.split(", ")
                    myGame.qMove(moves[0], moves[1])
            except Exception as e:
                print("An error occurred:", e)
                input()
        else:
            print(myGame.position.strOpt2())
            print("Game over! " + str(myGame.over))
            retry = input("Play again? ").lower()
    else:
        print("Insert a valid rival")