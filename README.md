# WeatherPiProject
RaspberryPi project that uses openweather api to display weather to e-ink display

![](IMG_0616.jpg)

**Required Hardware:**  
RaspberryPi (I used model 3B with Raspbian OS Lite but other models work)  
Waveshare 2.7inch e-ink display or something like Inky Phat

**Set Up:**  
I just manually connected the pi to a monitor temporarily before I switched over to SSH.  
If you prefer to set up headless, here is a link: https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html  

Make sure you enable SPI and I2PC. Just type sudo raspi-config in the terminal and navigate to interface and turn them on  

Type in hostname -I to get the ipaddress for your RaspberryPi. I used PuTTY for SSH so I simply ran PuTTY, and saved a profile with the ipaddress and loaded it up.

**Install dependecies with:**

sudo apt update  
sudo apt-get install python3-pip python3-pil git  
pip3 install RPi.GPIO spidev  
sudo pip3 install pyowm==2.10.0  

PyOWM makes it really convenient to make calls to the OWM API. Here is the link if you want to check it out: https://pyowm.readthedocs.io/en/latest/

I think those were all I needed but if you are installing from vanilla, you might need to install others.

Now simply just clone my respository and run python3 main.py to get the weather station running.

**BEFORE RUNNING:**  
Make sure you open up an account at https://openweathermap.org/ to get an API Key. It's free and allows up to 2000 calls per day iirc.
Once you get your API Key, edit the main.py file. I put a comment that shows where to put it.
Make sure to also get your cityid and replace that in main.py too. To get the cityid, you can simply search your city in https://openweathermap.org/ and then look at the 7 digit numbers at the end of your url.  

If you are using a different display than mine, make sure you go to https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd
and find the correct driver for your display and put it in the lib folder as well as changing the code in main.py corresponding to your display driver.

**Good References:**  
This is a good documentation to look at! I looked at it a lot to figure out how to get the data I want.  
https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#identifying_places  

Meteocons gives a lot of great free icons. The dictionary in the beginning of the main.py file is mapped using weather code from Open Weather Map to icons in Meteocons. I ended up not using a lot of them but a lot of them have been mapped for future use. Below is a link if you want to check it out.  
https://www.alessioatzeni.com/meteocons/
