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
  --version 3.0.0-2023-08 || exit $?
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_required.json \
  --version 3.0.0-2023-08 || exit $?
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_suggested.json \
  --version 3.0.0-2023-08 || exit $?
# Prior version(s):
# 2023-03
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_suggested-2023-03.json \
  --version 3.0.0-2023-03 || exit $?


# Validate B12 3.0.0 XYZ metadata
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_xyz_required.json \
  --version XYZ-3.0.0-2023-08 || exit $?
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_xyz_suggested.json \
  --version XYZ-3.0.0-2023-08 || exit $?
# Prior version(s):
# 2023-03
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_xyz_suggested-2023-03.json \
  --version XYZ-3.0.0-2023-03 || exit $?


# Validate B12 3.1.0
csbschema validate -f docs/IHO/b12_v3_1_0_example.json || exit $?
# Prior version(s):
# 2023-08
csbschema validate -f docs/IHO/b12_v3_1_0_example-2023-08.json \
  --version 3.1.0-2023-08 || exit $?
# 2023-03
csbschema validate -f docs/IHO/b12_v3_1_0_example-2023-03.json \
  --version 3.1.0-2023-03 || exit $?
# File expected to be invalid
csbschema validate -f docs/IHO/b12_v3_1_0_example-invalid.json
check_failed_as_expected

# Validate B12 3.1.0 XYZ metadata
csbschema validate -f docs/IHO/b12_v3_1_0_xyz_example.json \
  --version XYZ-3.1.0-2024-04 || exit $?
# Prior version(s):
# 2023-08
csbschema validate -f docs/IHO/b12_v3_1_0_xyz_example-2023-08.json \
  --version XYZ-3.1.0-2023-08 || exit $?
# File expected to be invalid
csbschema validate -f docs/IHO/b12_v3_1_0_xyz_example-invalid.json \
  --version XYZ-3.1.0-2023-08
check_failed_as_expected

# Run valid B12 3.0.0 against B12 3.1.0 - should fail (but clean)
csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_required.json --version 3.1.0-2024-04
check_failed_as_expected

exit 0
