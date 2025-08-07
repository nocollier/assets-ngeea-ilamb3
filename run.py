"""
A driver script for ilamb3 that builds up data registries (dataframes) and then
runs a configure file.
"""

import sys
from pathlib import Path

import ilamb3
import ilamb3.regions as ilr
from ilamb3.meta import generate_dashboard_page
from ilamb3.run import run_study

import database as dbase

# Reference data
df_ref = dbase.dataframe_reference()

# Model data
df_com = dbase.dataframe_e3sm()

# Setups up the regions and options we will use
ilamb_regions = ilr.Regions()
ilamb_regions.add_latlon_bounds("arctic", "Arctic", [66.5, 90], [-180, 180])
ilamb3.conf.set(
    regions=[None],
    use_cached_results=False,
    model_name_facets=["model"],
    comparison_groupby=["model"],
    shift_years=1711,
)

# Run study
yml_file = sys.argv[1] if len(sys.argv) == 2 else "standard.yaml"
build_dir = Path(f"_build_{yml_file.replace(".yaml","")}")
run_study(yml_file, df_com, ref_datasets=df_ref, output_path=build_dir)
generate_dashboard_page(build_dir, page_title="NGEE-Arctic ILAMB Results")
