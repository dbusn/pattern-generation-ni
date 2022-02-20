from numpy import ndarray, random, uint8, array
from os import path, makedirs, getcwd
from moviepy.editor import ImageSequenceClip, ImageClip

size = { 
    "frames": 180,
    "width": 4,
    "height": 6,
    "fps": 15
}

def generate_random_gif(frames: int, width: int, height: int) -> ndarray:
    return random.randint(256, size=[frames, height, width, 3], dtype=uint8)

def save_frames_as_gif(frames: ndarray, output_dir: str, gif_name: str):
    """Saves a list of frames as a gif to the given output directory."""

    frames_dir = path.join(output_dir, "frames", gif_name)
    
    # If the output dir does not exist, create it
    if not path.exists(frames_dir):
        makedirs(frames_dir)

    # Save the gif file
    clip = ImageSequenceClip(list(frames), fps=size["fps"])
    clip.write_gif(path.join(output_dir, gif_name +  ".gif"), fps=size["fps"])

    # Save individual frames
    for i, frame in enumerate(clip.iter_frames()):
        ImageClip(frame).save_frame(path.join(frames_dir, "frame_" + str(i) + ".png"))

def load_gif_to_frames(gif_frames_dir_path: str) -> ndarray:
    """Loads a gif from a directory."""
    return [frame for frame in ImageSequenceClip(path.join(gif_frames_dir_path, "frames"), fps=size["fps"]).iter_frames()]

def frames_from_lists(lists: list) -> ndarray:
    """Converts a list of arrays into a list of frames."""
    return [array(_list, dtype=uint8) for _list in lists]

def get_custom_gif() -> ndarray:
    """Returns a list of frames from a custom preset."""
    return frames_from_lists([
        [
            [[255, 255, 255], [255, 32 , 0  ], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
        ],[
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 32 , 0  ], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
            [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]
        ]
    ])

if __name__ == "__main__":
    gif_path = path.join(getcwd(), "test2")
    # Generate a random gif
    # gif = generate_random_gif(size["frames"], size["width"], size["height"])
    # print(gif)
    # gif = load_gif_to_frames(gif_path)
    
    # Save the gif
    save_frames_as_gif(get_custom_gif(), gif_path)

    # Load the gif
    gif = load_gif_to_frames(gif_path)
    print(gif)