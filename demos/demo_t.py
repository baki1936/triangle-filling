import numpy as np
import cv2
from src.render_img import render_img
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
image1 = cv2.imread(
    str(ROOT / "data" / "loony-repeat.png")
)

if image1 is None:
    raise FileNotFoundError("Could not load data/loony-repeat.png")

image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
image1 = image1.astype(np.float64) / 255.0

data = np.load(ROOT / "data" / "hw1.npy",
               allow_pickle=True).item()

vertices = data["v_pos2d"]
uvs = data["v_uvs"]
vcolors = data["v_clr"]
faces = data["t_pos_idx"]
depth = data["depth"]

image2 = render_img(faces, vertices, vcolors, uvs, depth, "t", image1)

image2 = (image2 * 255).astype(np.uint8) # modify range of from [0, 1] to [0, 255] (unsigned 8-bit integer)
image2 = cv2.cvtColor(image2, cv2.COLOR_RGB2BGR) # show BGR color

cv2.imshow("image", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(
    str(ROOT / "results" / "texture_maps_shading.png"),
    image2
)