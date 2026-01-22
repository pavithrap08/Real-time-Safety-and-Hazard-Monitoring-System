import network
from machine import Pin, ADC, SoftI2C
import ssd1306
from time import sleep, sleep_us
import dht
import urequests


ssid = 'Realme Narzo N55'
password = 'p1v9t8r1'


THINGSPEAK_API = "https://api.thingspeak.com/update?api_key=4TIRC50S2ZCZT3BH"


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print("Connecting to Wi-Fi", end="")
while not wlan.isconnected():
    print(".", end="")
    sleep(0.5)
print("\nConnected to Wi-Fi:", wlan.ifconfig())


led_dust = Pin(5, Pin.OUT)        
dust_adc = ADC(Pin(34))           
mq_adc = ADC(Pin(35))             
sound_adc = ADC(Pin(32))          
dht_pin = Pin(14)                 
dht_sensor = dht.DHT11(dht_pin)


dust_adc.atten(ADC.ATTN_11DB)
mq_adc.atten(ADC.ATTN_11DB)
sound_adc.atten(ADC.ATTN_11DB)


i2c = SoftI2C(scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


TEMP_LIMIT = 35
HUM_LIMIT = 70
DUST_LIMIT = 100
AIR_VOLT_LIMIT = 2.0
SOUND_LIMIT = 2000


def read_dust():
    led_dust.off()
    sleep_us(280)
    val = dust_adc.read()
    sleep_us(40)
    led_dust.on()
    sleep_us(9680)
    voltage = val * (3.3 / 4095)
    density = max((0.17 * voltage - 0.1) * 1000, 0)
    return density

def read_dht():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
    except:
        temp, hum = -1, -1
    return temp, hum

def read_mq135():
    val = mq_adc.read()
    voltage = val * (3.3 / 4095)
    return voltage

def read_sound():
    return sound_adc.read()

while True:
    dust = read_dust()
    temp, hum = read_dht()
    mq = read_mq135()
    sound = read_sound()

    
    alert_msgs = []
    if dust > DUST_LIMIT: alert_msgs.append("High Dust")
    if temp > TEMP_LIMIT: alert_msgs.append("High Temp")
    if hum > HUM_LIMIT: alert_msgs.append("High Humidity")
    if mq > AIR_VOLT_LIMIT: alert_msgs.append("Poor Air")
    if sound > SOUND_LIMIT: alert_msgs.append("High Noise")
    alert_text = ", ".join(alert_msgs) if alert_msgs else "All Normal"

    
    oled.fill(0)
    oled.text("Real-Time Safety", 0, 0)
    oled.text("Dust: {:.1f}".format(dust), 0, 12)
    oled.text("Temp:{}C Hum:{}%".format(temp, hum), 0, 24)
    oled.text("AirV:{:.2f}V".format(mq), 0, 36)
    oled.text("Sound:{}".format(sound), 0, 48)
    oled.show()

    # --- Print to console ---
    print("\n===== Real-Time Safety and Alett Monitoring System =====")
    print("Dust : {:.1f} ug/m3".format(dust))
    print("Temp : {} °C".format(temp))
    print("Hum  : {} %".format(hum))
    print("MQ135: {:.2f} V".format(mq))
    print("Sound: {}".format(sound))
    print("Status:", alert_text)
    print("============================\n")

    
    try:
        url = "{}&field1={}&field2={}&field3={}&field4={}&field5={}".format(
            THINGSPEAK_API, temp, hum, sound, mq, dust
        )
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak ✅")
    except Exception as e:
        print("ThingSpeak Error:", e)

    sleep(15)  


