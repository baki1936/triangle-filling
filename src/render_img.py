import numpy as np
from . import flat_shading
from . import gouraud_shading
from . import texture_maps_shading


def render_img(faces, vertices, vcolors, uvs, depth, shading, textImg):
    """
    'faces': dimensions are (K, 3). It contains the vertices of K triangles.
    The i-th row contains the indices of the 3 vertices that define the i-th triangle
    with reference to the matrix 'vertices'.
    'vertices': dimensions are (L, 2). It contains the 2D coordinates of the L vertices.
    'vcolors': dimensions are (L, 3). It contains the colors of the L vertices.
    'depth': dimensions are (L,). It contains the depths of the L vertices.
    """

    M, N = 512, 512  # initialize canvas dimensions and white background
    img = np.ones((M, N, 3))

    depth = depth.reshape(-1)

    """
    Each triangle depth is the center of gravity of the depths of its vertices.
    In other words, it's the average of the depths of its vertices.
    'depth[faces]' returns an array of the same dimensions as 'faces', which are (K, 3).
    Each row contains the depths of the 3 vertices of the respective triangle.
    'depth[faces].mean(axis=1)' calculates the average depth of the vertices
    of each triangle (across rows). Therefore, the resulting dimensions are (K,).
    """
    triangle_depths = depth[faces].mean(axis=1)  # vectorized way, results in dimensions (K,)

    """
    negating array: the lowest elements become the highest and vice-versa.
    argsort(...) returns the indices of the triangle depths in descending order.
    """
    indices = np.argsort(-triangle_depths)

    """
    Go through triangle indices, from the triangle with the highest to the one with the lowest depth.
    
    """
    for i in indices:

        # dimensions: (1, 3), returns "#i" row of faces.
        # "face" has the indices of 3 vertices that make up triangle number #i.
        face = faces[i]

        # dimensions: (3, 2), contains the 2D coordinates of the three vertices that make up triangle number #i
        points = vertices[face]

        colors = vcolors[face]  # dimensions: (3, 3), contains the 3 color components per vertex.

        # dimensions: (3, 2), contains the normalized coordinates of the position of the texture image "textImg".
        uv = uvs[face]

        if shading == "f":
            img = flat_shading.f_shading(img, points, colors)

        elif shading == "g":
            img = gouraud_shading.g_shading(img, points, colors)

        elif shading == "t":
            img = texture_maps_shading.t_shading(img, points, uv, textImg)

        else:
            print("Unknown shading type")

    return img