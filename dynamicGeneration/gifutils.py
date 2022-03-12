import numpy, os, moviepy.editor
"""Saves a list of frames as a gif to the given output directory."""
def save_frames_as_gif(frames: numpy.ndarray, output_dir: str, gif_name: str, fps: int = 25) -> None:

    # If the output dir does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the gif file
    clip = moviepy.editor.ImageSequenceClip(list(frames), fps=fps)
    clip.write_gif(os.path.join(output_dir, gif_name +  ".gif"), fps=fps)

"""Converts a list of arrays into a list of frames."""
def frames_from_lists(lists: list) -> numpy.ndarray:
    return [numpy.array(_list, dtype=numpy.uint8) for _list in lists]