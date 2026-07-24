import numpy as np


def f_shading(img, vertices, vcolors):
    edges = []
    for i in range(3):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % 3]
        if y1 == y2: # ignore horizontal edges
            continue
        if y1 < y2:
            y_min, y_max = y1, y2
            x = x1
            dx_dy = (x2 - x1) / (y2 - y1)
        else:
            y_min, y_max = y2, y1
            x = x2
            dx_dy = (x1 - x2) / (y1 - y2)
        edges.append([y_min, y_max, x, dx_dy])

    if len(edges) < 2: return img # in case the triangle is degenerate

    """
    sorted in conjunction with anonymous function
    as value to the key argument sorts list of lists
    by the first element in each sublist (by y_min).
    """

    edges = sorted(edges, key=lambda e: e[0])
    y_min = int(min(e[0] for e in edges))  # finds the minimum of the first elements of all 3 sublists
    y_max = int(max(e[1] for e in edges))

    active_edges = []
    h, w, _ = img.shape # get img dimensions

    for y in range(y_min, y_max):  # do not include y_max to avoid filling a vertex twice
        for e in edges:
            if int(e[0]) == y:  # add every edge that has y_min equal to y to active_edges
                active_edges.append(e)
        active_edges = [e for e in active_edges if int(e[1]) != y]  # remove the edges for whom y_max = y
        active_edges.sort(key=lambda e: e[2])  # sort by x of the lowest vertex of every edge
        for i in range(0, len(active_edges), 2):
            x_start = int(np.ceil(active_edges[i][2]))
            x_end = int(np.floor(active_edges[i + 1][2]))
            if 0 <= y < h: # ensure we are not out of bounds
                for x in range(x_start, x_end + 1):
                    if 0 <= x < w:
                        img[y, x] = (vcolors[0] + vcolors[1] + vcolors[2]) / 3
        for e in active_edges:  # update x using dx_dy
            e[2] += e[3]
    return img