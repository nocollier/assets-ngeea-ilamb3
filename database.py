"""
Functions which build small databases which ilamb3 will use.
"""

from pathlib import Path

import pandas as pd


def dataframe_e3sm(
    root: Path = Path("/lustre/orion/cli137/world-shared/ESGF-data/CMIP6"),
    cache_file: Path = Path("df_cmip.csv"),
) -> pd.DataFrame:
    if cache_file.exists():
        df = pd.read_csv(cache_file)
        return df
    df = []
    for dirpath, _, files in root.walk():
        for fname in files:
            if not fname.endswith(".nc"):
                continue
            path = str((dirpath / fname).absolute())
            df.append(
                {
                    "mip_era": path.split("/")[-11],
                    "activity_id": path.split("/")[-10],
                    "institution_id": path.split("/")[-9],
                    "source_id": path.split("/")[-8],
                    "experiment_id": path.split("/")[-7],
                    "member_id": path.split("/")[-6],
                    "table_id": path.split("/")[-5],
                    "variable_id": path.split("/")[-4],
                    "grid_label": path.split("/")[-3],
                    "path": path,
                }
            )
    df = pd.DataFrame(df)
    df.to_csv(cache_file, index=False)
    return df


def dataframe_reference(
    root: Path = Path(
        "/lustre/orion/world-shared/cli138/deeksha/ILAMB-Hydro/Data/Reference"
    ),
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
