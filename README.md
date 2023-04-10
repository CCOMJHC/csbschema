![example workflow](https://github.com/CCOMJHC/csbschema/actions/workflows/flake8-and-unit-tests.yml/badge.svg)

# csbschema

`csbschema` defines a JSON Schema and validator (implemented in Pyhon) for 
[IHO B-12 Crowdsourced Bathymetry](https://iho.int/uploads/user/pubs/Drafts/CSB-Guidance_Document-Edition_3.0.pdf) 
metadata and data.

# Installation
Clone or download this repository, then run:
```shell
$ pip install .
```

# Usage

## Convention GeoJSON CSB 3.1
JSON files conforming to [GeoJSON CSB 3.0.0 metadata](docs/IHO/CSB-Guidance_Document-Edition_3.0.pdf)
can be validated using the 3.1.0-2023-03 [schema](csbschema/data/CSB-schema-3_1_0-2023-03.json)
(e.g., convention 'GeoJSON CSB 3.1'):
```shell
$ csbschema validate -f docs/IHO/b12_v3_1_0_example.json
CSB data file 'docs/IHO/b12_v3_1_0_example.json' successfully validated against schema '3.1.0-2023-03'.
```

Validating an invalid document will show where in the document errors were be found:
```shell
$ csbschema validate -f docs/IHO/b12_v3_1_0_example-invalid.json 
Validation of docs/IHO/b12_v3_1_0_example-invalid.json against schema 3.1.0-2023-03 failed due to the following errors: 
Path: /properties/trustedNode/convention, error: 'GeoJSON CSB 3.0' is not one of ['GeoJSON CSB 3.1']
Path: /features/1/properties, error: 'depth' is a required property
Path: /features/3/properties, error: 'time' is a required property
Path: /features/4/properties/time, error: '2016-03-03 18:41:49Z' does not match '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)([.][0-9]+)?[Zz]$'
Path: /properties/platform/IDNumber, error: IDNumber IMO3699580 is not valid for IDType MMSI.
Path: /properties/platform/dataProcessed, error: dataProcessed flag is 'false', but 'processing' properties were found.
Path: /properties/platform/uniqueID, error: uniqueID: SEAID-45f5c322-10f2-4946-802e-d5992ad36727 does not match /properties/trustedNode/uniqueVesselID: SEAID-e8c469f8-df38-11e5-b86d-9a79f06e9478
```

## Conventions GeoJSON CSB 3.0 and XYZ CSB 3.0
A schema for the provisional JSON encoding of B12 3.0.0 data and metadata (e.g., convention 'GeoJSON CSB 3.0') is 
available under the schema name '3.0.0-2023-03':
```shell
$ csbschema validate -f docs/NOAA/example_csb_geojson_file.geojson --version 3.0.0-2023-03
```

Similarly, a metadata-only schema (e.g., convention 'XYZ CSB 3.0') is available under the schema name 
'XYZ-3.0.0-2023-03':
```shell
$ csbschema validate -f docs/NOAA/noaa_b12_v3_0_0_xyz_required.json --version XYZ-3.0.0-2023-03
```

The metadata-only 'XYZ schema' is meant to be used for JSON metadata supplied alongside CSB data in CSV or another 
format.

## Convention GeoJSON CSB 3.2
A schema for a beta JSON encoding of B12 3.0.0 (e.g., convention 'GeoJSON CSB 3.2') is available under the schema
name '3.2.0-BETA':
```shell
$ csbschema validate -f docs/IHO/b12_v3_2_0-BETA_example.json --version 3.2.0-BETA
CSB data file 'docs/IHO/b12_v3_2_0-BETA_example.json' successfully validated against schema '3.2.0-BETA'.
```
> Run `csbschema validate --help` for more information about validating against different versions of the schema.

# Testing
First, install csbschema with test dependencies:
```shell
$ pip install ".[test]"
```

Then run unit tests:
```shell
$ pytest tests/unit/test_*.py
```

Run integration tests, which tests running the `csbschema validate` command line tool for many of the example
CSB documents found in the `csbschema` repository:
```shell
$ bash tests/integration/validate_cmd.sh
```
