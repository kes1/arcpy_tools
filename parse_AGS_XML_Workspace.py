#-------------------------------------------------------------------------------
# Name:        Get Feature Classes from XML Workspace Document
# Purpose:     Utility functions for using XML Workspace documents.
#
# Author:      Andrew Kesterton
#
# Created:     30/07/2015
# Copyright:   (c) Andrew Kesterton 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")


def main():
    """ Given an ArcGIS XML workspace document returns a list of feature classes that it contains """
    xml_document = "D:/temp.xml" #"D:/MapAction/echo/2015-07-18-SouthSudan/GIS/5-Tools/RAMP-South-Sudan-Settlements/MASTER_SCHEMA.xml"   #DENORMALISED_SCHEMA.xml"
    fc_list = []
    wd_tree = etree.parse(xml_document)
    root = wd_tree.getroot()


    # 2. loop through "DatasetElement" elements with attribute "esri:DEFeatureClass"
    fcs = root.findall(".//DatasetDefinitions//DataElement[@{http://www.w3.org/2001/XMLSchema-instance}type='esri:DEFeatureClass']")
    for data_element in fcs:
        for fc_name_element in data_element.findall("./Name"):
            fc_list.append(fc_name_element.text)
    return fc_list




if __name__ == '__main__':
    main()
