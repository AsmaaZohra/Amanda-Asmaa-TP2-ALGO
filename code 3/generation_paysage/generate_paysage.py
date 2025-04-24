import numpy as np
from solid import *
from solid.utils import *

# -----------------------------
# baSe and matrix 
# -----------------------------
GRID_SIZE = 50  
MODEL_WIDTH = 70  # mm
MODEL_DEPTH = 60  # mm
MAX_HEIGHT = 40  # mm
ISLAND_RADIUS = GRID_SIZE // 3.6

#think gonna add trees and something else, the colors are not set it was just tot get an image. 

# -----------------------------
# Height Map 
# -----------------------------
def generate_height_map(size):
    center = (int(size * 0.45), int(size * 0.50))
    heights = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            dx = i - center[0]
            dy = j - center[1]

            # Distance with squashed radius for shape asymmetry
            dist = np.sqrt((dx / 1.1)**2 + (dy / 1.3)**2)

            #  randomness
            radius_variation = np.sin(i * 0.15) * 3 + np.cos(j * 0.1) * 2 + np.random.uniform(-2, 2)
            island_radius = ISLAND_RADIUS + radius_variation

            if dist < island_radius:
                
                radial_factor = 1 - dist / (ISLAND_RADIUS + 5)

                
                terrain_bump = (
                    np.sin(i * 0.2) * 0.6 +
                    np.cos(j * 0.25) * 0.4 +
                    np.random.uniform(-0.5, 0.5)
                )

                
                # Flatten peaks, keep gentle slope
                raw_elevation = (radial_factor + terrain_bump / 2) * MAX_HEIGHT

# Cap max elevation to avoid mountain peak
                elevation = min(raw_elevation, MAX_HEIGHT * 0.65)


                if radial_factor < 0.1:
                    elevation *= 2  # soften the outer slope even more

                heights[i, j] = max(0, elevation)


    return heights

def tile_as_triangle(x, y, z00, z01, z10, z11, tile_w, tile_d):
    # 4 corners of the square tile (with elevation)
    p0 = [x, y, z00]
    p1 = [x, y + tile_d, z01]
    p2 = [x + tile_w, y, z10]
    p3 = [x + tile_w, y + tile_d, z11]

    vertices = [p0, p1, p2, p3]

    # 2 triangles forming a quad (two triangle faces per square)
    faces = [
        [0, 1, 2],
        [1, 3, 2]
    ]

    return polyhedron(points=vertices, faces=faces)

# -----------------------------
# Island 
# -----------------------------
def generate_island(height_map):
    tile_w = MODEL_WIDTH / GRID_SIZE
    tile_d = MODEL_DEPTH / GRID_SIZE

    low_faces     = []
    lowmid_faces  = []
    mid_faces     = []
    midhigh_faces = []
    high_faces    = []

    for i in range(height_map.shape[0] - 1):
        for j in range(height_map.shape[1] - 1):
            z00 = height_map[i, j]
            z01 = height_map[i, j + 1]
            z10 = height_map[i + 1, j]
            z11 = height_map[i + 1, j + 1]

            avg_height = (z00 + z01 + z10 + z11) / 4

            if z00 == 0 and z01 == 0 and z10 == 0 and z11 == 0:
              continue

            # Shift tile upward by 1mm so it sits above the ocean base
            tile = tile_as_triangle(
                i * tile_w, j * tile_d,
                z00 + 0.7, z01 + 0.7, z10 + 0.7, z11 + 0.7,
                tile_w, tile_d
            )

            # Group tiles by height
            if avg_height < MAX_HEIGHT * 0.05:
                low_faces.append(tile)
            elif avg_height < MAX_HEIGHT * 0.15:
                lowmid_faces.append(tile)
            elif avg_height < MAX_HEIGHT * 0.20:
                mid_faces.append(tile)
            elif avg_height < MAX_HEIGHT * 0.35:
                midhigh_faces.append(tile)
            else:
                high_faces.append(tile)

    # Return terrain with grouped coloring
    return union()(
        color([0.6, 0.6, 0.4])(union()(*low_faces)),     # dark brown
        color([0.36, 0.25, 0.20])(union()(*lowmid_faces)),  # lighter brown
        color([0.45, 0.35, 0.25])(union()(*mid_faces)),        # khaki
        color([0.2, 0.4, 0.2])(union()(*midhigh_faces)),    # olive green
        color([0.13, 0.37, 0.13])(union()(*high_faces))     # dark forest green
    )


# -----------------------------
# ocean and Label
# -----------------------------
def generate_ocean_plate():
    
    base = color([0.0, 0.2, 0.4])(
        cube([MODEL_WIDTH, MODEL_DEPTH, 1], center=False)
    )

    # Label text
    label_text = linear_extrude(height=0.8)(
        text("AZS-AD IFT2125", size=5, halign="left", valign="baseline")
    )

   
    x_margin = 10
    y_position = MODEL_DEPTH - 5  # near the  edge

   
    label = translate([x_margin, y_position, -0.8])(
        rotate([180, 0, 0])(label_text)
    )

    return union()(base, label)

def smooth_height_map(height_map, passes=1):
    smoothed = height_map.copy()
    for _ in range(passes):
        new_map = smoothed.copy()
        for i in range(1, height_map.shape[0] - 1):
            for j in range(1, height_map.shape[1] - 1):
                region = smoothed[i-1:i+2, j-1:j+2]
                new_map[i, j] = np.mean(region)
        smoothed = new_map
    return smoothed

# -----------------------------
# model
# -----------------------------
def generate_model():
    height_map = generate_height_map(GRID_SIZE)
    height_map = smooth_height_map(height_map, passes=3)  # lissage, peut le modifier si on veut 
    base = generate_ocean_plate()
    island = generate_island(height_map)
    return union()(base, island)

# -----------------------------
# SCAD
# -----------------------------
if __name__ == "__main__":
    scad_render_to_file(generate_model(), 'model.scad', file_header='$fn = 50;')
