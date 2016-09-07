# arcpy_tools
Various modules and tools for with ArcPy. 

To use, download or clone this repository and use directly on a computer with ArcGIS Installed. The toolbox can be added to ArcGIS without an installation process.

## Portal Tools

* Add Item
Adds layers from an ArcGIS MapService as feature layer items to ArcGIS Portal. This can provide layer by layer access to mapservice layers, similar to when accessing a Feature Service.

*Requires* [Python for Windows Extension](https://sourceforge.net/projects/pywin32/)

## Workspace Tools

* Parse AGS XML Workspace
A native python script that parses ArcGIS XML Workspace documents to return a list of feature classes they define.  