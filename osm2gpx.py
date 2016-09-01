#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from lxml import etree
import sys
import getopt
import re
import os

def print_gpx_header():
  print("""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:rmc="urn:net:trekbuddy:1.0:nmea:rmc" creator="QLandkarteGT 1.7.0 http://www.qlandkarte.org/" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.qlandkarte.org/xmlschemas/v1.1 http://www.qlandkarte.org/xmlschemas/v1.1/ql-extensions.xsd" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:ql="http://www.qlandkarte.org/xmlschemas/v1.1">
 <metadata>
  <time>2016-04-18T05:07:54Z</time>
 </metadata>
      """)

def print_gpx_end():
  print("""
</gpx>
      """)

def print_gpx_marker(node):
  name=""
  ele=0.0
  lat=float(node.get("lat"))
  lon=float(node.get("lon"))
  action=node.get("action")
  if action!=None:
    if action=="delete":
      return
  for tag in node:
    if tag.tag == "tag":
      k=tag.get("k")
      v=tag.get("v")
      if k=="ref":
        # имя маркера берём из тега "ref":
        name=v
      if k=="ele":
        ele=float(v)
  print("""
 <wpt lon="%(lon)f" lat="%(lat)f">
  <ele>%(ele)f</ele>
  <time>2016-03-17T01:27:57Z</time>
  <name>%(name)s</name>
  <cmt></cmt>
  <sym>Flag, Blue</sym>
 </wpt>
      """ % {\
      "lat":lat,\
      "lon":lon,\
      "ele":ele,\
      "name":name\
      })



#################  Main  ##################
nodes={}
ways={}
relations={}
DEBUG=False

in_file=sys.argv[1]

osm = etree.parse(in_file)
osm_root = osm.getroot()
#print (etree.tostring(osm_root,pretty_print=True, encoding='unicode'))

for node in osm_root:
	if DEBUG:
		print node.tag
	if node.tag=="bounds":
		continue
	# Формируем списки точек, линий, отношений:
	if node.tag=="node":
#		if DEBUG:
#			print ("DEBUG: node.keys: ", node.keys())
		nodes[node.get("id")]=node
	if node.tag=="way":
#		if DEBUG:
#			print ("DEBUG: node.keys: ", node.keys())
		ways[node.get("id")]=node
	if node.tag=="relation":
#		if DEBUG:
#			print ("DEBUG: node.keys: ", node.keys())
		relations[node.get("id")]=node

print_gpx_header()
# Печатаем точки как маркеры, имя маркера - в теге 'ref' osm-данных:
for node_id in nodes:
  print_gpx_marker(nodes[node_id])
print_gpx_end()






