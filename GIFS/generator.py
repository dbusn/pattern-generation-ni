import numpy as np
import os, json, sys
import moviepy.editor

def save_frames_as_gif(frames: np.ndarray, output_dir: str, gif_name: str, fps: int = 10) -> None:
    """Saves a list of frames as a gif to the given output directory."""

    # If the output dir does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the gif file
    clip = moviepy.editor.ImageSequenceClip(list(frames), fps=fps)
    clip.write_gif(os.path.join(output_dir, gif_name +  ".gif"), fps=fps)

def frames_from_lists(lists: list) -> np.ndarray:
    """Converts a list of arrays into a list of frames."""
    return [np.array(_list, dtype=np.uint8) for _list in lists]

if __name__ == "__main__":
    iters = [iteration['iteration'] for iteration in json.loads(sys.argv[1])['pattern']]
    grids = [[[[255, 255, 255] for _ in range(0,4)] for _ in range(0,6)] for _ in range(0,len(iters))]

    for i, iteration in enumerate(iters):
        col_coord = int(str(iteration[0]['coord'])[0])
        row_coord = int(str(iteration[0]['coord'])[1])
        amp = iteration[0]['amplitude']
        grids[i][row_coord-1][col_coord-1] = [255-amp,255-amp, 255-amp]

    save_frames_as_gif(frames_from_lists(grids), 'gifs', sys.argv[1].split('.')[0])