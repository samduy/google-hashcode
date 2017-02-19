#!/bin/python

# Type of invalid piece
M = -1
T = -2

input = open("medium.in").readlines()

setting = input[0].split()
R = int(setting[0])
C = int(setting[1])
L = int(setting[2])
H = int(setting[3])

pizza = input[1:]

def cut(pizza, piece_rect):
  global R,C

  pieces = []

  h = piece_rect[0]
  w = piece_rect[1]

  for i in range(0,C,w):
    for j in range(0,R,h):
      c1 = i;
      c2 = i+w-1
      if (c2 > C): c2 = C
      r1 = j;
      r2 = j+h-1
      if (r2 > R): r2 = R
      # a piece
      p = [r1, c1, r2, c2]
      # add to the list
      pieces.append(p)

  return pieces

# Refine the cut, filter only the pieces that validate
def refine_cut(pieces):
    score = 0
    ps = []

    for p in pieces:
      if (check(p) == 1): 
	ps.append(p)
	score = score + pie_size(p)

    return ps, score

# Calculate the size of the cut
def pie_size(p):
  r = p[3] - p[1] + 1
  c = p[2] - p[0] + 1
  return r*c

# Check if a piece is validated or not
# Return 1 if OK
# Return 0 if it's too big
# Return -1 if it lacks of Mushroom
# Return -2 if it lacks of Tomato
def check(piece):
  global M,T,H,L

  s = pie_size(piece)

  if (s > H): ret = 0
  elif (count("M",piece) < L) : ret = M
  elif (count("T",piece) < L) : ret = T
  else : ret = 1

  return ret

# Counting number of ingredient in a piece
def count(c, piece):
  global pizza

  cnt = 0;
  for i in range(piece[0], piece[2]+1):
    for j in range(piece[1], piece[3]+1):
      if (pizza[i][j] == c): cnt = cnt+1
  return cnt

# Print slices to file
def output(fined_pieces):
  f = open("sol-medium-1.out", "w")
  # write total number of slices
  f.write(str(len(fined_pieces))+"\n")

  for p in fined_pieces:
    f.write(str(p[0])+" "+str(p[1])+" "+str(p[2])+" "+str(p[3])+"\n")

  f.flush()
  f.close()

#print pizza
#print "L="+ str(L)

#print check([0,0,1,1])
#print count("M",[0,0,1,1])
#print count("T",[0,0,1,1])

cut, score = refine_cut(cut(pizza, [1,H]))
#print cut
print score
output(cut)
