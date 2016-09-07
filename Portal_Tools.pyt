import arcpy, re, os, urllib, json

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "ArcGIS Portal Windows Tools"
        self.alias = ""


        # List of tool classes associated with this toolbox
        self.tools = [AddItems]


class AddItems(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Items to Portal"
        self.description = "Add feature layer items from an ArcGIS Server MapService"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []

        # URL to the Map Service, will authenticate using Integrated Windows Authentication.
        params.append(arcpy.Parameter(
        displayName="ArcGIS Server Map Service URL",
        name = "inMapServiceURL",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        ))

        # String for ArcGIS Portal, including the web adapter.  Will authenticate using Integrated Windows Authentication.
        params.append(arcpy.Parameter(
        displayName="ArcGIS Portal URL",
        name = "inPortalURL",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        ))

        params.append(arcpy.Parameter(
        displayName="Item Tags",
        name = "inTagsCSV",
        datatype="GPString",
        parameterType="Optional",
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


        s_url_pattern = re.compile(r'^http[s]?://(?:.+)/MapServer$',re.IGNORECASE) # Basic Regex to keep form responsive.
        if parameters[0].altered:
            # Check that URL parameter matched a URL, ending in mapserver
            if re.match(s_url_pattern, parameters[0].valueAsText):
                parameters[0].clearMessage()
            else:
                parameters[0].setErrorMessage('Please specify a map service URL, e.g. http://myagsServer.co.uk/arcgis/myService/MapServer')

        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        try:
            import win32com.client
        except ImportError:
            arcpy.AddError("Cannot load Win32 module.  Please install to enable integrated authentication with your ArcGIS Server")
            return

        # Parameters
        serviceURL  = parameters[0].valueAsText
        portalURL = parameters[1].valueAsText
        tags = parameters[2].valueAsText

        # Uses win32 client to dispatch the request which will use integrated authentication,
        # authenticating with portal and ArcGIS Server as the user running the script.

        h = win32com.client.Dispatch('WinHTTP.WinHTTPRequest.5.1')
        h.SetAutoLogonPolicy(0)
        h.SetProxy(0)
        portalUser = os.getenv('username') + "@" + os.getenv('userdomain')
        params = {'f': 'json'}
        req = serviceURL  + "?" + urllib.urlencode(params)

        h.Open("GET",req, False)
        h.Send()
        response = h.responseText
        data = json.loads(response)
        for layer in data['layers']:
            name =  layer['name']
            id = layer['id']
            serviceURL2 = serviceURL + "/{0}".format(id)
            agolURL = portalURL + '/sharing/rest/content/users/' + portalUser + '/addItem'
            params = {'f': 'json', 'url': serviceURL2, 'title': name, 'type': 'Feature Service', 'tags': tags + ',' + name}
            pURL = agolURL + "?" + urllib.urlencode(params)
            h.Open("POST",pURL, False)
            h.Send()
            response = h.responseText

            try:
                data = json.loads(response)
                if 'error' in data:
                    arcpy.AddError(data['error']['message'])
                else:
                    arcpy.AddMessage("Successfully added " + name + " as an item")
            except:
                arcpy.AddError("Error adding {0}: {1} {2}\n\t{3}".format(name, h.Status, h.StatusText, h.responseText))



        return
