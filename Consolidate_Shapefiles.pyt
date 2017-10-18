import arcpy, os, fnmatch


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ConsolidateShapefiles]


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
        datatype="DEFolder",
        parameterType="Required",
        direction="Input"
        ))

        # Search filter
        # Filename filter that will be searched
        params.append(arcpy.Parameter(
        displayName="Filter String e.g. *RIVERS*",
        name = "fileFilter",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        ))

        # Output geodatabase
        out_gdb = arcpy.Parameter(
        displayName="Output Geodatabase",
        name = "out_gdb",
        datatype="DEWorkspace",
        parameterType="Required",
        direction="Input"
        )
        out_gdb.filter.list = ["Local Database"]
        params.append(out_gdb)
        # Output feature class name
        # A Feature class will be created with this name.
        params.append(arcpy.Parameter(
        displayName="Output Feature Class Name",
        name = "output_FC_Name",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        ))

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
        # Initialise Parameters

        self.search_folder = parameters[0].valueAsText
        filter_string = parameters[1].valueAsText
        out_gdb = parameters[2].valueAsText
        out_fc_name = parameters[3].valueAsText

        # Search for shapefiles
        input_shapefiles = self.listShapefiles(self.search_folder, filter_string)
        if len(input_shapefiles) == 0:
            arcpy.AddError("No shapefiles found")
            return
        elif len(input_shapefiles) == 1:
            arcpy.AddWarning("Only 1 input shapefile found")
        else:
            arcpy.AddMessage(str(len(input_shapefiles)) + " input shapefiles found.")


        # Note that no transformation will take place
        # TODO - add a field for source file.
        out_fc = out_gdb + "\\" + out_fc_name
        # Check if output FC exists.
        if arcpy.Exists(out_fc):
            # Append all data.
            self.appendShapefiles(input_shapefiles, out_fc)

        else:
            # Create output feature class using first input shapefile
            # WARNING - this approach will cause problems if schemas don't match exactly, e.g. a TEXT description field is longer in a subsequent shapefile.
            arcpy.CopyFeatures_management (input_shapefiles[0], out_gdb + "\\" + out_fc_name)
            if len(input_shapefiles) > 1:
                # Append subsequent files.
                self.appendShapefiles(input_shapefiles[1:], out_fc)
                #

        return
    def appendShapefiles(self, input_shapefiles, out_fc):
        """ Simply runs append for the given shapefile list to target FC."""
        out_spatRef = arcpy.Describe(out_fc).spatialReference
        arcpy.AddMessage("Output spatial reference {0} ({1} {2})".format (out_spatRef.name, out_spatRef.factoryCode, out_spatRef.abbreviation))
        arcpy.SetProgressor("step", "Loading shapefiles to " + out_fc, 0, len(input_shapefiles))
        for in_shp in input_shapefiles:
            arcpy.SetProgressorLabel("Loading {0}...".format(in_shp.replace(self.search_folder + "\\","")))
            # Check spatial reference equal.
            arcpy.AddMessage(" Loading {0}".format(in_shp.replace(self.search_folder + "\\","")))
            if not out_spatRef.name == arcpy.Describe(in_shp).spatialReference.name:
                arcpy.AddWarning(" {0} Possible Spatial Reference Mismatch - {1} ({2})".format(os.path.basename(in_shp), arcpy.Describe(in_shp).spatialReference.name, arcpy.Describe(in_shp).spatialReference.abbreviation))
            # TODO - check schema/fields? #NiceToHave

            arcpy.Append_management(in_shp, out_fc, 'NO_TEST') #, fieldMappings, subtype)
            arcpy.SetProgressorPosition()

    def listShapefiles(self, search_folder, filter_string):
        """Returns a list of shapefiles matching the input filename filter"""
        shapefile_list = []
        if not filter_string.endswith(".shp"):
            filter_string = filter_string + ".shp"
        for path, subdirs, files in os.walk(search_folder):
            for name in files:
                if fnmatch.fnmatch(name, filter_string):
                    shapefile_list.append(os.path.join(path, name))

        return shapefile_list