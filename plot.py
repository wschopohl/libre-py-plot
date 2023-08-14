# importing libraries
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import serial_data

# matplotlib.use('TkAgg') 

figure, axis = plt.subplots(6, 1)
axis[0].set_title("Battery Voltage")
axis[1].set_title("Battery Current")
axis[2].set_title("Solar Voltage")
axis[3].set_title("Solar Current")
axis[4].set_title("Load Current")
axis[5].set_title("PWM Freuency")

styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']

def plot(ax, style):
    return ax.plot(x, y, style, animated=True)[0]
lines = [plot(ax, style) for ax, style in zip(axis, styles)]


xs = []
ys = [[],[],[],[],[],[]]

def animate(i, xs, ys):
    if not serial_data.received: return
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys[0].append(serial_data.datahistory[-1].battery_voltage)
    ys[1].append(serial_data.datahistory[-1].battery_current)
    ys[2].append(serial_data.datahistory[-1].solar_voltage)
    ys[3].append(serial_data.datahistory[-1].solar_current)
    ys[4].append(serial_data.datahistory[-1].load_current)
    ys[5].append(serial_data.datahistory[-1].duty_cycle)

    # Limit x and y lists to 20 items
    xs = xs[-100:]
    for i in range(6):
        ys[i] = ys[i][-100:]

        # Draw x and y lists
        axis[i].clear()
        axis[i].plot(xs, ys[i])
        plt.setp(axis[i].get_xticklabels(), visible=False)

def press(event):
    if event.key == "l":
        print('load')
        serial_data.toggle_load()

ani = animation.FuncAnimation(figure, animate, fargs=(xs, ys), interval=200, save_count=100)
figure.canvas.mpl_connect('key_press_event', press)

def start():
    plt.show()