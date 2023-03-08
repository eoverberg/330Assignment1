# Sources: 
# CS 330, Python Plotter v2.py
#
# Require matplotlib
# To install run "pip install matplotlib" in command line / terminal
# To run:
#  1. Place this file and the file to be plotted in the same folder
#  2. Open this file and change the variable filename to the name of the file
#         to be opened.
#  3. Run in IDE, or run "python 'CS 330, Python Plotter v3.py'" in command line /
#         terminal.


import matplotlib.pyplot as plt
import csv
import math

# Change this to data file name
filename = "output.txt"

# ************************** Setup Plotting Axis ****************************
xLineX = [-100, 100]
xLineY = [0, 0]
yLineX = [0, 0]
yLineY = [-100, 100]
plt.figure(figsize=(6, 6))

# add dashed grey lines
plt.plot(xLineX, xLineY, color='grey', linestyle='dashed', linewidth=1)
plt.plot(yLineX, yLineY, color='grey', linestyle='dashed', linewidth=1)


# Mover class will hold data for each mover entity on the plot
class Mover:
    def __init__(self, behavior):
        self.behavior = behavior  # steering behavior status code
        self.z = []  # position z (meters)
        self.x = []  # position x (meters)
        self.vXp = []  # values to plot velocity x (meters per second)
        self.vZp = []  # values to plot velocity z (meters per second)
        self.laXp = []  # values to plot linear acceleration x (meters per second per second)
        self.laZp = []  # values to plot linear acceleration z (meters per second per second)
        self.oXp = []  # values to plot orientation in x
        self.oZp = []  # values to plot orientation in z


movers = {}  # create dictionary to store different movers

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:

        # as we find other
        if row[1] not in movers:  # row[1] holds the id of the Mover
            movers[row[1]] = Mover(int(row[9]))  # if we don't have a Mover object for a particular id yet,
            # we create one and add it to the dictionary

        m = movers[row[1]]

        m.x.append(float(row[2]))  # Position x
        m.z.append(float(row[3]))  # Position z
        m.vXp.append(
            (float(row[4]) * 2) + float(row[2]))  # Velocity data is multiplied by constants to increase visiblity
        m.vZp.append((float(row[5]) * 2) + float(row[3]))
        m.laXp.append((float(row[6])) + float(row[2]))  # Linear acceleration
        m.laZp.append((float(row[7])) + float(row[3]))
        m.oXp.append((math.cos(float(row[8]))) + float(row[2]))  # Orientation
        m.oZp.append((math.sin(float(row[8]))) + float(row[3]))

for mov in movers:  # for each mover
    m = movers[mov]

    for c in range(0, len(m.x)):  # Plot velocity data
        i = [m.x[c], m.vXp[c]]  # current x, current x + x velocity
        j = [m.z[c], m.vZp[c]]  # current z, current z + z velocity

        plt.plot(i, j, color='#5beb34', linewidth=0.5)  # green

    for c in range(0, len(m.x)):  # Plot linear acceleration data
        i = [m.x[c], m.laXp[c]]  # current x, current x + x linear acceleration
        j = [m.z[c], m.laZp[c]]  # current z, current z + z linear acceleration

        plt.plot(i, j, color='blue', linewidth=0.5)

    # uncomment this to plot orientation data
    # for c in range(0, len(m.x)):    # Plot orientation data
    #     i = [m.x[c], m.oXp[c]]          # current x, current x + x orientation
    #     j = [m.z[c], m.oZp[c]]          # current z, current z + z orientation

    #     plt.plot(i, j, color='yellow', linewidth=0.5) #, label="position") # plots position

for mov in movers:
    m = movers[mov]

    # Plot labels for steering behavior type
    label = ""
    if (m.behavior == 1):
        label = "Continue"
    elif (m.behavior == 3):
        label = "Seek"
    elif (m.behavior == 2):
        label = "Flee"
    elif (m.behavior == 4):
        label = "Arrive"
    elif (m.behavior == 5):
        label = "Follow Path"

    plt.annotate(label, color='red', xy=(m.x[0] + 2, m.z[0] - 2))

    # add red dots to the start and end of each mover's trail
    plt.plot(m.x[0], m.z[0], color='red', marker='o', markerfacecolor='red', markersize=3)  # mark start position
    plt.plot(m.x[-1], m.z[-1], color='red', marker='o', markerfacecolor='red', markersize=4)  # mark end position

    # plot position
    plt.plot(m.x, m.z, color='red', linewidth=1)

# create legend
plt.plot(0, 0, color='red', label='position')
plt.plot(0, 0, color='green', label='velocity')
plt.plot(0, 0, color='blue', label='linear')
# plt.plot(0, 0, color='yellow', label='orientation')


# format plot and save to file
plt.xlabel('x')
plt.ylabel('z')
plt.title('Dynamic Movement PVL Sample')
plt.legend(bbox_to_anchor=(1.0, 0.05), loc='lower right')
plt.xlim(-100, 100)
plt.ylim(100, -100)

# plt.savefig("outputPlot.png",dpi=200)
plt.show()
