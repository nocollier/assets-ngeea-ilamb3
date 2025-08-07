"""
Functions which build small databases which ilamb3 will use.
"""

from pathlib import Path

import pandas as pd
import xarray as xr


def dataframe_e3sm(
    root: Path = Path(
        "/gpfs/wolf2/cades/cli185/proj-shared/f9y/archives/elm_ngee4/ELMngee4_TFSmeq2_ERA5daymet_AK-TFSG_ICB1850CNPRDCTCBC/run/"
    ),
    cache_file: Path = Path("df_e3sm.csv"),
) -> pd.DataFrame:
    if cache_file.exists():
        df = pd.read_csv(cache_file)
        return df
    df = []
    for dirpath, _, files in root.walk():
        for fname in files:
            if not fname.endswith(".nc"):
                continue
            if ".h0." not in fname:
                continue
            path = str((dirpath / fname).absolute())
            ds = xr.open_dataset(path)
            tokens = fname.split("_")
            df += [
                {
                    "model": tokens[0],
                    "question": tokens[1],
                    "forcing": tokens[2],
                    "location": tokens[3],
                    "variable_id": v,
                    "path": path,
                }
                for v in ds
                if "time" in ds[v].dims
            ]

    df = pd.DataFrame(df)
    df.to_csv(cache_file, index=False)
    return df


def dataframe_reference(
    root: Path = Path("/ccsopen/proj/cli185/ilamb-work/reference-data/"),
    cache_file: Path = Path("df_reference.csv"),
) -> pd.DataFrame:
    if cache_file.exists():
        df = pd.read_csv(cache_file)
        df = df.set_index("key")
        return df
    df = []
    for dirpath, _, files in root.walk():
        for fname in files:
            if not fname.endswith(".nc"):
                continue
            path = str((dirpath / fname).absolute())
            df.append(
                {
                    "key": fname,
                    "path": path,
                }
            )
    df = pd.DataFrame(df)
    df.to_csv(cache_file, index=False)
    df = df.set_index("key")
    return df
