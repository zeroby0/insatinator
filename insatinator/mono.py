from pathlib import Path
import numpy as np
from PIL import Image as im

def mono(path_data: Path):
    for child in path_data.iterdir():
        if child.is_file() and child.suffix == ".npy":
            print(child)
            
            arr_variant = np.load(child)

            data = im.fromarray(arr_variant)
            data.save(f"images/{path_data.stem}/{child.stem}.png")

if __name__ == '__main__':
    for child in Path("temp_files").iterdir():
        if child.is_dir():
            print(child)
            mono(child)