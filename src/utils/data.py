import pandas as pd
import numpy as np

def load_tsp_file(filepath):
    """
    Load a .tsp file and convert it into a pandas DataFrame.

    This function processes .tsp files from the TSPLIB project, specifically for 2D maps.
    """
    with open(filepath) as file:
        node_section_index = None
        city_count = None
        file_lines = file.readlines()

        # Extract metadata from the .tsp file
        index = 0
        while not city_count or not node_section_index:
            current_line = file_lines[index]
            if current_line.startswith('DIMENSION :'):
                city_count = int(current_line.split()[-1])
            if current_line.startswith('NODE_COORD_SECTION'):
                node_section_index = index
            index += 1

        print(f'Read problem containing {city_count} cities.')

        file.seek(0)

        # Parse the coordinates into a DataFrame
        cities_df = pd.read_csv(
            file,
            skiprows=node_section_index + 1,
            delim_whitespace=True,
            names=['city', 'x', 'y'],
            dtype={'city': str, 'x': np.float64, 'y': np.float64},
            header=None,
            nrows=city_count
        )

        return cities_df

def normalize_coordinates(coords):
    """
    Normalize a set of points.

    This function adjusts the offset of an n-dimensional array and scales it to fit within 
    a proportional range of [0,1] for the y-axis, preserving the original x-axis ratio.
    """
    scale_ratio = (coords.x.max() - coords.x.min()) / (coords.y.max() - coords.y.min()), 1
    scale_ratio = np.array(scale_ratio) / max(scale_ratio)
    normalized = coords.apply(lambda column: (column - column.min()) / (column.max() - column.min()))
    return normalized.apply(lambda point: scale_ratio * point, axis=1)
