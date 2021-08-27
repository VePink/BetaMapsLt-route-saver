import datetime

root = (input("Paste path to folder. Result KML will be saved there: ") or "C:\\Users\\Vejas\\Downloads\\22")
print("Selected result folder: " + root)
root = root.replace('\\','\\\\')

input_url = (input("Paste beta.maps.lt routing URL here and then press enter: ") or "https://beta.maps.lt/route/2663056.466808474%2C7338750.124243488%40czE2MzYxMg%3D%3D%3B2664286.6252324716%2C7340109.27015272%40czE1MTk3Ng%3D%3D/car?c=2664011.9%2C7339444&r=0&s=9027.977411&b=topo&bl=false")
print("Selected input URL: " + input_url)

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(executable_path = ChromeDriverManager().install())

print('-----------------')
print('DO NOT close browser window. Getting route vertices ...')

if input_url != "":
    driver.get(input_url)

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.url == "https://beta.maps.lt/services/agssecure/Marsrutai/Marsrutai_WM_FGDB_D/NAServer/Route/solve": 
        response_body = request.response.body

import gzip
response_body = gzip.decompress(response_body)
response_body = response_body.decode('utf-8')
import json
response_body = json.loads(response_body)

routeVertices_EPGS3857 = response_body['routes']['features'][0]['geometry']['paths'][0]

driver.close()

print('-----------------')
print('Transforming vertex coordinates ...')
from pyproj import Transformer
transformer = Transformer.from_crs("epsg:3857", "epsg:4326")


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

routeVertices_EPSG4326 = []

i = 0

for v in routeVertices_EPGS3857:
    i += 1
    totalVertexCount = len(routeVertices_EPGS3857)
    res = transformer.transform(v[0], v[1])
    res = Reverse(res)
    print("=====================")
    print("vertex no " + str(i) + " / " + str(totalVertexCount))
    routeVertices_EPSG4326.append(res)

print('-----------------')
print('Combining to route ...')

import simplekml
kml = simplekml.Kml(open=1)

routePolyline = kml.newlinestring(name="Planned route")
routePolyline.style.linestyle.color = simplekml.Color.red
routePolyline.style.linestyle.width = 5
routePolyline.coords = routeVertices_EPSG4326

timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H%M_%S"))

kml.save(root + "\\Route_" + timestamp + ".kmz")
print('-----------------')
print('Saving as KMZ route ...')

print('-----------------')
print("Saved route as KMZ file on " + root)

from CLTreport.summary import report_summary
report_summary()

# Below are notes for making EXE package with pyinstaller from PY code.

# cd C:\Users\Ve\Documents\GitHub\BetaMapsLt-route-saver
# cd C:\Users\Vejas\Documents\GitHub\BetaMapsLt-route-saver
# pyinstaller ./BetaMapsLt-route-saver.py --onefile