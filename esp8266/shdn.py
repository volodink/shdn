import machine
from time import sleep
import network
import socket

# Напишете имя точки доступа и пароль !!!
AP_SSID = ''
AP_PASS = ''

sta_if = network.WLAN(network.STA_IF)

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)


def main():
    print('ESP8266 shutdown node started.')
    while True:
        blink(3, 0.1)
        connectWiFi()
        if sta_if.isconnected():
            blink(5, 0.1)
            can_shutdown = getArduinoData()
            if can_shutdown:
                shutdownHost()
                blink(10, 0.05)            
            blink(5, 0.5)
        else:
            blink(5, 1)


def getArduinoData():
    print('Getting data from arduino board ...')
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=100000)
    scan_result = i2c.scan()
    print('Scan result: ', scan_result)
    print('Sending request for data command ...')
    i2c.writeto(85, 'U')
    print('Sending request for data command ... ok')

    print('Receiving data from slave ...')

    try:
        data = i2c.readfrom(85, 1)
    except OSError:
        print('Cant get data from board ...')
        return False

    try:
        data = int.from_bytes(data, 'big')
    except OSError:
        pass

    print('Got data: ', data)

    if data == 0x01:
        print('got permission to shutdown ...')
        return True
    else:
        print('got smth else ...')
        return False


def shutdownHost():
    # Напишите адрес и порт сервера !!!
    addr = socket.getaddrinfo('192.168.1.38', 5555)[0][-1]
    s = socket.socket()
    try:
        s.connect(addr)
    except OSError:
        print('Cant connect to ', addr)
        s.close()
        return
    try:
        s.send('qweqweqweq123456')
    except OSError:
        print('Cant send data to ', addr)
        s.close()


def connectWiFi():
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to ', AP_SSID, ' network...')
        sta_if.active(True)
        sta_if.connect(AP_SSID, AP_PASS)
        while not sta_if.isconnected():
            pass
        print('Network config:', sta_if.ifconfig())


def blink(times, sleep_time):
    led = machine.Pin(16, machine.Pin.OUT)
    for i in range(times):
        led.on()
        sleep(sleep_time)
        led.off()
        sleep(sleep_time)
