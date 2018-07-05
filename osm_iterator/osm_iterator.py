# coding=utf-8

from lxml import etree

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

    def get_tag_dictionary(self):
        returned = {}
        for tag in self.element:
            if tag.tag != "tag":
                continue
            key = tag.attrib['k']
            value = tag.attrib['v']
            returned[key] = value
        return returned

    def get_coords(self):
        if self.element.tag == "node":
            lat = float(self.element.attrib['lat'])
            lon = float(self.element.attrib['lon'])
            return Coord(lat, lon)
        return self.data.get_coords_of_complex_object(self.element)

    def get_bbox(self):
        return self.data.get_bbox_of_object(self.element)

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

    def get_bbox_of_object(self, lxml_element):
        if lxml_element.tag == "way" or lxml_element.tag == "relation":
            return self.get_bbox_of_complex_object(lxml_element)
        if lxml_element.tag == "node":
            return self.get_bbox_of_node_object(lxml_element)

    def get_bbox_of_node_object(self, lxml_element):
        if lxml_element.tag == "node":
            lat = float(lxml_element.attrib['lat'])
            lon = float(lxml_element.attrib['lon'])
            return {'min_lat': lat, 'min_lon': lon, 'max_lat': lat, 'max_lon': lon}
        else:
            raise ValueError("Not a proper lxml_element passed to get_bbox_of_node_object")

    def get_bbox_of_complex_object(self, lxml_element):
        min_lat = 180
        max_lat = -180
        min_lon = 180
        max_lon = -180
        if lxml_element.tag != "way" and lxml_element.tag != "relation":
            raise ValueError("Not a proper lxml_element passed to get_coords_of_complex_object")
        for tag in lxml_element:
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
        return {'min_lat': min_lat, 'min_lon': min_lon, 'max_lat': max_lat, 'max_lon': max_lon}

    def get_coords_of_complex_object(self, lxml_element):
        bb = self.get_bbox_of_complex_object(lxml_element)
        if bb == None:
            return None
        return Coord((bb['min_lat'] + bb['max_lat']) / 2, (bb['min_lon'] + bb['max_lon']) / 2)


    def iterate_over_data(self, fun):
        for lxml_element in self.data.getiterator():
            if lxml_element.tag != "node" and lxml_element.tag != "way" and lxml_element.tag != "relation":
                continue
            if lxml_element.tag == "node":
                lat = float(lxml_element.attrib['lat'])
                lon = float(lxml_element.attrib['lon'])
                osm_id = int(lxml_element.attrib['id'])
                self.node_database[osm_id] = Coord(lat, lon)
            if lxml_element.tag == "way":
                coords = self.get_coords_of_complex_object(lxml_element)
                osm_id = int(lxml_element.attrib['id'])
                self.way_database[osm_id] = coords
            fun(Element(lxml_element, self))

