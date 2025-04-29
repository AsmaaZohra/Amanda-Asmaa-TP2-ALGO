# Asmaa Zohra Skou et Amanda Dorval
import numpy as np
from solid import *
from solid.utils import *
import random

# -----------------------------
# Base Parameters
# -----------------------------
GRID_SIZE = 50  # grid size (50x50)
MODEL_WIDTH = 70  # in mm
MODEL_DEPTH = 60  # in mm
MAX_HEIGHT = 40   # maximum height in mm

# Radius of the two islands
ISLAND_RADIUS_LARGE = GRID_SIZE // 5
ISLAND_RADIUS_SMALL = GRID_SIZE // 7

# Centers of the two islands
ISLAND_CENTERS = [
    (int(GRID_SIZE * 0.35), int(GRID_SIZE * 0.5)),  # larger island center
    (int(GRID_SIZE * 0.6), int(GRID_SIZE * 0.5))    # smaller island center
]

# Lagoon center and its radius
LAGOON_CENTER = (int(GRID_SIZE * 0.42), int(GRID_SIZE * 0.52))
LAGOON_RADIUS = 5

# -----------------------------
# Generate Height Map (map + lagoon + rivers)
# -----------------------------
def generate_height_map(size):
    heights = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            elevation = 0
            # from each island
            for idx, center in enumerate(ISLAND_CENTERS):
                dx = i - center[0]
                dy = j - center[1]

                # slightly distorted distance for ellipsoidal shape
                if idx == 0:
                    dist = np.sqrt((dx / 1.2)**2 + (dy / 1.4)**2)
                    radius = ISLAND_RADIUS_LARGE
                    max_height = 15  # max height for large island
                else:
                    dist = np.sqrt((dx / 1.2)**2 + (dy / 1.2)**2)
                    radius = ISLAND_RADIUS_SMALL
                    max_height = 20  # max height for smaller island

                # Introduce slight random variation in radius
                radius_variation = np.random.uniform(-1.0, 1.0)
                adjusted_radius = radius + radius_variation

                if dist < adjusted_radius:
                    radial_factor = 1 - dist / (radius + 5)
                    # natural bumps
                    terrain_bump = (
                        np.sin(i * 0.15) * 0.4 +
                        np.cos(j * 0.2) * 0.4 +
                        np.random.uniform(-0.2, 0.2)
                    )
                    raw_elevation = (radial_factor + terrain_bump / 2) * max_height
                    elevation = max(elevation, min(raw_elevation, max_height * 0.65))

            # Bridge between islands 
            if (int(GRID_SIZE * 0.4) < i < int(GRID_SIZE * 0.55)) and (int(GRID_SIZE * 0.48) < j < int(GRID_SIZE * 0.52)):
                elevation = max(elevation, 0.5)

            # Lagoon depression
            dx_lagoon = i - LAGOON_CENTER[0]
            dy_lagoon = j - LAGOON_CENTER[1]
            dist_lagoon = np.sqrt(dx_lagoon**2 + dy_lagoon**2)
            if dist_lagoon < LAGOON_RADIUS:
                elevation = 0

            # River leading to the lagoon
            if (i < LAGOON_CENTER[0]) and (abs(j - LAGOON_CENTER[1]) < 2) and (LAGOON_CENTER[0] - i < 7):
                elevation = min(elevation, max(elevation, 3))

            heights[i, j] = max(0, elevation)  # final elevation
    return heights

# -----------------------------
# Generate a Tile (as two triangles)
# -----------------------------
def tile_as_triangle(x, y, z00, z01, z10, z11, tile_w, tile_d):
    # four points of the square
    p0 = [x, y, z00]
    p1 = [x, y + tile_d, z01]
    p2 = [x + tile_w, y, z10]
    p3 = [x + tile_w, y + tile_d, z11]
    vertices = [p0, p1, p2, p3]
    faces = [
        [0, 1, 2],  # first triangle
        [1, 3, 2]   # second triangle
    ]
    return polyhedron(points=vertices, faces=faces)

# -----------------------------
# Generate Island (terrain + forest)
# -----------------------------
def generate_island(height_map):
    tile_w = MODEL_WIDTH / GRID_SIZE
    tile_d = MODEL_DEPTH / GRID_SIZE

    low_faces = []
    lowmid_faces = []
    mid_faces = []
    midhigh_faces = []
    high_faces = []
    lagoon_faces = []
    vegetation_positions = []

    for i in range(height_map.shape[0] - 1):
        for j in range(height_map.shape[1] - 1):
            z00 = height_map[i, j]
            z01 = height_map[i, j + 1]
            z10 = height_map[i + 1, j]
            z11 = height_map[i + 1, j + 1]
            avg_height = (z00 + z01 + z10 + z11) / 4

            if (z00 == 0 and z01 == 0 and z10 == 0 and z11 == 0):
                continue  # skip ocean

            tile = tile_as_triangle(
                i * tile_w, j * tile_d,
                z00 + 0.7, z01 + 0.7, z10 + 0.7, z11 + 0.7,
                tile_w, tile_d
            )

            dx_lagoon = i - LAGOON_CENTER[0]
            dy_lagoon = j - LAGOON_CENTER[1]
            dist_lagoon = np.sqrt(dx_lagoon**2 + dy_lagoon**2)

            if dist_lagoon < LAGOON_RADIUS + 1:
                lagoon_faces.append(tile)  # lagoon color zone
            elif avg_height < MAX_HEIGHT * 0.05:
                low_faces.append(tile)  # light blue transition
            elif avg_height < MAX_HEIGHT * 0.15:
                lowmid_faces.append(tile)  # low lands 
            elif avg_height < MAX_HEIGHT * 0.20:
                mid_faces.append(tile)  # mid-slopes
            elif avg_height < MAX_HEIGHT * 0.35:
                midhigh_faces.append(tile)  # high slopes 
                vegetation_positions.append((i, j))
            else:
                high_faces.append(tile)  # mountain tops 
                vegetation_positions.append((i, j))

    # Generate trees on high vegetation areas
    trees = []
    random.seed(42)
    sampled_positions = random.sample(vegetation_positions, min(35, len(vegetation_positions)))

    for (i, j) in sampled_positions:
        x = i * tile_w
        y = j * tile_d
        z = height_map[i, j] + 0.7

        # Tree made of trunk and leaves
        tree = translate([x, y, z])(
            union()(
                color([0.2, 0.05, 0.08])(cylinder(r=0.15, h=1.2)),  # trunk 
                translate([0, 0, 1.2])(color([0.31, 0.6, 0.0])(sphere(r=0.7)))  # leaves 
            )
        )
        trees.append(tree)

    return union()(
        color([0.3, 0.6, 0.9])(union()(*lagoon_faces)),    # lagoon -- blue tone
        color([0.5, 0.79, 0.85])(union()(*low_faces)),     # shallow area -- light cyan-blue
        color([0.36, 0.20, 0.20])(union()(*lowmid_faces)), # lower slopes -- dark brown
        color([0.2, 0.31, 0.25])(union()(*mid_faces)),     # mid-level slopes -- dark green-gray
        color([0.2, 0.4, 0.2])(union()(*midhigh_faces)),   # high-level slopes -- medium dark green
        color([0.13, 0.37, 0.13])(union()(*high_faces)),   # peaks and top areas -- very dark forest green
        union()(*trees)                                   # trees (forest)
    )

# -----------------------------
# Generate Ocean Plate (with waves)
# -----------------------------
def generate_ocean_plate():
    tile_w = MODEL_WIDTH / GRID_SIZE
    tile_d = MODEL_DEPTH / GRID_SIZE

    ocean_faces = []
    for i in range(GRID_SIZE - 1):
        for j in range(GRID_SIZE - 1):
            wave_height = 0.3 * np.sin(i * 0.2) * np.cos(j * 0.2)  # add wave effect
            base_height = 1 + wave_height

            blue_shade = 0.7 + 0.1 * np.sin(i * 0.3 + j * 0.3)
            blue_shade = min(max(0.6, blue_shade), 0.9)
            color_variation = [0.0, 0.4 + 0.1 * np.sin(j * 0.2), blue_shade]

            tile = color(color_variation)(
                tile_as_triangle(
                    i * tile_w, j * tile_d,
                    base_height, base_height, base_height, base_height,
                    tile_w, tile_d
                )
            )
            ocean_faces.append(tile)

    # Text label below the model
    label_text = linear_extrude(height=0.2)(
        text("AZS-AD IFT2125", size=5, halign="left", valign="baseline")
    )
    label = translate([7, MODEL_DEPTH - 5, 0.6])(rotate([180, 0, 0])(label_text))

    return union()(ocean_faces, label)

# -----------------------------
# Smooth Height Map (apply smoothing over the terrain)
# -----------------------------
def smooth_height_map(height_map, passes=3):
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
# Generate Full Model (terrain + lagoon + ocean)
# -----------------------------
def generate_model():
    height_map = generate_height_map(GRID_SIZE)
    height_map = smooth_height_map(height_map, passes=3)
    ocean = generate_ocean_plate()
    island = generate_island(height_map)
    return union()(ocean, island)

# -----------------------------
# Export to SCAD
# -----------------------------
if __name__ == "__main__":
    scad_render_to_file(generate_model(), 'model.scad', file_header='$fn = 50;')
