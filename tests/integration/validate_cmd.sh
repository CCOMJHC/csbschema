#!/bin/bash

function check_failed_as_expected () {
  if [[ $? -lt 1 ]]
  then
    echo "Command succeeded, but was expected to fail."
    exit 1
  fi
}


# Validate B12 3.0.0
csbschema validate -f docs/NOAA/example_csb_geojson_file.geojson \
  --version 3.0.0-2023-03 || exit $?
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_required.json \
  --version 3.0.0-2023-03 || exit $?
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_suggested.json \
  --version 3.0.0-2023-03 || exit $?


# Validate B12 3.0.0 XYZ metadata
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_xyz_required.json \
  --version XYZ-3.0.0-2023-03 || exit $?
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_xyz_suggested.json \
  --version XYZ-3.0.0-2023-03 || exit $?


# Validate B12 3.1.0
csbschema validate -f docs/IHO/b12_v3_1_0_example.json || exit $?


csbschema validate -f docs/IHO/b12_v3_1_0_example-invalid.json
check_failed_as_expected


# Validate B12 3.2.0-BETA
csbschema validate -f docs/IHO/b12_v3_2_0-BETA_example.json --version 3.2.0-BETA || exit $?


exit 0
