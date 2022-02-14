#!/usr/bin/env python

import json
import GifDisplay as gd

def load_pattern(filename: str) -> list:
    with open(filename) as in_file:
        pattern = json.load(in_file)
        iterations = []

        for iteration in pattern['pattern']:
            iterations.append(iteration['iteration'])

    return iterations

filename = 'UU.json'    

iters = load_pattern(filename)

grids = [[[[255, 255, 255] for _ in range(0,4)] for _ in range(0,6)] for _ in range(0,len(iters))]

for i, iteration in enumerate(iters):
    col_coord = int(str(iteration[0]['coord'])[0])
    row_coord = int(str(iteration[0]['coord'])[1])
    amp = iteration[0]['amplitude']
    
    grids[i][col_coord-1][row_coord-1] = [255-amp,255-amp, 255-amp]

arr = gd.frames_from_lists(grids)
gd.save_frames_as_gif(arr, 'gif_output', filename.split('.')[0])
