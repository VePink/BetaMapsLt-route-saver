import datetime
import gzip
import json
import simplekml
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import sys
from pyproj import Transformer



input_url = (input("Paste beta.maps.lt routing URL here and then press enter: ") or "https://beta.maps.lt/route/2663056.466808474%2C7338750.124243488%40czE2MzYxMg%3D%3D%3B2664286.6252324716%2C7340109.27015272%40czE1MTk3Ng%3D%3D/car?c=2664011.9%2C7339444&r=0&s=9027.977411&b=topo&bl=false")
print("Selected input URL: " + input_url)


driver = webdriver.Chrome(executable_path = ChromeDriverManager().install())

print('-----------------')
print('DO NOT close browser window. Getting route vertices ...')

if input_url != "":
    driver.get(input_url)

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.url == "https://beta.maps.lt/services/agssecure/Marsrutai/Marsrutai_WM_FGDB_D/NAServer/Route/solve": 
        response_body = request.response.body


response_body = gzip.decompress(response_body)
response_body = response_body.decode('utf-8')

#response_body = json.loads(response_body)

#routeVertices_EPGS3857 = response_body['routes']['features'][0]['geometry']['paths'][0]
print(response_body['Total_Minutes'])
driver.close()

