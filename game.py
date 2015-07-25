#! /usr/bin/env python

import copy, os, select, sys, termios, time, tty

def gameover(winrar):

  os.system('clear')
  print "\n"*10+" "*15+"GAME OVER"
  if winrar=="red": print " "*15+"RED WINS"
  else: print " "*15+"BLUE WINS"
  raw_input()
  exit()

class player:

  def __init__(self,upk,downk,rightk,leftk,typep):
    self.up=upk
    self.down=downk
    self.right=rightk
    self.left=leftk
    if typep=="red":
      self.put="f"
      self.stoptime="q"
    if typep=="blue":
      self.put=0
      self.stoptime=0

    self.last=""
    self.colour=typep
    self.xpos=2 if typep=="red" else 78
    self.ypos=2 if typep=="red" else 38

  def move(self,terrain,opponent):
    """
    0: Out of bounds
    1: ok
    2: kill condition
    """

    if self.last=="up" and self.ypos>0:
      if self.colour=="red" and (self.xpos,self.ypos-1)==(opponent.xpos,opponent.ypos): gameover("blue")
      elif self.colour=="blue" and terrain.grid[self.ypos-1][self.xpos]=="#": gameover("red")
      elif self.colour=="blue" and (self.xpos,self.ypos-1)==(opponent.xpos,opponent.ypos): gameover("blue")
      else: self.ypos-=1
      return 1

    elif self.last=="down" and self.ypos<39:
      if self.colour=="red" and (self.xpos,self.ypos+1)==(opponent.xpos,opponent.ypos): gameover("blue")
      elif self.colour=="blue" and terrain.grid[self.ypos+1][self.xpos]=="#": gameover("red")
      elif self.colour=="blue" and (self.xpos,self.ypos+1)==(opponent.xpos,opponent.ypos): gameover("blue")
      else: self.ypos+=1
      return 1

    elif self.last=="right" and self.xpos<79:
      if self.colour=="red" and (self.xpos+1,self.ypos)==(opponent.xpos,opponent.ypos): gameover("blue")
      elif self.colour=="blue" and terrain.grid[self.ypos][self.xpos+1]=="#": gameover("red")
      elif self.colour=="blue" and (self.xpos+1,self.ypos)==(opponent.xpos,opponent.ypos): gameover("blue")
      else: self.xpos+=1
      return 1

    elif self.last=="left" and self.xpos>0:
      if self.colour=="red" and (self.xpos-1,self.ypos)==(opponent.xpos,opponent.ypos): gameover("blue")
      elif self.colour=="blue" and terrain.grid[self.ypos][self.xpos-1]=="#": gameover("red")
      elif self.colour=="blue" and (self.xpos-1,self.ypos)==(opponent.xpos,opponent.ypos): gameover("blue")
      else: self.xpos-=1
      return 1
    else: return 0

class terrain:

  def __init__(self):

    self.grid=[[" " for i in range(80)] for i in range(40)]
    self.running=0

  def processcells(self,blue):

    futurear=[[" " for i in range(80)] for i in range(40)]
    for idx,i in enumerate(self.grid):
      for jdx,j in enumerate(i):
        neighbours=""
        try:neighbours+=self.grid[idx-1][jdx]
        except IndexError: pass
        try:neighbours+=self.grid[idx+1][jdx]
        except IndexError: pass
        try:neighbours+=self.grid[idx][jdx+1]
        except IndexError: pass
        try:neighbours+=self.grid[idx][jdx-1]
        except IndexError: pass
        try:neighbours+=self.grid[idx-1][jdx-1]
        except IndexError: pass
        try:neighbours+=self.grid[idx+1][jdx+1]
        except IndexError: pass
        try:neighbours+=self.grid[idx+1][jdx-1]
        except IndexError: pass
        try:neighbours+=self.grid[idx-1][jdx+1]
        except IndexError: pass
        if neighbours.count("#")<2: futurear[idx][jdx]=" "
        elif neighbours.count("#")>3: futurear[idx][jdx]=" "
        elif neighbours.count("#") in [2,3] and j=="#": 
          futurear[idx][jdx]="#"
          if (jdx,idx)==(blue.xpos,blue.ypos): gameover("red")
        if neighbours.count("#")==3 and j==" ": 
          futurear[idx][jdx]="#"
          if (jdx,idx)==(blue.xpos,blue.ypos): gameover("red")
    self.grid=copy.deepcopy(futurear)

  def display(self,player1,player2):

    os.system('clear')
    displaygrid=copy.deepcopy(self.grid)
    displaygrid[player1.ypos][player1.xpos]="\033[31m@\033[0m"
    displaygrid[player2.ypos][player2.xpos]="\033[34m0\033[0m"
    for i in displaygrid: print "".join(i)
    if self.running: print "RUNNING",
    print player1.xpos,player1.ypos,player2.xpos,player2.ypos
    print "Player 1:",player1.up,player1.down,player1.right,player1.left
    print "Player 2:",player2.up,player2.down,player2.right,player2.left

  def putcell(self,x,y):

    self.grid[y][x]="#"

def pressed():

  def isData():

    return select.select([sys.stdin], [], [], 0.11)==([sys.stdin], [], [])

  c=""
  old_settings=termios.tcgetattr(sys.stdin)
  try:
    tty.setcbreak(sys.stdin.fileno())
    c=sys.stdin.read(1) if isData() else ""
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return c

previousdt=0
def iterate():

  global previousdt
  deltat=(time.time()*1000-starttime)/200
  if deltat>previousdt: 
    previousdt=deltat
    return 1
  return 0

def mainloop(red,blue,arena):

  #Record current pressed key
  pressedkey=pressed()
  if   pressedkey==red.up:        red.last="up"
  elif pressedkey==red.down:      red.last="down"
  elif pressedkey==red.right:     red.last="right"
  elif pressedkey==red.left:      red.last="left"
  elif pressedkey==red.stoptime:  red.last="startstop"
  elif pressedkey==red.put:       red.last="put"
  elif pressedkey==blue.up:       blue.last="up"
  elif pressedkey==blue.down:     blue.last="down"
  elif pressedkey==blue.right:    blue.last="right"
  elif pressedkey==blue.left:     blue.last="left"
  elif pressedkey=="j":os.system('clear');exit()

  

  if iterate():
    if red.last in ["up","down","right","left"]: 
      red.move(arena,blue)
      red.last=""
    elif red.last=="put": 
      arena.putcell(red.xpos,red.ypos)
      red.last=""
    if blue.last in ["up","down","right","left"]: 
      blue.move(arena,red)
      blue.last=""
    if red.last=="startstop": 
      arena.running^=1
      red.last=""
    if arena.running: arena.processcells(blue)
    
    arena.display(red,blue)

if __name__=="__main__":

  os.system('clear')
  starttime=time.time()*1000
  area=terrain()
  red=player("w","r","s","a","red")
  blue=player("u","e","i","n","blue")
  while 1:
    try:
      mainloop(red,blue,area)
    except KeyboardInterrupt:
      break;
      exit()
