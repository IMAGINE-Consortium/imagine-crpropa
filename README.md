# IMAGINE and CRPropa integration

*This package is still under development*

This package provides interfaces between [CRPropa](https://crpropa.desy.de/)
and [IMAGINE pipeline](https://github.com/IMAGINE-Consortium/imagine/).

First and foremost, it allows using CRPropa as an IMAGINE [Simulator](https://imagine-code.readthedocs.io/en/latest/components.html#simulators), which can take
IMAGINE Fields as input and can also be included in a [Pipeline](https://imagine-code.readthedocs.io/en/latest/components.html#pipeline) object. 

The package also provides IMAGINE [Fields](https://imagine-code.readthedocs.io/en/latest/components.html#fields)
which wrap around magnetic field models originally developed for use within CRPropa
which may have other uses by the IMAGINE community.

## Installation

1. Install [CRPropa](https://crpropa.github.io/CRPropa3/pages/Installation.html)
and [IMAGINE](https://imagine-code.readthedocs.io/en/latest/installation.html).
2. Clone this repository or download the desired [release](https://github.com/IMAGINE-Consortium/imagine-crpropa/releases)
3. Install it as a regular python package, running:

```console
cd PATH_TO_IMAGINE-CRPROPA
pip install -e .
```
## Usage

### CRPropaSimulator


### CRPropa Fields
