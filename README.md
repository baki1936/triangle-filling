# Triangle Filling and Shading Algorithms

Implementation of a software rasterizer in Python featuring multiple triangle shading techniques based on the scanline algorithm.

The project renders a triangular mesh by sorting triangles according to their depth and rasterizing each triangle using one of the supported shading methods.

## Implemented Algorithms

- **Flat Shading** – Assigns a single color to the entire triangle using the average color of its vertices.
- **Gouraud Shading** – Linearly interpolates the vertex colors across the triangle using barycentric coordinates.
- **Texture Mapping** – Maps a texture image onto each triangle using UV coordinates and scanline interpolation.
- **Vector Interpolation** – Linear interpolation utility used during texture mapping.

## Rendering Pipeline

- Triangle mesh
- Compute triangle depths
- Sort triangles by depth
- Select shading method
  - Flat Shading
  - Gouraud Shading
  - Texture Mapping
- Scanline rasterization
- Rendered image

## Project Structure

- `src/flat_shading.py` – Scanline implementation of Flat Shading.
- `src/gouraud_shading.py` – Gouraud Shading using barycentric color interpolation.
- `src/texture_maps_shading.py` – Texture Mapping using UV interpolation across scanlines.
- `src/render_img.py` – Main rendering pipeline, triangle depth sorting, and shading dispatch.
- `demos/demo_f.py` – Demonstration of Flat Shading.
- `demos/demo_g.py` – Demonstration of Gouraud Shading.
- `demos/demo_t.py` – Demonstration of Texture Mapping.
- `data/` – Input mesh data and texture image.
- `results/` – Generated rendering results.
- `docs/` – Project documentation.

## Requirements

- Python 3.x
- NumPy
- OpenCV

Install the required packages:

```bash
pip install numpy opencv-python
```

## Running the Demos

Run the commands from the root directory of the repository.

Flat Shading:

```bash
python -m demos.demo_f
```

Gouraud Shading:

```bash
python -m demos.demo_g
```

Texture Mapping:

```bash
python -m demos.demo_t
```

The rendered images are saved in the `results/` directory:

- `results/flat_shading.png`
- `results/gouraud_shading.png`
- `results/texture_maps_shading.png`