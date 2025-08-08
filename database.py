"""
Functions which build small databases which ilamb3 will use.
"""

import re
import warnings
from pathlib import Path

import pandas as pd
import xarray as xr

warnings.simplefilter("ignore", category=xr.SerializationWarning)

# Used to parse out CV from the filenames, example filename:
# ELMngee4_TFSmeq2_ERA5daymet_AK-TFSG_ICB1850CNRDCTCBC_ad_spinup.elm.h0.0201-01-01-00000.nc
E3SM_FILENAME_PATTERN = r"(?P<activity>[^_]*)_(?P<question>[^_]*)_(?P<forcing>[^_]*)_(?P<location>[^_]*)_(?P<casename>[^.]*)\.(?P<model>[^.]*)\.(?P<output_type>[^.]*)\.(?P<timestamp>[^.]*)\.nc"


def dataframe_e3sm(
    root: Path = Path("/gpfs/wolf2/cades/cli185/proj-shared/f9y/archives/elm_ngee4/"),
    cache_file: Path = Path("df_e3sm.csv"),
) -> pd.DataFrame:
    if cache_file.exists():
        df = pd.read_csv(cache_file)
        return df
    df = []
    for dirpath, _, files in root.walk():
        for fname in files:
            m = re.match(E3SM_FILENAME_PATTERN, fname)
            if not m:
                continue
            row = m.groupdict()
            path = str((dirpath / fname).absolute())
            ds = xr.open_dataset(path, decode_timedelta=False, decode_times=False)
            df += [
                dict(**row, variable_id=v, path=path)
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
