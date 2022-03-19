import json
import sys
import gifutils

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        json_pattern = json.load(f)

    iters = [iteration["iteration"] for iteration in json_pattern["pattern"]]
    grids = [
        [[[255, 255, 255] for _ in range(0, 4)] for _ in range(0, 6)]
        for _ in range(0, len(iters))
    ]

    for i, iteration in enumerate(iters):
        for iter in iteration:
            col_coord = int(str(iter["coord"])[0])
            row_coord = int(str(iter["coord"])[1])
            amp = iter["amplitude"]
            grids[i][row_coord - 1][col_coord - 1] = [amp, amp, amp]

    gifutils.save_frames_as_gif(
        gifutils.frames_from_lists(grids), "gifs", sys.argv[1].split(".")[0]
    )