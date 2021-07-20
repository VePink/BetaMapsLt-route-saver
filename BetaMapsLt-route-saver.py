from selenium import webdriver
import simplekml
import os
import sys
import datetime
import json

clear = lambda: os.system('cls')
clear() #clear terminal every time code runs

print("STARTING ...")
timestampSTART = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)



root = input("Paste path to folder. Result KML will be saved there: ")
root = root.replace('\\','\\\\')
input_url = input("Paste beta.maps.lt routing URL here and then press enter: ")

from seleniumwire import webdriver  # Import from seleniumwire

# Create a new instance of the Chrome driver
#driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

print('-----------------')
print('DO NOT close browser window. Getting route vertices ...')

if input_url != "":
    driver.get(input_url)

response_body = ''

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.url == "https://beta.maps.lt/services/agssecure/Marsrutai/Marsrutai_WM_FGDB_D/NAServer/Route/solve": 
        response_body=request.response.body

response_body = json.loads(response_body)

routeVertices_EPGS3857 = response_body['routes']['features'][0]['geometry']['paths'][0]

driver.quit()
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

timestampEND = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print("____________________")
print("started: " + timestampSTART)
print("ended: " + timestampEND)
print("____________________")
print("SUCCESSFUL process")

os.system("pause")

#cd C:\Users\Ve\Documents\GitHub\BetaMapsLt-route-saver
#pyinstaller ./BetaMapsLt-route-saver.py --onefile --add-binary "./driver/chromedriver.exe;./driver"