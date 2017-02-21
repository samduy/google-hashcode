#!/bin/python

import sys

# Type of invalid piece
M = -1
T = -2

# Handle parameters
if (len(sys.argv)) < 3:
  sys.stderr.write("Usage: %s input_file output_file\n" % sys.argv[0]);
  sys.exit()

iFile = sys.argv[1]
oFile = sys.argv[2]

input = open(iFile).readlines()

setting = input[0].split()
R = int(setting[0])
C = int(setting[1])
L = int(setting[2])
H = int(setting[3])

# Main input data: pizza to be cut
pizza = input[1:]

# Output data: slices/pieces after cut
gPieces = []

# Function: cutting pizza with specified shape of piece
# Shape of piece: a rectangular
def cut(pizza, piece_rect):
  global R,C

  pieces = []

  h = piece_rect[0]
  w = piece_rect[1]

  for i in range(0,C,w):
    for j in range(0,R,h):
      c1 = i;
      c2 = i+w-1
      if (c2 > C-1): c2 = C-1
      r1 = j;
      r2 = j+h-1
      if (r2 > R-1): r2 = R-1
      # a piece
      p = [r1, c1, r2, c2]
      # add to the list
      pieces.append(p)

  return pieces

# Refine the cut, filter only the pieces that validate
# The validated piece: qualify the minumum number of
# each ingredient (L) and maximum total number of them (H)
def refine_cut(pieces):
    ps = []

    for p in pieces:
      if (check(p) == 1): 
	ps.append(p)

    return ps

# Calculate the size of the cut
def pie_size(p):
  r = p[3] - p[1] + 1
  c = p[2] - p[0] + 1
  return r*c

# Calculate possible score in a set of slices
def cal_score(pieces):
  score = 0

  for p in pieces:
    if (check(p) == 1):
      score = score + pie_size(p)

  return score

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
  f = open(oFile, "w")
  # write total number of slices
  f.write(str(len(fined_pieces))+"\n")

  for p in fined_pieces:
    f.write(str(p[0])+" "+str(p[1])+" "+str(p[2])+" "+str(p[3])+"\n")

  f.flush()
  f.close()

## Some ALGORITHM to improve the cut result

# Identify the neighbour cells (left, right, up, down)
def piece_left_n_cells(p, n):
  r1,c1,r2,c2 = p[0],p[1],p[2],p[3]

  if (c1-n) < 0: return None
  else: 
    return [r1, c1-n, r2, c1-1]

def piece_right_n_cells(p, n):
  global C
  r1,c1,r2,c2 = p[0],p[1],p[2],p[3]

  if (c2+n) > C: return None
  else: 
    return [r1, c2+1, r2, c2+n]

def piece_up_n_cells(p, n):
  r1,c1,r2,c2 = p[0],p[1],p[2],p[3]
  if (r1-n) < 0: return None
  else: 
    return [r1-n, c1, r1-1, c2]

def piece_down_n_cells(p, n):
  global R
  r1,c1,r2,c2 = p[0],p[1],p[2],p[3]

  if (r2+n) > R: return None
  else: 
    return [r2+1, c1, r2+n, c2]

# Check if the cells is already cut (belong to validate pieces)
# return 1 if the cells have not been cut yet
def is_available_piece(pie):
  global gPieces

  if (pie == None): return None

  r1,c1,r2,c2 = pie[0],pie[1],pie[2],pie[3]

  for p in gPieces:
    if ( (c2 < p[1]) or (c1 > p[3]) ): continue
    elif ( (r2 < p[0]) or (r1 > p[2]) ): continue
    else: 
      return 0
      break

  return 1

# Merge two slices into one new slice
def merge_piece(p1, p2):
  # vertically
  if ((p1[1] == p2[1]) and (p1[3]==p2[3])):
    r1 = min(p1[0],p2[0],p1[2],p2[2])
    r2 = max(p1[0],p2[0],p1[2],p2[2])
    return [r1, p1[1], r2, p2[3]]
  # horizontally
  elif ((p1[0] == p2[0]) and (p1[2]==p2[2])):
    c1 = min(p1[1],p2[1],p1[3],p2[3])
    c2 = max(p1[1],p2[1],p1[3],p2[3])
    return [p1[0], c1, p2[2], c2]
  else: return p1

# Cut any big slices with best strategy
# check to make sure it return best result possible
# TODO:
def best_cut(big_pieces):
  #print big_pieces
  row = big_pieces[2] - big_pieces[0] + 1
  #print "Row:" + str(row)
  if (row > H): row = H
  elif (row < 1): row = 1
  return refine_cut(cut(big_pieces, [row, H/row]))

# IMPROVE CUTTING STRATEGY
def improve_cut():
  global H, gPieces

  cut_pieces = []
  new_pieces = []

  for piece in gPieces:
    cut_pieces.append(piece)

  for pie in cut_pieces:
    p = pie
    max_row = H
    count = 1

    # original score
    orig_score = pie_size(p)
    score = 0

    # merge with not-cut cells upper
    p_up = piece_up_n_cells(p,1)
    while is_available_piece(p_up):
      if (count >= max_row): break
      count = count + 1
      p = merge_piece(p, p_up)
      p_up = piece_up_n_cells(p,1)
    # merge with not-cut cells lower
    p_down = piece_down_n_cells(p,1)
    while is_available_piece(p_down):
      if (count >= max_row): break
      count = count + 1
      p = merge_piece(p, p_down)
      p_down = piece_down_n_cells(p,1)

    #print "Count:"+ str(count)

    if (p != pie):
      # cut after merging
      best_slices = best_cut(p)
  
      if (best_slices != None):
        # check if it is improvement or not
        score = cal_score(best_slices)
        if (orig_score < score):
  	#print "Origin score:" + str(orig_score)
  	#print "After score:" + str(score)
          del(gPieces[gPieces.index(pie)]) # delete p from gPieces
          for q in best_slices:
	    if (q != None): 
	      if (q not in gPieces): gPieces.append(q)
    
## MAIN PROGRAM

#print pizza
#print "L="+ str(L)

#print check([0,0,1,1])
#print count("M",[0,0,1,1])
#print count("T",[0,0,1,1])

# Dumpiest cut (no improvement)
gPieces = refine_cut(cut(pizza, [1,H]))
print cal_score(gPieces)

# Some improvement
improve_cut()
#print gPieces
print cal_score(gPieces)

# Process: output result to file
output(gPieces)
