#!/usr/bin/env python

import json
import GifDisplay
import sys

def load_pattern(filename: str) -> list:
    with open(filename) as in_file:
        pattern = json.load(in_file)
        iterations = []

        for iteration in pattern['pattern']:
            iterations.append(iteration['iteration'])

    return iterations

if __name__ == "__main__":
    json_f = sys.argv[1]
    iters = load_pattern(json_f)
    grids = [[[[255, 255, 255] for _ in range(0,4)] for _ in range(0,6)] for _ in range(0,len(iters))]

    for i, iteration in enumerate(iters):
        col_coord = int(str(iteration[0]['coord'])[0])
        row_coord = int(str(iteration[0]['coord'])[1])
        amp = iteration[0]['amplitude']
    
        # print("col: " + str(col_coord))
        # print("row: " + str(row_coord))
        grids[i][row_coord-1][col_coord-1] = [255-amp,255-amp, 255-amp]

    arr = GifDisplay.frames_from_lists(grids)
    GifDisplay.save_frames_as_gif(arr, 'gifs', json_f.split('.')[0])