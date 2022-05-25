from pathlib import Path
import h5py
import numpy as np
from skimage.transform import resize

def preprocess(path_file: Path):
    (Path("temp_files") / path_file.stem).mkdir(exist_ok=True, parents=True)
    (Path("images") / path_file.stem).mkdir(exist_ok=True, parents=True)

    with h5py.File(path_file, "r") as hdf_file:
        bands = [
            "IMG_MIR",
            "IMG_SWIR",
            "IMG_TIR1",
            "IMG_TIR2",
            "IMG_VIS",
            "IMG_WV",
        ]

        variants = [
            "ALBEDO",
            "RADIANCE",
            "TEMP",
        ]

        for band in bands:
            arr = np.array(hdf_file[band][0])

            for variant in variants:
                title = f"{band}_{variant}"

                if title not in hdf_file:
                    continue

                arr_replace = np.array(hdf_file[title])

                arr_replace = arr_replace - arr_replace.min()
                arr_replace = arr_replace * (255 / arr_replace.max())

                # https://stackoverflow.com/questions/8188726/how-do-i-do-this-array-lookup-replace-with-numpy
                arr_variant = arr_replace[arr]

                if band in ["IMG_SWIR", "IMG_VIS"]:
                    arr_variant = resize(arr_variant, (2816, 2805))

                arr_variant = arr_variant.astype(np.uint8)
                
                np.save(Path("temp_files") / path_file.stem / f"{band}_{variant}.npy", arr_variant)



if __name__ == '__main__':
    for child in Path("./raw_data/").iterdir():
        if child.is_file() and child.suffix == ".h5":
            print(child)
            preprocess(child)