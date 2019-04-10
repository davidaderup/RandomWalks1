# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:42:36 2019

@author: david
"""

import numpy as np

# Set case, 1 = free random walk, 2 = self avoiding random walk, 3 = biased sampling
case = 3
# Set parameters
dims = 3
steps = 160
walks = 10000


# Initialize
location = np.zeros((dims, 1))
history = []
dists = []
move_products = []
# Create list with possible moves
all_moves = []
base_vector = np.zeros((dims, 1))
for dim in range(dims):
    pos_move = base_vector.copy()
    pos_move[dim] = 1
    neg_move = base_vector.copy()
    neg_move[dim] = -1
    
    all_moves.append(pos_move)
    all_moves.append(neg_move)
    
# Random walk function
def random_walk(location, dims, all_moves, case, history = None):
    # Determine dim to move in and direction
    if case == 1:
        # Free random walk
        movement = all_moves[np.random.randint(len(all_moves))]
    if case == 2:
        # Self avoiding random walk
        possible_moves = all_moves.copy()
        # find move that brings back to previous location and remove
        for index, possible_move in enumerate(possible_moves):
            if len(history)>1 and np.array_equal(possible_move,  history[-2] - location):
                possible_moves.pop(index)
                break
        movement = possible_moves[np.random.randint(len(possible_moves))]
    if case == 3:
        # Biased sampling
        possible_moves = all_moves.copy()
        lattice_spots = [possible_move + location for possible_move in possible_moves]
        index = 0
        for lattice_spot in lattice_spots:
            if len(possible_moves) == 0:
                break
            for h in history:
                if len(history) > 1 and np.array_equal(lattice_spot, h):
                    possible_moves.pop(index)
                    index -= 1
                    break
            index += 1
        if len(possible_moves) > 0:
            movement = possible_moves[np.random.randint(len(possible_moves))]
        else:
            movement = np.zeros(location.shape)
        return location + movement, len(possible_moves)
        
    return location + movement, None

# Loop for walks
for walk in range(walks):
    if walk % (walks/100) == 0:
        print(walk)
    location = np.zeros(location.shape)
    history = []
    if case == 3:
        move_product = 1
        
    # Loop for steps
    for step in range(steps):
        history.append(location)
        location, number_of_possible_moves = random_walk(location, dims, all_moves, case, history=history)
        if case == 2:
            # If chain touches itself, terminate
            terminate = False
            for h in history[:-1]:
                if np.array_equal(h, location):
                    terminate = True
                    break
            if terminate:
                break
        if case == 3:
            move_product *= number_of_possible_moves
            if np.array_equal(history[-1], location):
                break
        
    # Calc distance
    if len(history) == steps:    
        dist = np.sum(location * location)
        dists.append(dist)
        if case == 3:
            move_products.append(move_product)
if case == 3:
    numerators = []
    for dist, move_product in zip(dists, move_products):
        numerators.append(dist*move_product)
    av_dist = np.sum(numerators)/np.sum(move_products)
else:
    av_dist = np.mean(dists)