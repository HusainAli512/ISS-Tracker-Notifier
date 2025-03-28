import requests
from datetime import datetime
import math 
import smtplib
import time
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude
def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return abs(MY_LAT - iss_latitude) <=5 and abs(MY_LONG - iss_longitude) <=5

def sendmail():
    email = "youremail"
    password = "yourpassword"
    with smtplib.SMTP("smtp.gmail.com" , 587) as connection:
        connection.starttls()
        connection.login(user= email , password = password)
        connection.sendmail(from_addr=email , to_addrs= "youremail", msg = "subject:look up\n\n look up")

def runcode():
    if is_nighttime() and iss_overhead():
                sendmail()

def is_nighttime():
  
    parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = time_now.hour
    return hour >= sunset or hour <= sunrise
while True:
     runcode()
     time.sleep(60)
    
