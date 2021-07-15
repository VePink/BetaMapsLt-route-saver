from selenium import webdriver
import simplekml
import os
import datetime
import json

clear = lambda: os.system('cls')
clear() #clear terminal every time code runs

print("STARTING ...")
timestampSTART = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

root = "C:\\Users\\Ve\\Documents\\GitHub\\BetaMapsLt-route-saver"
PATH = "C:\Program Files (x86)\chromedriver.exe"

'''
driver = webdriver.Chrome(PATH)

driver.get('https://aibe.lt/parduotuves/') #open browser
jsonMarkers = driver.execute_script('return jsonMarkers') #get var "jsonMarkers"
shopList = jsonMarkers[10:] #shops starts with n-th object in the list and continues to end of list
driver.quit() #close browser
'''

from seleniumwire import webdriver  # Import from seleniumwire

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(PATH)

input_url = 'https://beta.maps.lt/route/2505789.1674634535%2C7431158.745906778%40YTExMDYwMjU%3D%3B2535752.481384866%2C7435744.967603883%40cmU2MzQ2/car?c=2512485.6%2C7441815.6&r=0&s=144447.638572&b=topo&bl=false'
driver.get(input_url)

response_body = ''

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.url == "https://beta.maps.lt/services/agssecure/Marsrutai/Marsrutai_WM_FGDB_D/NAServer/Route/solve": 
        response_body=request.response.body



#response_body = response_body.decode("utf-8")
response_body = json.loads(response_body)



#print("-------------")
#print(response_body)
#print("-------------")
#print(type(response_body))
#print("-------------")
print(response_body['routes']['features'][0]['geometry']['paths'])

driver.quit()
#data = json.loads(response)




'''
# Create an instance of Kml
kml = simplekml.Kml(open=1)

for lat, lon, address, name, weekdayTimeOpens, weekdayTimeCloses, saturdayTimeOpens, saturdayTimeCloses, sundayTimeOpens, sundayTimeCloses, a11, a12, type, a14, a15, a16, a17, phone, a19, a20, a21, a22, a23, a24, a25, a26, a27 in shopList:
    pnt = kml.newpoint()
    pnt.name = name
    pnt.description = "tipas: " + type + "\n" + "adresas: " + address + "\n" + "tel: " + phone + "\n" + "darbo laikas:" + "\n" + "dd.: "+ weekdayTimeOpens + "-" + weekdayTimeCloses + "\n" + "Š.: "+ saturdayTimeOpens + "-" + saturdayTimeCloses + "\n" + "S.: "+ sundayTimeOpens + "-" + sundayTimeCloses
    pnt.coords = [(lon, lat)]
    pnt.style.iconstyle.icon.href = root + "\\Input\\Aibe.png"
    pnt.style.labelstyle.scale = 0 # hides label

timestamp = str(datetime.datetime.now().strftime("%Y%m%d_%H"))

kml.save(root + "\\Output\\AIBE_" + timestamp + ".kml")
'''

timestampEND = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print("____________________")
print("started: " + timestampSTART)
print("ended: " + timestampEND)
print("____________________")
print("SUCCESSFUL process")


