#! /usr/bin/env python

import os, select, sys, termios, time, tty

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

  def move(self,terrain):
    """
    0: Out of bounds
    1: ok
    2: kill condition
    """

    if self.last==self.up and self.ypos>0:
      if self.colour=="red" and terrain.grid[self.ypos-1][self.xpos]=="@": return 2
      elif self.colour=="blue" and terrain.grid[self.ypos-1][self.xpos]=="#": return 2
      else: self.ypos-=1
      return 1

    elif self.last==self.down and self.ypos<39:
      if self.colour=="red" and terrain.grid[self.ypos+1][self.xpos]=="@": return 2
      elif self.colour=="blue" and terrain.grid[self.ypos+1][self.xpos]=="#": return 2
      else: self.ypos+=1
      return 1

    elif self.last==self.right and self.xpos<79:
      if self.colour=="red" and terrain.grid[self.ypos][self.xpos+1]=="@": return 2
      elif self.colour=="blue" and terrain.grid[self.ypos][self.xpos+1]=="#": return 2
      else: self.xpos+=1
      return 1

    elif self.last==self.left and self.xpos>0:
      if self.colour=="red" and terrain.grid[self.ypos][self.xpos-1]=="@": return 2
      elif self.colour=="blue" and terrain.grid[self.ypos][self.xpos-1]=="#": return 2
      else: self.xpos-=1
      return 1
    else: return 0

class terrain:

  def __init__(self):

    self.grid=[[" " for i in range(80)] for i in range(40)]

  def processcells(self):

    for idx,i in enumerate(self.grid):
      for jdx,j in enumerate(self.grid[idx]):
        neighbours=""
        try:neigbours+=self.grid[idx-i][jdx]
        except IndexError: pass
        try:neigbours+=self.grid[idx+i][jdx]
        except IndexError: pass
        try:neigbours+=self.grid[idx][jdx+1]
        except IndexError: pass
        try:neigbours+=self.grid[idx][jdx-1]
        except IndexError: pass
        if neighbours.count("#")<2: self.grid[idx][jdx]=" "
        elif neighbours.count("#")>3: self.grid[idx][jdx]="#"

  def display(self,player1,player2):

    os.system('clear')
    displaygrid=self.grid
    displaygrid[player1.ypos][player1.xpos]="."
    displaygrid[player2.ypos][player2.xpos]="@"
    for i in displaygrid: print "".join(i)

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

directions=["up","down","right","left"]
def mainloop(red,blue,arena):

  #Record current pressed key
  pressedkey=pressed()
  if   pressedkey==red.up:        red.last="up"
  elif pressedkey==red.down:      red.last="down"
  elif pressedkey==red.right:     red.last="right"
  elif pressedkey==red.left:      red.last="left"
  elif pressedkey==red.put:       red.last="put"
  elif pressedkey==red.stoptime:  red.last="startstop"
  elif pressedkey==blue.up:       blue.last="up"
  elif pressedkey==blue.down:     blue.last="down"
  elif pressedkey==blue.right:    blue.last="right"
  elif pressedkey==blue.left:     blue.last="left"
  elif pressedkey=="j":os.system('clear');exit()

  if red.last=="startstop": arena.processcells()

  if iterate():
    if red.last in directions: 
      red.move(arena)
      # red.last=""
    elif red.last=="put": arena.putcell(red.xpos,red.ypos)
    if blue.last in directions: 
      blue.move(arena)
      # blue.last=""
    
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
