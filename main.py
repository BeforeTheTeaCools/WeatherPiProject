import sys
sys.path.append(r'lib')

import signal
import epd2in7b
import epdconfig
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import pyowm

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")
#put api key below
owm = pyowm.OWM('ENTER API KEY') # I have removed mine in this upload

city_id = 4702732 # Katy, Texas, US
city_state = 'Katy, Tx'

# check meteocons documentation for mapping
weather_icon_dict = {200 : "6", 201 : "6", 202 : "6", 210 : "6", 211 : "6", 212 : "6",
                     221 : "6", 230 : "6" , 231 : "6", 232 : "6",

                     300 : "7", 301 : "7", 302 : "8", 310 : "7", 311 : "8", 312 : "8",
                     313 : "8", 314 : "8", 321 : "8",

                     500 : "7", 501 : "7", 502 : "8", 503 : "8", 504 : "8", 511 : "8",
                     520 : "7", 521 : "7", 522 : "8", 531 : "8",

                     600 : "V", 601 : "V", 602 : "W", 611 : "X", 612 : "X", 613 : "X",
                     615 : "V", 616 : "V", 620 : "V", 621 : "W", 622 : "W",

                     701 : "M", 711 : "M", 721 : "M", 731 : "M", 741 : "M", 751 : "M",
                     761 : "M", 762 : "M", 771 : "M", 781 : "M",

                     800 : "1",

                     801 : "H", 802 : "N", 803 : "N", 804 : "Y"
}


def main():
    epd = epd2in7b.EPD()
    while True:

        # Get Weather data from OWM
        obs = owm.weather_at_id(city_id)
        location = obs.get_location().get_name()
        weather = obs.get_weather()
        description = weather.get_detailed_status()
        tempunit = 'fahrenheit' # change it to 'celsius' for celsius
        temperature = weather.get_temperature(unit=tempunit)
        clouds = weather.get_clouds()
        wind = weather.get_wind()
        rain = weather.get_rain()
        print("location: " + location)
        print("weather: " + str(weather))
        print("description: " + description)
        print("temperature: " + str(temperature))
        print("clouds: " + str(clouds))
        print("wind: " + str(wind))
        print("rain: " + str(rain))
        # This is where I display weather data on the E-ink display
        try:
            print("Clear")
            epd.init()
            epd.Clear()

            # Drawing on the Horizontal image
            HBlackimage = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 298*126

            print("Drawing")
            drawblack = ImageDraw.Draw(HBlackimage)
            fontbig = ImageFont.truetype('fonts/arial.ttf', 54)
            font28 = ImageFont.truetype('fonts/arial.ttf', 28)
            font24 = ImageFont.truetype('fonts/arial.ttf', 24)
            font18 = ImageFont.truetype('fonts/arial.ttf', 18)
            font16 = ImageFont.truetype('fonts/arial.ttf', 16)
            font20 = ImageFont.truetype('fonts/arial.ttf', 20)
            fontweather = ImageFont.truetype('fonts/meteocons-webfont.ttf', 30)
            fontweatherbig = ImageFont.truetype('fonts/meteocons-webfont.ttf', 60)

            w2, h2 = font20.getsize(description)
            w3, h3 = fontweatherbig.getsize(weather_icon_dict[weather.get_weather_code()])

            drawblack.text((10, 5), city_state, font = font24, fill = 0)
            drawblack.text((10, 35), description, font = font20, fill = 0)
            drawblack.text((264 - w3 - 10, 0), weather_icon_dict[weather.get_weather_code()], font = fontweatherbig, fill = 0)

            tempstr = str("{0}{1}F".format(int(round(temperature['temp'])), u'\u00b0'))
            print( tempstr)
            drawblack.text((75, 65), tempstr, font = fontbig, fill = 0)
            drawblack.text((95, 120), str("{0}{1} | {2}{3}".format(int(round(temperature['temp_min'])), u'\u00b0', int(round(temperature['temp_max'])), u'\u00b0')), font = font18, fill = 0)


            epd.display(epd.getbuffer(HBlackimage),epd.getbuffer(HBlackimage))
            time.sleep(2)

            epd.sleep()

        except IOError as e:
            print ('traceback.format_exc():\n%s',traceback.format_exc())
            epdconfig.module_init()
            epdconfig.module_exit()
            exit()

        time.sleep(900) # I want to let it sleep for 15 minutes since I want to preserve the e-ink display and don't need weather data updated too much



def ctrl_c_handler(signal, frame):
    print('Goodbye!')
    epdconfig.module_init()
    epdconfig.module_exit()
    exit(0)

signal.signal(signal.SIGINT, ctrl_c_handler)

if __name__ == '__main__':
    main()
