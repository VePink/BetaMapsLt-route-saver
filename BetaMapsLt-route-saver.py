import simplekml
import os
import sys
import datetime
import json

clear = lambda: os.system('cls')
clear() #clear terminal every time code runs


def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)

sys.excepthook = show_exception_and_exit


print("STARTING ...")
timestampSTART = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

root = (input("Paste path to folder. Result KML will be saved there: ") or "D:\\TEMP")
print("Selected result folder: " + root)
root = root.replace('\\','\\\\')

input_url = (input("Paste beta.maps.lt routing URL here and then press enter: ") or "https://beta.maps.lt/route/2352894.9400547915%2C7499450.809661161%40YTE4NzQyODg%3D%3B2702415.017184936%2C7376482.156027843%40czE0NjQzMw%3D%3D/car/fastest/single?c=2380887.5%2C7440929&r=0&s=2311162.217155&b=topo&bl=false")
print("Selected input URL: " + input_url)

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(executable_path = ChromeDriverManager().install())

print('-----------------')
print('DO NOT close browser window. Getting route vertices ...')

if input_url != "":
    driver.get(input_url)

response_body = ''

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.url == "https://beta.maps.lt/services/agssecure/Marsrutai/Marsrutai_WM_FGDB_D/NAServer/Route/solve": 
        response_body = request.response.body

response_body = json.loads(response_body)

routeVertices_EPGS3857 = response_body['routes']['features'][0]['geometry']['paths'][0]

driver.close()
print('-----------------')
print('Transforming vertex coordinates ...')

from pyproj import Transformer
transformer = Transformer.from_crs("epsg:3857", "epsg:4326")

routeVertices_EPSG4326 = []

def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

for v in routeVertices_EPGS3857:
    res = transformer.transform(v[0], v[1])
    res = Reverse(res)
    routeVertices_EPSG4326.append(res)

print('-----------------')
print('Combining to route ...')

# Create an instance of Kml
kml = simplekml.Kml(open=1)

linestring = kml.newlinestring(name="A Hovering Line")
linestring.coords = routeVertices_EPSG4326

timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H%M_%S"))

kml.save(root + "\\Route_" + timestamp + ".kml")
print('-----------------')
print('Saving as KML route ...')

print('-----------------')
print("Saved route as KML file on " + root)

from CLTreport.summary import report_summary
report_summary()

# Below are notes for making EXE package with pyinstaller from PY code.
# cd C:\Users\Ve\Documents\GitHub\BetaMapsLt-route-saver
# cd C:\Users\Vejas\Documents\GitHub\BetaMapsLt-route-saver
# pyinstaller ./BetaMapsLt-route-saver.py --onefile