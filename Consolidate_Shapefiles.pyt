import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class ConsolidateShapefiles(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Search and Append Shapefiles"
        self.description = "This tool will search for files matching a file search string (e.g. *HEALTH*.shp), once found they will be consolidated into a new file."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Params:
        params = []
        # input workspace - shapefiles in this folder and subdirectories will be searched
        params.append(arcpy.Parameter(
        displayName="Input Folder",
        name = "inWorkspace",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        ))


        # Search filter
        # Filename filter that will be searched

        # Output geodatabase

        # Output feature class name
        # A Feature class will be created with this name.
        params = None
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return
