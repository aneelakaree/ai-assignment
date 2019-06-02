import numpy as np
from TicTacToe import TicTacToeStatic
from random import shuffle

class Node:
    def __init__(self,s,cnt,x=1,c=None,m=None,v=None):
        self.s = s
        self.children = [] 
        self.x = x 
        self.move = m 
        self.score = v
        self.cnt = cnt

    def expand(self):
        status = TicTacToeStatic.Status(self.s)
        if(status != None):
            return
        moves = TicTacToeStatic.available_moves(self.s)
        if(self.cnt<=3):
            moves = TicTacToeStatic.removecopies(self.s,moves)

        turn = self.x
        for move in moves:
            new_s = self.s.copy()
            r = move[0]
            c = move[1]
            new_s[r][c] = turn
            next = Node(new_s,self.cnt+1,turn*-1,None,(r,c))
            self.children.append(next)
        shuffle(self.children)
    def build_tree(self):
        self.expand()
        flag = 0
        for node in self.children:
            if(flag == 0):
                node.build_tree()
            else:
                node.score = 99
            if(node.score == self.x):
                self.score = node.score
                flag = 1 
        self.children = [x for x in self.children if x.score != 99 ]
        self.compute_score()
    def compute_score(self):
        status = TicTacToeStatic.Status(self.s)
        if(status != None):
            self.score = status
            return
            
        score1 = -1
        score2 = 1
        for child in self.children:
            if(self.x == 1):
                if(child.score > score1):
                    score1 = child.score
                if(child.score == 1):
                    break
            if(self.x == -1):
                if(child.score < score2):
                    score2 = child.score
                if(child.score == -1 ):
                    break
                    
        if(self.x == 1):
            self.score = score1
        elif(self.x == -1):
            self.score = score2

class MiniMaxPlayer:
    def __init__(self,name='MiniMax'):
        self.name = name
        self.x = None

    def make_a_move(self,ss):
        s=np.array(ss.copy())
        cnt = 0
        length = len(ss)
        for i in range(length):
            for j in range(length):
                if(s[i][j]!=0):
                    cnt += 1

        treeRoot = Node(s,cnt,self.x)
        treeRoot.build_tree()
        r=0
        c=0
        for child in treeRoot.children:
            if(child.score==treeRoot.score):
                move = child.move
                r = move[0]
                c = move[1]
                break

        return r*len(s)+c