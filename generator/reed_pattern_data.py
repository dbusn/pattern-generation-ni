from collections import namedtuple

static_pattern = namedtuple('static_pattern', 'phoneme total_time modulation fraction phi dis coord_list pho_freq')

reed_data = [
    static_pattern('B',  92, 30, 0.5, 0, 6, [[1,5],[1,6],[2,5],[2,6]], 300),
    static_pattern('M', 392, 8, 0.5, 0, 12,  [[1,5],[1,6],[2,5],[2,6]], 60),
    static_pattern('J', 392, 8, 0.5, 0, 12, [[1,1],[1,6],[2,1],[2,6]], 300),
    static_pattern('D',  92, 30, 0.5, 0, 6, [[3,3],[3,4],[4,3],[4,4]], 300),
    static_pattern('G',  92, 30, 0.5, 0, 6, [[1,1],[1,2],[2,1],[2,2]], 300),
    static_pattern('V', 392, 8, 0.5, 0, 12, [[1,6],[2,6],[3,6],[4,6]], 300),
    static_pattern('DH',392, 8, 0.5, 0, 12,[[1,3],[1,4],[2,3],[2,4]], 300),
    static_pattern('Z', 392, 8, 0.5, 0, 12, [[1,1],[2,1],[3,1],[4,1]], 300),
    static_pattern('ZH',392, 8, 0.5, 0, 12,[[3,1],[3,2],[4,1],[4,2]], 60),
    static_pattern('N', 392, 8, 0.5, 0, 12, [[3,3],[3,4],[4,3],[4,4]], 60),
    static_pattern('NG',392, 8, 0.5, 0, 12,[[1,1],[1,2],[2,1],[2,2]], 60),
    static_pattern('W', 392, 8, 0.5, 0, 12, [[1,3],[1,4],[1,5],[1,6],[3,3],[3,4],[3,5],[3,6]], 60),
    static_pattern('L', 392, 30, 0.5, 0, 12,[[3,5],[3,6],[4,5],[4,6]], 300),
    static_pattern('R', 392, 30, 0.5, 0, 12,[[3,1],[3,2],[4,1],[4,2]], 300),
]

# Type definitions
E = []
a = -1
d = -1
f = -1
g_f = -1
w = ''