This code loads .osm file and allows to call function on all OSM objects in dataset.

# Installation

`pip install osm-iterator`

Likely `pip3 install osm-iterator` if `pip` points to Python2 pip.

It is distributed as an `osm_iterator` PyPI package.

[![PyPI version](https://badge.fury.io/py/osm-iterator.svg)](https://badge.fury.io/py/osm-iterator)

# Usage example

## Download data and show it
This usage example includes downloading data using `requests` library, that you may need to install (also available via pip).
```
from osm_iterator import osm_iterator
import requests
import os.path

def download_from_overpass(query, output_filepath):
  print(query)
  url = "http://overpass-api.de/api/interpreter"
  r = requests.get(url, params={'data': query})
  result = r.text
  with open(output_filepath, 'w') as file:
      file.write(str(result))

def show_places(element):
    place_tag = element.get_tag_value("place")
    name_tag = element.get_tag_value("name")
    osm_object_url = element.get_link()
    if place_tag != None:
        print(name_tag, "(", place_tag, ") is ", osm_object_url)

filepath = "places_in_Kraków.osm"
query = """
[out:xml][timeout:2500];
area[name='Kraków']->.searchArea;
(
  node["place"](area.searchArea);
  way["place"](area.searchArea);
  relation["place"](area.searchArea);
);
out center;
"""

if os.path.isfile(filepath) == False:
    download_from_overpass(query, filepath)
osm = osm_iterator.Data(filepath)
osm.iterate_over_data(show_places)
```

## Load data only

```
from osm_iterator import osm_iterator

global osm_object_store
osm_object_store = []

def record_objects(element):
    global osm_object_store
    print(element.element.tag, element.element.attrib['id'])
    osm_object_store.append({"type": element.get_type(), "id": element.get_id()})

filepath = "output.osm"
osm = osm_iterator.Data(filepath)
osm.iterate_over_data(record_objects)
for entry in osm_object_store:
    print(entry)
```

# Running tests

```nosetests3``` or ```python3 -m unittest``` or ```python3 tests.py```

# History

Design explanation: this code has deeply suboptimal handling of pretty much everything. For start, all data is loaded into memory and then duplicated in-memory dataset is created.

As result, attempt to process any large datasets will cause issues due to excessive memory consumption.

This situation is consequence of following facts

* This code was written during my first attempt to process OSM data using Python
* API allows (at least in theory) to painlessly switch to real iterator that is not loading all data into memory at once
* So far this was good enough for my purposes so I had no motivation to spend time on improving something that is not a bottleneck

Though, if someone has good ideas for improvements (especially in form of a working code) - comments and pull requests are welcomed.

