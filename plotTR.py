from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Tkinter as tk				#http://www.python-course.eu/tkinter_sliders.php

#-----Global Variables-----#
global x_length
global parameters 
global spectra
global fig

x_length = 1801

fig = plt.figure(figsize=(11,4))

parameters = {
	'lambda': np.arange(200, 2000, 1),
	'thickness': 150,
	'intensityL2': 0.5
	}
spectra = {
	'T': np.zeros(x_length),
	'R': np.zeros(x_length),
	'Tb': np.zeros(x_length),
	'Rb': np.zeros(x_length)
	}
#--------------------------#

#---------Sliders----------#
master = tk.Tk()
thickness = tk.Scale(master, from_=10, to=300, length = 300,
					orient=tk.HORIZONTAL)
intensity = tk.Scale(master, from_=0,  to=100, length = 300,
					orient=tk.HORIZONTAL)
thickness.pack()
intensity.pack()

# Button press
def get_parameters():
	parameters['thickness'] = thickness.get()
	parameters['intensityL2'] = intensity.get()/100
	calc_all()
	lines[0].set_ydata(spectra['T'])
	lines[1].set_ydata(spectra['R'])
	lines[2].set_ydata(spectra['T']/(1-spectra['R']))
	lines[3].set_ydata(spectra['Te'])
	lines[4].set_ydata(spectra['Re'])
	lines[5].set_ydata(spectra['Te']/(1-spectra['Re']))
	lines[6].set_ydata(spectra['Tb'])
	lines[7].set_ydata(spectra['Rb'])
	lines[8].set_ydata(spectra['Tb']/(1-spectra['Rb']))
	fig.canvas.draw()
tk.Button(master, text = 'Enter',command=get_parameters).pack()
#--------------------------#

def calc_all():
	# All units in nanometers
	d = parameters['thickness']
	x = parameters['lambda']

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
	phi2 = 2*np.pi*d*n2/(x[:]*2)	# Let the second order light 
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
	
	# e for extra	
	I_extra = parameters['intensityL2']
	Re = R2 * I_extra
	Te = T2 * I_extra
	
	# b for bad
	N = 1 + I_extra
	Rb = (R1 + R2 * I_extra) / N
	Tb = (T1 + T2 * I_extra) / N
	
	spectra['T'] = T
	spectra['R'] = R
	spectra['Te'] = Te
	spectra['Re'] = Re
	spectra['Tb'] = Tb
	spectra['Rb'] = Rb

def plot_all():
	x = parameters['lambda']
	ax1 = fig.add_subplot(131)
	ax2 = fig.add_subplot(132)
	ax3 = fig.add_subplot(133)
	ax1.plot()
	ax2.plot()
	ax3.plot()
	ax1.axis([200, 2000, 0, 1])
	ax2.axis([200, 2000, 0, 1])
	ax3.axis([200, 2000, 0, 1])
	line1, line2, line3, = ax1.plot(x, spectra['T'],x, spectra['R'],
									x, spectra['T']/(1-spectra['R']))
	
	line4, line5, line6, = ax2.plot(x, spectra['Te'],x, spectra['Re'],
									x, spectra['Te']/(1-spectra['Re']))
	
	line7, line8, line9, = ax3.plot(x, spectra['Tb'],x, spectra['Rb'],
									x, spectra['Tb']/(1-spectra['Rb']))
	
	global lines
	lines = [line1, line2, line3, line4, 		\
			line5, line6, line7, line8,line9]
	
	plt.show()

# Run
calc_all()
plot_all()
while True:
	get_parameters()
