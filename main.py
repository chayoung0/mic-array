from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import gui_utilities as utils

# frame1
# frame2 frame4
# frame3

root = Tk()
root.title('Sound Localization v1.0')

font_1 = ('Helvatica bold', 16)
font_2 = ('Helvatica bold', 10)

frame1 = LabelFrame(root, text='Sound Localization', font=font_1, padx=10, pady=10)
frame2 = LabelFrame(root, text='File Selection', font=font_1, padx=10, pady=10)
frame3 = LabelFrame(root, text='Status', font=font_1, padx=10, pady=10)
frame4 = LabelFrame(root, text='Result', font=font_1, padx=10, pady=10)

frame1.grid(row=0, column=0, padx=15, pady=15, sticky=E + W + N)
frame2.grid(row=1, column=0, padx=15, pady=15, sticky=W + N + S + E)
frame4.grid(row=0, column=1, padx=15, pady=15, rowspan=3, sticky=E + N + S)
frame3.grid(row=2, column=0, padx=15, pady=15, sticky=E + W + S)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

frame3.columnconfigure(1, weight=0)
frame3.rowconfigure(1, weight=0)

frame4.rowconfigure(0, weight=1)
frame4.columnconfigure(0, weight=1)


def openFile():
    global mic_out_data
    mic_out_data = filedialog.askopenfile(mode='r', title='Select',
                                          filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if mic_out_data:
        myLabel.config(text=mic_out_data.name, anchor='e', fg='ivory4')
    else:
        statusLabel.config(text="Error while opening the file", bg='tomato')


def start():
    u = utils.one_function_to_rule_them_all(mic_out_data, arrayGeometry.get())
    statusLabel.config(text="PROCESSING", bg='light goldenrod')
    plot(arrayGeometry.get(), u[0], u[1], u[2])
    statusLabel.config(text="FINISHED", bg='lime green')


def plot(arrayGeometry, point1=None, point2=None, point3=None):
    ax.clear()

    if arrayGeometry == 4:
        plot4mic()
    elif arrayGeometry == 6:
        plot6mic()
    else:
        plot8mic()

    if point1 is None:
        ax.scatter
    else:
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        ax.set_xlim(0, xlim)
        ax.set_ylim(0, ylim)
        ax.set_zlim(0, zlim)

        ax.quiver(0, 0, 0, point1, point2, point3)
        # ax.scatter(point1, point2, point3, marker="x", s=60, label="Source Location")
        ax.legend(loc='upper right')
        canvas.draw_idle()


def plot4mic():
    ax.clear()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.set_zlim(0, zlim)
    x = (0, 0, xlim, xlim)
    y = (0, ylim, 0, ylim)
    z = (0, 0, 0, 0)
    ax.scatter(x, y, z)
    canvas.draw_idle()


def plot6mic():
    ax.clear()
    c = xlim * 0.366
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.set_zlim(0, zlim)
    x = [0, 10, 10, 0, 5, 5]
    y = [0, 10, 0, 10, 0, 10]
    z = [0, 0, 0, 0, 0, 0.1]
    # x = (c, xlim / 2 - c, xlim, xlim / 2 + c, xlim - c, 0)  # bunlar düzgün altıgen geometri için koordinatlar
    # y = (0, xlim / 2 + c, xlim - c, xlim / 2 - c, xlim, c)
    # z = (0, 0, 0, 0, 0, 0)
    ax.scatter(x, y, z)
    canvas.draw_idle()


def plot8mic():
    ax.clear()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.set_zlim(0, zlim)
    x = (0, 0, 0, 0, xlim, xlim, xlim, xlim)
    y = (0, 0, ylim, ylim, 0, 0, ylim, ylim)
    z = (0, zlim, 0, zlim, 0, zlim, 0, zlim)
    ax.scatter(x, y, z)
    canvas.draw_idle()


plt.ion()

# the figure that will contain the plot
fig = Figure(figsize=(6, 6), dpi=100)

# adding the subplot
ax = fig.add_subplot(111, projection="3d")

xlim, ylim, zlim = 100, 100, 100

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

ax.set_xlim(0, xlim)
ax.set_ylim(0, ylim)
ax.set_zlim(0, zlim)

canvas = FigureCanvasTkAgg(fig, master=frame4)
canvas.draw()

canvas.get_tk_widget().pack()

# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas, frame4)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()

introText = '''
Sound localization is a field of signal \nprocessing that deals with determining the \norigin of a detected sound signal. This \ninvolves determining the direction and \ndistance of the source of the sound. The \nmethod requires the employment of \nmicrophone arrays which record the sound \nsignal. This program uses an array of 4, 6, or 8 \nmicrophones to present a experimental \nsound source localization method in \n3-dimensional space.
'''
introLabel = Label(frame1, text=introText, font=('Helvatica bold', 12), padx=10, pady=5, anchor='w', justify=LEFT)
introLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)

myLabel = Label(frame2, text='Data File (please select)', font=font_2, relief=GROOVE, padx=10, pady=5, width=25)
myLabel.grid(row=0, column=0, padx=15, pady=15, sticky=W + E)

selectButton = Button(frame2, text='SELECT', font=font_2, command=openFile, padx=15, pady=2)
selectButton.grid(row=0, column=1, padx=15, pady=15, sticky=W + E)

myLabel2 = Label(frame2, text='Array Geometry', font=font_2)
myLabel2.grid(row=1, column=0, columnspan=2, sticky='w', padx=15)

arrayGeometry = IntVar()
arrayGeometry.set(4)
plot4mic()
Radiobutton(frame2, text="4", font=font_2, variable=arrayGeometry, command=plot4mic, value=4).grid(row=2, column=0,
                                                                                                   columnspan=2,
                                                                                                   sticky='w', padx=15,
                                                                                                   pady=10)
Radiobutton(frame2, text="6", font=font_2, variable=arrayGeometry, command=plot6mic, value=6).grid(row=2, column=0,
                                                                                                   columnspan=2,
                                                                                                   padx=15, pady=10)
Radiobutton(frame2, text="8", font=font_2, variable=arrayGeometry, command=plot8mic, value=8).grid(row=2, column=0,
                                                                                                   columnspan=2,
                                                                                                   sticky='e', padx=15,
                                                                                                   pady=10)

startButton = Button(frame2, text='START', font=font_2, command=start, padx=15, pady=2)
startButton.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

statusLabel = Label(frame3, text='READY', font=font_2, relief=GROOVE, padx=10, pady=5, width=40)
statusLabel.pack()

# root.state('zoomed')
main = mainloop()