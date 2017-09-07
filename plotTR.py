# Ryan Lance 
# 17-0905
# Tate Lab
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk				#http://www.python-course.eu/tkinter_sliders.php

d = 150

# Parameter Sliders
master = tk.Tk()
thickness = tk.Scale(master, from_=10, to=250, length = 300,
 orient=tk.HORIZONTAL)
thickness.pack()
parameter1 = tk.Scale(master, from_=0,  to=1000, length = 300,
 orient=tk.HORIZONTAL)
parameter1.pack()
def get_parameters():
	d = thickness.get()
	parameter1.get()
	calc_all(d)
	line1.set_ydata(T)
	line2.set_ydata(R)
	line3.set_ydata(T/(1-R))
	fig.canvas.draw()
tk.Button(master, text = 'Enter',command=get_parameters).pack()

def calc_all(d):
	global x
	global T
	global R
	global n_film
	global k_film
	# All units in nanometers
	x = np.arange(200, 2000, 1)
	#~ d = 150

	# Refractive Index of Film
	n_xshift = 180
	n_yshift = 3.5
	n_yscale = 1000
	n_film = n_yshift + n_yscale/(x**2 - (n_xshift)**2)

	# Refractive Index of Air and Substrate
	n_air = np.ones(len(x))
	n_sub = n_air[:] * 1.5

	# Film absorption
	k_film = 100/(200 - x)

	# Relabel
	n1 = n_air
	n2 = n_film + 1j*k_film
	n3 = n_sub

	# Fresnel Coefficients		(Yeh pg. 86)
	r12 = (n1-n2)/(n1+n2)
	r23 = (n2-n3)/(n2+n3)
	t12 = 2*n1/(n1+n2)
	t23 = 2*n2/(n2+n3)

	# phase
	phi = 2*np.pi*d*n2/x

	# amplitudes
	t = (t12*t23*np.exp(-1j*phi))/(1+r12*r23*np.exp(-2j*phi)) # F/A
	r = (r12+r23*np.exp(-2j*phi))/(1+r12*r23*np.exp(-2j*phi)) # B/A

	# Reflection and Transmission
	R = r.real**2 + r.imag**2
	T = (t.real**2 + t.imag**2)*(n3/n1)

calc_all(d)
#~ nplot = plt.plot(x, n1, x, n2, x, n3)
#~ plt.axis([200, 2000, 0, 10])
fig = plt.figure(figsize=(9,4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot()
ax2.plot(x, n_film, x, k_film)
line1, = ax1.plot(x, T)
line2, = ax1.plot(x, R)
line3, = ax1.plot(x, T/(1-R))

ax1.axis([200, 2000, 0, 1])
ax2.axis([200, 2000, 0, 5])
plt.show()
