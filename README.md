This code loads .osm file and allows to call function on all OSM objects in dataset.

# Installation

`pip install osm-iterator`

It is distributed as an `osm_iterator` PyPI package.

[![PyPI version](https://badge.fury.io/py/osm-iterator.svg)](https://badge.fury.io/py/osm-iterator)

# Usage example

```
from osm_iterator.osm_iterator import Data

def show_places(element):
    place_tag = element.get_tag_value("place")
    name_tag = element.get_tag_value("name")
    osm_object_url = element.get_link()
    if place_tag != None:
        print(name_tag, "is an object", osm_object_url)

osm = Data("file.osm")
osm.iterate_over_data(show_places)
```

# Running tests

```nosetests3``` or ```python3 -m unittest```

# History

Design explanation: this code has deeply suboptimal handling of pretty much everything. For start, all data is loaded into memory and then duplicated in-memory dataset is created.

As result, attempt to process any large datasets will cause issues due to excessive memory consumption.

This situation is consequence of following facts

* This code was written during my first attempt to process OSM data using Python
* API allows (at least in theory) to painlessly switch to real iterator that is not loading all data into memory at once
* So far this was good enough for my purposes so I had no motivation to spend time on improving something that is not a bottleneck

Though, if someone has good ideas for improvements (especially in form of a working code) - comments and pull requests are welcomed.

