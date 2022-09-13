import bluetooth
import socket
import time
import re
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def getData():
    sock.send('AT RV\r') 
    time.sleep(0.0)
    x=sock.recv(25)
    matches = re.findall("[+-]?\d+\.\d+",str(x))

    try:
        z = matches[0]
    except IndexError:
        z = 'null'

    return z


def append_hex(a, b):
    sizeof_b = 0

    # get size of b in bits
    while((b >> sizeof_b) > 0):
        sizeof_b += 1

    # align answer to nearest 4 bits (hex digit)
    sizeof_b += sizeof_b % 4

    return (a << sizeof_b) | b

def getRPM():

    sock.send('01 0C\r') 
    time.sleep(0.0)
    x=sock.recv(25)
    #x = str("b'01 0C\r41 0C FE 34 \r\n\r\n>")
    matches = re.findall('[0-F]+', x)
    print(matches)
    try:
        z = matches[0]
    except IndexError:
        z = 'null'

    matches[4] = int(matches[4],16)
    matches[5] = int(matches[5],16)
    num1 =  matches[4]
    num2 =  matches[5]
    num1 = num1 << 8
    result = num1 + num2
  
    result = result /4
    
    return result

def animate(i,xs,ys):
    # Data for plotting
    
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    i = getData()
    ys.append(i)
    
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)
    # Format plot
    plt.gca().invert_yaxis()
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Battery Power Level')
    plt.ylabel('Voltage [V]')

    # Set up plot to call animate() function periodically


def find_bt_address_by_target_name(name):
    # sometimes bluetooth.discover_devices() failed to find all the devices
    MAX_COUNT = 3
    count = 0
    while True:
        nearby_devices = bluetooth.discover_devices()

        for btaddr in nearby_devices:
            if name == bluetooth.lookup_name( btaddr ):
                return btaddr

        count += 1
        if count > MAX_COUNT:
            return None
        print("Try one more time to find target device..")   


btadd = "00:00:00:33:33:33"
#btadd = find_bt_address_by_target_name('OBDII')
print(btadd)

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((btadd, port))
sock.send(b'01 0C\r')
time.sleep(1)
'''
while 1:
    getRPM()
    time.sleep(1)
'''

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=80)
plt.show()

sock.close()