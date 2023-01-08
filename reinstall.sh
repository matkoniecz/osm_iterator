rm dist -rf
python3 setup.py sdist bdist_wheel
cd dist
pip3 uninstall osm_iterator -y
pip3 install --user *.whl
cd ..
python3 -m unittest
# twine upload dist/* # to upload to PyPi
