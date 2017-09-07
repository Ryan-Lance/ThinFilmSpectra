# Ryan Lance 
# 17-0905
# Tate Lab
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk				#http://www.python-course.eu/tkinter_sliders.php

# Parameter Sliders
master = tk.Tk()
thickness = tk.Scale(master, from_=10, to=250, length = 300,
 orient=tk.HORIZONTAL)
thickness.pack()
parameter1 = tk.Scale(master, from_=0,  to=1000, length = 300,
 orient=tk.HORIZONTAL)
parameter1.pack()

# Button press
def get_parameters():
	d = thickness.get()
	parameter1.get()
	calc_all(d)
	#~ line1.set_ydata(T)
	#~ line2.set_ydata(R)
	line1.set_ydata(Tb)
	line2.set_ydata(Rb)
	line3.set_ydata(Tb/(1-Rb))
	line6.set_ydata(T)
	line7.set_ydata(R)
	line8.set_ydata(T/(1-R))
	fig.canvas.draw()
tk.Button(master, text = 'Enter',command=get_parameters).pack()

def calc_all(d):
	global x, T, R, Tb, Rb, n_film, k_film
	
	# All units in nanometers
	x = np.arange(200, 2000, 1)

	# Refractive Index of Film	(Cauchy)
	n_yshift = 3.5
	n_yscale = 500
	n_xshift = 150
	n_film = n_yshift + n_yscale/(x**2 - n_xshift)

	# Refractive Index of Air and Substrate
	n_air = np.ones(len(x))
	n_sub = n_air[:] * 1.5

	# Film absorption
	k_film = 200/(150 - x)

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
	phi1 = 2*np.pi*d*n2/x
	phi2 = 2*np.pi*d*n2/(x[:]/2)	# Let the second order light 
									#	have 1/2 the lambda

	# amplitudes
	t1 = (t12*t23*np.exp(-1j*phi1))/(1+r12*r23*np.exp(-2j*phi1)) # F/A
	r1 = (r12+r23*np.exp(-2j*phi1))/(1+r12*r23*np.exp(-2j*phi1)) # B/A
	
	t2 = (t12*t23*np.exp(-1j*phi2))/(1+r12*r23*np.exp(-2j*phi2)) # F/A
	r2 = (r12+r23*np.exp(-2j*phi2))/(1+r12*r23*np.exp(-2j*phi2)) # B/A

	# Reflection and Transmission
	R1 = r1.real**2 + r1.imag**2
	T1 = (t1.real**2 + t1.imag**2)*(n3/n1)
	R2 = r2.real**2 + r2.imag**2
	T2 = (t2.real**2 + t2.imag**2)*(n3/n1)
	R = R1
	T = T1
	
	# b for bad	
	I_extra = 0.5
	Rb = R1 + R2[:] * I_extra			# Let the second order light 
	Tb = T1 + T2[:] * I_extra			# 	have 1/2 the intensity
	N = 1 + I_extra
	Rb /= N
	Tb /= N


# Do the calculation
d = 150
calc_all(d)

# Plot everything
fig = plt.figure(figsize=(10,4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot()
line1, = ax1.plot(x, Tb)
line2, = ax1.plot(x, Rb)
line3, = ax1.plot(x, Tb/(1-Rb))

ax2.plot()
line6, = ax2.plot(x, T)
line7, = ax2.plot(x, R)
line8, = ax2.plot(x, T/(1-R))

ax1.axis([200, 2000, 0, 1])
ax2.axis([200, 2000, 0, 1])
plt.show()
