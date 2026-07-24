import numpy as np
import cv2
import render_img
import trimesh

data = np.load("hw1.npy", allow_pickle=True).item()

vertices = data["v_pos2d"]
uvs = data["v_uvs"]
vcolors = data["v_clr"]
faces = data["t_pos_idx"]
depth = data["depth"]

image2 = render_img.render_img(faces, vertices, vcolors, uvs, depth, "g", None)

image2 = (image2 * 255).astype(np.uint8) # modify range of from [0, 1] to [0, 255] (unsigned 8-bit integer)
image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR) # show BGR color

cv2.imshow("image", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("gouraud_shading.png", image2)