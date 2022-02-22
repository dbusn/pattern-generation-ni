import json, sys, gifutils
if __name__ == "__main__":
    iters = [iteration['iteration'] for iteration in json.loads(sys.argv[1])['pattern']]
    grids = [[[[255, 255, 255] for _ in range(0,4)] for _ in range(0,6)] for _ in range(0,len(iters))]

    for i, iteration in enumerate(iters):
        col_coord = int(str(iteration[0]['coord'])[0])
        row_coord = int(str(iteration[0]['coord'])[1])
        amp = iteration[0]['amplitude']
        grids[i][row_coord-1][col_coord-1] = [255-amp,255-amp, 255-amp]

    gifutils.save_frames_as_gif(gifutils.frames_from_lists(grids), 'gifs', sys.argv[1].split('.')[0])