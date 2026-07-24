import numpy as np


def vector_interp1(p1, p2, V1, V2, coord, dim):
    x1, y1 = p1
    x2, y2 = p2
    if dim == 1:
        if x2 == x1: # in case the denominator is 0
            return V1
        interp = (coord - x1)/(x2 - x1)
    elif dim == 2:
        if y2 == y1:
            return V1
        interp = (coord - y1)/(y2 - y1)
    else:
        return None
    V = [V1[i] + interp*(V2[i] - V1[i]) for i in range(len(V1))]
    return V


def t_shading(img, vertices, uv, textImg):
    edges = []
    for i in range(3):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % 3]
        if y1 == y2:
            continue
        if y1 < y2:
            y_min, y_max = y1, y2
            x = x1
            dx_dy = (x2 - x1) / (y2 - y1)
            i1, i2 = i, (i + 1) % 3 # store the vertices that define the specific edge
        else:
            y_min, y_max = y2, y1
            x = x2
            dx_dy = (x1 - x2) / (y1 - y2)
            i1, i2 = (i + 1) % 3, i
        edges.append([y_min, y_max, x, dx_dy, i1, i2]) # i1 is the index of the vertex with the lowest y-coordinate
    if len(edges) < 2: return img
    sorted_edges = sorted(edges, key=lambda e: e[0])
    y_min = int(min(e[0] for e in sorted_edges))
    y_max = int(max(e[1] for e in sorted_edges))

    active_edges = []
    h, w, _ = img.shape
    th, tw, _ = textImg.shape

    for y in range(y_min, y_max):
        for e in sorted_edges:
            if int(e[0]) == y:
                active_edges.append(e)
        active_edges = [e for e in active_edges if int(e[1]) != y]
        active_edges.sort(key=lambda e: e[2])
        for i in range(0, len(active_edges), 2):
            e1 = active_edges[i] # retrieve the edges to retrieve their vertices later
            e2 = active_edges[i + 1]
            x_start = int(np.ceil(e1[2]))
            x_end = int(np.floor(e2[2]))
            i1a, i1b = e1[4], e1[5] # retrieve the indices of the vertices of each active edge
            i2a, i2b = e2[4], e2[5]
            """
            calculate the normalized coordinates of points A & B (referring to the plot in the assignment instructions)
            through interpolation by using the normalized coordinates of the vertices.
            """
            v1 = vector_interp1(vertices[i1a], vertices[i1b], uv[i1a], uv[i1b], y, 2)
            v2 = vector_interp1(vertices[i2a], vertices[i2b], uv[i2a], uv[i2b], y, 2)
            for x in range(x_start, x_end + 1):
                # interpolation across the scanline for every point inbetween
                scanline_interp = vector_interp1((x_start, y), (x_end, y), v1, v2, x, 1)
                u, v = scanline_interp
                u = np.clip(u, 0.0, 1.0)
                v = np.clip(v, 0.0, 1.0)
                u = int(u * (tw - 1))
                v = int(v * (th - 1))
                if 0 <= x < w and 0 <= y < h:
                    if 0 <= u < tw and 0 <= v < th:
                        img[y, x] = textImg[v, u]
        for e in active_edges:
            e[2] += e[3]
    return img