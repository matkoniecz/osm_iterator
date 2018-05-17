import unittest
import osm_iterator
from io import BytesIO

class Tests(unittest.TestCase):
    def test_osm_iterator(self):
        some_file_or_file_like_object = BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><osm><node id="17658600" lat="49.8698080" lon="8.6300980"></node></osm>')
        print(osm_iterator.Data(some_file_or_file_like_object).data)
        for element in osm_iterator.Data(some_file_or_file_like_object).data.getiterator():
            print("XXYXYXYXY" + " " + str(element.tag))
 
if __name__ == '__main__':
    unittest.main()
