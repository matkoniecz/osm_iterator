﻿# coding=utf-8

from lxml import etree
import decimal

"""
usage:

from osm_iterator.osm_iterator import Data

def show_places(element):
    place_tag = element.get_tag_value("place")
    name_tag = element.get_tag_value("name")
    osm_object_url = element.get_link()
    if place_tag != None:
        print(name_tag + " is an object " + osm_object_url)

osm = Data("file.osm")
osm.iterate_over_data(show_places)

"""
class Coord:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Element(etree._Element):
    def __init__(self, element, data):
        self.element = element
        self.data = data

    def get_element(self):
        return self.element
    
    def get_tag_value(self, querried_tag):
        for tag in self.element:
            if tag.tag != "tag":
                continue
            if tag.attrib['k'] == querried_tag:
                return tag.attrib['v']
        return None

    def get_keys(self):
        returned = []
        for tag in self.element:
            if tag.tag != "tag":
                continue
            returned += [tag.attrib['k']]
        return returned

    def get_coords(self):
        if self.element.tag == "node":
            lat = float(self.element.attrib['lat'])
            lon = float(self.element.attrib['lon'])
            return Coord(lat, lon)
        return self.data.get_coords_of_complex_object(self.element)

    def get_link(self):
        return ("http://www.openstreetmap.org/" + self.element.tag + "/" + self.element.attrib['id'])

class Data(object):
    def __init__(self, filename_with_osm_data):
        self.data = etree.parse(filename_with_osm_data)
        self.node_database = {}
        self.way_database = {}

    def get_coords_of_object_in_database(self, id, database):
        try:
            if database[id] is None:
                raise KeyError
        except KeyError:
            return None, None  # node outside of downloaded map
        lat = database[id].lat
        lon = database[id].lon
        return lat, lon

    def get_coords_of_complex_object(self, element):
        min_lat = 180
        max_lat = -180
        min_lon = 180
        max_lon = -180
        if element.tag != "way" and element.tag != "relation":
            raise ValueError("Not a proper element passed to get_coords_of_complex_object")
        for tag in element:
            if (tag.tag == "nd") or (tag.tag == "member" and tag.attrib['type'] == "node"):
                node_id = int(tag.attrib['ref'])
                lat, lon = self.get_coords_of_object_in_database(node_id, self.node_database)
                if lat == None:
                    return None
            elif tag.tag == "member" and tag.attrib['type'] == "way":
                way_id = int(tag.attrib['ref'])
                lat, lon = self.get_coords_of_object_in_database(way_id, self.way_database)
                if lat == None:
                    return None
            else:
                continue
            min_lat = min([min_lat, lat])
            max_lat = max([max_lat, lat])
            min_lon = min([min_lon, lon])
            max_lon = max([max_lon, lon])
        return Coord((min_lat + max_lat) / 2, (min_lon + max_lon) / 2)


    def iterate_over_data(self, fun):
        for element in self.data.getiterator():
            if element.tag != "node" and element.tag != "way" and element.tag != "relation":
                continue
            if element.tag == "node":
                lat = decimal.Decimal(element.attrib['lat'])
                lon = decimal.Decimal(element.attrib['lon'])
                osm_id = int(element.attrib['id'])
                self.node_database[osm_id] = Coord(lat, lon)
            if element.tag == "way":
                coords = self.get_coords_of_complex_object(element)
                osm_id = int(element.attrib['id'])
                self.way_database[osm_id] = coords
            fun(Element(element, self))

