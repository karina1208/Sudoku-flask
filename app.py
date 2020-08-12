from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime
import random

app = Flask(__name__)

#initialize board
board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]

#initial page
@app.route('/', methods=['POST', 'GET'])
def index():
    global board
    #reset board each time
    board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]
    gen_board(board)
    solve(board)
    gen_playBoard(board)

    return render_template('index.html', playBoard=board)

#get and return jSON data of cell
@app.route('/checkvalid', methods=['POST', 'GET'])
def checkvalid():
    position = request.args.get('position', 0, type=int)
    number = request.args.get('number', 0, type=int)
    cellText = request.args.get('cellText', 0, type=int)
    posX = position // 9
    posY = position % 9

    check = valid(board, number, (posX, posY))
    
    if check:
        #only if the number is valid, the input will be insert to the array list
        insertToCell(board, number, (posX, posY))

    if (cellText == number):
        insertToCell(board, 0, (posX, posY))
        number = None

    app.logger.info(check) #console log

    return jsonify(number=number,check=check,cellText=cellText)

#get and return jSON data to check if the board is finished
@app.route('/checkfinish', methods=['POST', 'GET'])
def checkfinish():
    position = request.args.get('position', 0, type=int)
    number = request.args.get('number', 0, type=int)
    cellText = request.args.get('cellText', 0, type=int)

    find = find_empty(board)
    if not find:
        return jsonify(finish=True)
    else: 
        return jsonify(finish=False)

#if the number is valid, insert it in the playboard
def insertToCell(bo, num, pos):
    bo[pos[0]][pos[1]] = num

def gen_board(bo): #gen whole board
    iRow = list(range(1,10)) #i stands for initial
    random.shuffle(iRow)
    bo[0] = iRow
    iCol = [i for i in range(1,10) if i != bo[0][0]]

    while True:
        random.shuffle(iCol)
        if iCol[0] != bo[0][1] and iCol[0] != bo[0][2] and iCol[1] != bo[0][1] and iCol[1] != bo[0][2]:
            break
    
    for i in range(1,9):
        bo[i][0] = iCol[i-1]

def gen_playBoard(bo): #gen play board with random empty cell
    i = 1
    while i<=10:
        bo[random.randint(0, 8)][random.randint(0, 8)] = 0
        i += 1

def find_empty(bo):
    for i in range (len(bo)):
        for j in range(len(bo[0])): # len(bo[0]) = length of each row
            if bo[i][j] == 0:
                return (i, j) # row, col
    
    return None

def valid(bo, num, pos):
    #check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos [1] != i: #do not check the same pos
            return False
    
    #check col
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos [0] != i: #do not check the same pos
            return False

    #check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3 

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos: #do not check the same pos
                return False

    return True

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else: 
        row, col = find

    for i in range(1,10): #1-9
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0
    
    return False





if __name__ == "__main__":
    app.run(debug=True)