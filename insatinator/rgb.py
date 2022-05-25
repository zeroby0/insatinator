from pathlib import Path
import numpy as np
from PIL import Image as im

bands = ["IMG_MIR", "IMG_SWIR", "IMG_TIR1", "IMG_TIR2", "IMG_VIS", "IMG_WV"]
variants = ["ALBEDO", "RADIANCE", "TEMP"]


def rgb(path_data: Path):
    arr_r = np.load(path_data / "IMG_VIS_RADIANCE.npy")
    arr_g = np.load(path_data / "IMG_SWIR_RADIANCE.npy")
    arr_b = np.load(path_data / "IMG_MIR_RADIANCE.npy")

    arr_rgb = np.array(
        [
            arr_r.flatten(),
            arr_g.flatten(),
            arr_b.flatten(),
        ]
    )

    arr_rgb = arr_rgb.T.reshape((2816, 2805, 3))

    data = im.fromarray(arr_rgb)
    data.save(f"images/{path_data.stem}/rgb.png")


if __name__ == "__main__":
    for child in Path("temp_files").iterdir():
        if child.is_dir():
            print(child)
            rgb(child)
