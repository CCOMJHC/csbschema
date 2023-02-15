# csbschema

`csbschema` defines a JSON Schema and validator (implemented in Pyhon) for 
[IHO B-12 Crowdsourced Bathymetry](https://iho.int/uploads/user/pubs/Drafts/CSB-Guidance_Document-Edition_3.0.pdf) 
metadata and data.

# Installation
Clone or download this repository, then run:
```shell
pip install .
```

# Usage
JSON files conforming to [GeoJSON CSB 3.0.0 metadata](docs/IHO/CSB-Guidance_Document-Edition_3.0.pdf) 
can be validated using the [CSB 3.0.0 schema](csbschema/data/CSB-schema-3_0_0-2023-02.json):
```shell
$ csbschema validate -f docs/IHO/b12_v3_example.json
CSB data file 'docs/IHO/b12_v3_example.json' successfully validated against schema '3.0.0-2023-02'.
```

Validating an invalid document will show where in the document errors were be found:
```shell
$ csbschema validate -f docs/IHO/b12_v3_example-invalid.json 
Validation of docs/IHO/b12_v3_example-invalid.json against schema 3.0.0-2023-02 failed due to the following errors: 
Path: /features/1/properties, error: 'depth' is a required property
Path: /features/3/properties, error: 'time' is a required property
Path: /features/4/properties/time, error: '2016-03-03 18:41:49Z' does not match '^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)([.][0-9]+)?[Zz]$'
Path: /properties/platform/IDNumber, error: IDNumber IMO3699580 is not valid for IDType MMSI.
Path: /properties/platform/dataProcessed, error: dataProcessed flag is 'false', but 'processing' properties were found.
```

> Note: A schema for a provisional JSON encoding of B12 version 3.0.0 is available under the version `3.0.0-2022-12`.
> Run `csbschema validate --help` for more information about validating against different versions of the schema.

# Testing
First, install csbschema with test dependencies:
```shell
pip install ".[test]"
```

Then run tests:
```shell
pytest tests/unit/test_*.py
```
