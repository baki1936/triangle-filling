import numpy as np


def triangle_area(p1, p2, p3):
    """
    p1, p2 and p3: points in 2D space and should be
    tuples or lists in the format (x, y).
    The function calculates the area of a triangle
    using the coordinates of its vertices
    (shoelace formula).
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    return area


def drawpixel(img, vertices, vcolors, p, area):
    """
    Calculates the color c = (R, G, B) on point p
    inside the triangle defined by the given vertices,
    using the colors (vectors with 3 elements) of each vertex
    in vcolors and changes the value of img on point p.
    """
    if area == 0:
        return None
    h, w, _ = img.shape
    w0 = triangle_area(p, vertices[1], vertices[2]) / area
    w1 = triangle_area(vertices[0], p, vertices[2]) / area
    w2 = triangle_area(vertices[0], vertices[1], p) / area
    if 0 <= p[0] < w and 0 <= p[1] < h:
        img[p[1], p[0]] = w0 * vcolors[0] + w1 * vcolors[1] + w2 * vcolors[2]
    return None


def g_shading(img, vertices, vcolors):
    edges = []
    for i in range(3):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % 3]
        if y1 == y2:  # ignore horizontal edges
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

    """
    sorted in conjunction with anonymous function
    as value to the key argument sorts list of lists
    by the first element in each sublist (by y_min).
    """

    if len(edges) < 2: return img

    edges = sorted(edges, key=lambda e: e[0])
    y_min = int(min(e[0] for e in edges))  # finds the minimum of the first elements of all 3 sublists
    y_max = int(max(e[1] for e in edges))

    active_edges = []
    area = triangle_area(vertices[0], vertices[1], vertices[2])

    for y in range(y_min, y_max):  # do not include y_max to avoid filling a vertex twice
        for e in edges:
            if int(e[0]) == y:  # add every edge that has y_min (first element of every row) equal to y to active_edges
                active_edges.append(e)
        active_edges = [e for e in active_edges if int(e[1]) != y]  # remove the edges for whom y_max = y
        active_edges.sort(key=lambda e: e[2])  # sort by x of the lowest vertex of every edge
        for i in range(0, len(active_edges), 2):
            x_start = int(np.ceil(active_edges[i][2]))
            x_end = int(np.floor(active_edges[i + 1][2]))
            for x in range(x_start, x_end + 1):
                drawpixel(img, vertices, vcolors, (x, y), area)
        for e in active_edges:  # update x using dx_dy
            e[2] += e[3]
    return img