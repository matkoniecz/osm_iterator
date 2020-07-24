import unittest
import osm_iterator
from io import BytesIO

class Tests(unittest.TestCase):
    def test_osm_iterator(self):
        some_file_or_file_like_object = BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><osm><node id="17658600" lat="49.8698080" lon="8.6300980"></node></osm>')
        parsed = osm_iterator.Data(some_file_or_file_like_object)
        print(parsed.data)
        for element in parsed.data.getiterator():
            print("XXYXYXYXY" + " " + str(element.tag))

    def test_location_for_node(self):
        collected = []
        def helper_function_for_test_locations_in_center_output(element):
            collected.append(element.get_coords())
        # obtained by Overpass call
        """
        node(1);
        out center;
        """
        # Tags removed to keep it simple
        some_file_or_file_like_object = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
        <osm version="0.6" generator="Overpass API 0.7.56.3 eb200aeb">
        <note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>
        <meta osm_base="2020-07-24T09:13:02Z"/>

        <node id="1" lat="42.7957187" lon="13.5690032">
        </node>
        </osm>
        """)
        parsed = osm_iterator.Data(some_file_or_file_like_object)
        parsed.iterate_over_data(helper_function_for_test_locations_in_center_output)
        #print(len(collected))
        #print(collected[0].lat, collected[0].lon, "node")
        self.assertEqual(collected[0].lat, 42.7957187)
        self.assertEqual(collected[0].lon, 13.5690032)

    def test_locations_for_way_center_output(self):
        collected = []
        def helper_function_for_test_locations_in_center_output(element):
            collected.append(element.get_coords())
        # obtained by Overpass call
        """
        way(30565458);
        out center;
        """
        # Oboźna modified to Obozna to keep file mocking working
        # Tags, nodes removed to keep it simple anyway
        some_file_or_file_like_object = BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
        <osm version="0.6" generator="Overpass API 0.7.56.3 eb200aeb">
        <note>The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.</note>
        <meta osm_base="2020-07-24T09:13:02Z"/>

        <way id="30565458">
            <center lat="50.0792021" lon="19.9284416"/>
        </way>
        </osm>
        """)
        parsed = osm_iterator.Data(some_file_or_file_like_object)
        parsed.iterate_over_data(helper_function_for_test_locations_in_center_output)
        #print(len(collected))
        #print(collected[0].lat, collected[0].lon, "way")
        self.assertEqual(collected[0].lat, 50.0792021)
        self.assertEqual(collected[0].lon, 19.9284416)

if __name__ == '__main__':
    unittest.main()

