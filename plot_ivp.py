# importing libraries
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import serial_data
import math

# matplotlib.use('TkAgg') 

figure, axis = plt.subplots(1, 3, figsize=(8, 8))
figure.tight_layout()
plt.subplots_adjust(hspace=0.2, wspace=0.1 )
axis[0].set_title("Solar Voltage")
axis[1].set_title("Solar Current")
axis[2].set_title("Solar Power")


def idx2axis(idx):
    return idx

xs = range(100)
ys = [[11,22] * 50, [-5,5] * 50, [0,70] * 50]

styles = ['r-', 'g-', 'y-']

def iplot(idx, style):
    return axis[idx2axis(idx)].plot(xs, ys[idx], style, animated=True)[0]
lines = [iplot(idx, style) for idx, style in enumerate(styles)]

ys = [[0] * 100,[0] * 100,[0] * 100,[0] * 100,[0] * 100,[0] * 100]

def animate(i):
    if not serial_data.received: return []
    # xs.append(i)
    ys[0].append(serial_data.datahistory[-1].solar_voltage)
    ys[1].append(-serial_data.datahistory[-1].solar_current)
    ys[2].append(abs(serial_data.datahistory[-1].solar_voltage * serial_data.datahistory[-1].solar_current))
    
    
    for j, line in enumerate(lines):
        ys[j] = ys[j][-100:]

        line.set_xdata(xs)
        line.set_ydata(ys[j])
    
    return lines

def press(event):
    if event.key == "l":
        # print('load')
        serial_data.toggle_load()
    if event.key == "r":
        # print('load')
        serial_data.start_sweep()

ani = animation.FuncAnimation(figure, animate, interval=200, save_count=100, blit=True)
figure.canvas.mpl_connect('key_press_event', press)

def start():
    plt.show()