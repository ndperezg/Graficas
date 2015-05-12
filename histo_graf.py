#!/usr/bin/env python2.7
"""
Programa que realiza estadisticas basicas a partir de un select.out 
(formato nordico).

(c) 2014 Nelson Perez <nperez@sgc.gov.co>

v0.1 - 20140312 - N. Perez
20150512-- agragado a github
"""

import sys
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, YearLocator, MonthLocator, DayLocator, AutoDateLocator

os.system('report select.out report.inp')

namereport='report.out'

if str(os.path.isfile(namereport))=='False':
	print "No Input file: "+namereport
	sys.exit()

report = open('report.out','r')

year, MM, dd, hh, mm, sec, lat, lon, dep, err_lat, err_lon, err_dep,  ml, rms, gap, nsta, mw  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

counter=0
for line in report:
	counter+=1
	if counter>1:
		year.append(int(line[1:5]))
		MM.append(int(line[6:8]))	
		dd.append(int(line[8:10]))
		hh.append(int(line[10:13]))
		mm.append(int(line[13:15]))
		sec.append(float(line[16:18]))
		lat.append(float(line[20:28]))
		lon.append(float(line[34:43]))
		dep.append(float(line[49:55]))
		err_lat.append(float(line[29:34]))
		err_lon.append(float(line[44:49]))	
		err_dep.append(float(line[56:61]))
		nsta.append(int(line[63:66]))
		rms.append(float(line[68:71]))
		gap.append(int(line[70:74]))
		if line[76:79] == '   ':
			ml.append(0)
		else:
			ml.append(float(line[76:79]))
		if line[81:84] == '   ':
			mw.append(0)
		else:
			mw.append(float(line[81:84]))

"""
for i in range(len(ml)):
	print i, type(err_lat[i]), type(ml[i]), gap[i], ml[i]
	if ml[i] == '   ':
		print i, 'ERROR!!!', year[i], MM[i], dd[i]
"""



fig=plt.figure(1, figsize=(20,20))

plt.subplot(321)
plt.grid('on')
plt.plot(ml, err_lat, 'bo')
plt.title("Error en latitud vs ML",fontsize=16)
#plt.xlabel('Magnitud Local (Ml)')
plt.ylabel('Error en latitud [km]',fontsize=16)
plt.ylim(0,max(err_lat)+0.1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(322)
plt.grid('on')
plt.plot(ml, err_lon, 'bo')
plt.title("Error en longitud vs ML",fontsize=16)
#plt.xlabel('Magnitud Local (Ml)')
plt.ylabel('Error en longitud [km]',fontsize=16)
plt.ylim(0,max(err_lon)+0.1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(323)
plt.grid('on')
plt.plot(ml, err_dep, 'bo')
plt.title("Error en Profundidad vs ML",fontsize=16)
#plt.xlabel('Magnitud Local (Ml)')
plt.ylabel('Error en profundidad [km]',fontsize=16)
plt.ylim(-0.1,max(err_dep)+0.1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(324)
plt.grid('on')
plt.plot(ml, nsta, 'bo')
plt.title("Numero de estaciones vs Ml",fontsize=16)
plt.xlabel('Magnitud Local (Ml)',fontsize=16)
plt.ylabel('Numero de estaciones',fontsize=16)
plt.ylim(0,max(nsta)+1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(325)
plt.grid('on')
plt.plot(ml, rms, 'bo')
plt.title("RMS vs Ml",fontsize=16)
plt.xlabel('Magnitud Local (Ml)',fontsize=16)
plt.ylabel('RMS')
plt.ylim(-0.03,max(rms)+0.1)
plt.xlim(0,max(ml)+0.1)
#plt.show()
fig.savefig('figura1.pdf',format='pdf')

"""
##conteo histograma:
bin_gap=[]
ar_gap= np.arange(0,360,5)
for i in range(len(ar_gap)):
	count=0
	for j in range(len(gap)):
		if ar_gap[i]<=gap[j]<ar_gap[i+1]:
			count+=1
	bin_gap.append(count)
print len(ar_gap), len(bin_gap)
print type(ar_gap[0]), type(bin_gap[0])
print ar_gap, bin_gap
"""
#Histogramas
plt.figure(2)
plt.subplot(221)
hist_gap=plt.hist(gap,bins=np.arange(0,360,10))
plt.xlabel('GAP (grados)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(222)
hist_ml=plt.hist(ml,bins=np.arange(0,9,0.5))
plt.xlabel('$M_l$',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(223)
hist_nsta=plt.hist(nsta,bins=np.arange(0,50,1))
plt.xlabel('Numero de estaciones',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)
plt.savefig('figura2.pdf')

plt.figure(3)
plt.subplot(221)
hist_errlat=plt.hist(err_lat,bins=np.arange(0,100,1))
plt.xlabel('Error en latitud (km)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(222)
hist_errlon=plt.hist(err_lon,bins=np.arange(0,100,1))
plt.xlabel('Error en longitud (km)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(223)
hist_errdep=plt.hist(err_dep,bins=np.arange(0,100,1))
plt.xlabel('Error en profundidad (km)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)
#plt.show()
plt.savefig('figura3.pdf')

plt.figure(4)
plt.subplot(111)
hist_errdep=plt.hist(dep,bins=np.arange(0,600,5))
plt.xlabel('Profundidad (km)',fontsize=16)
plt.ylabel('Numero de sismos',fontsize=16)
plt.savefig('figura4.pdf')

plt.figure(5)
plt.subplot(111)
hist_errdep=plt.hist(rms,bins=np.arange(0,2,0.1))
plt.xlabel('RMS',fontsize=16)
plt.ylabel('Numero de sismos',fontsize=16)
plt.savefig('figura5.pdf')
###HISTOGRAMA FECHAS

#plt.figure(3, figsize(20,20))

Dates = []

for fec in range(len(year)):
	Dates.append(str(year[fec])+'-'+str(MM[fec])+'-'+str(dd[fec])+'-'+str(hh[fec])+'-'+str(mm[fec]))
	Dates[fec] = datetime.datetime.strptime(Dates[fec], '%Y-%m-%d-%H-%M')
#	print fec, Dates[fec]

(hist, bin_edges) = np.histogram(date2num(Dates), 608)
print hist, bin_edges[:-1]
width = bin_edges[1] - bin_edges[0]
fig = plt.figure(6)
ax = fig.add_subplot(111)
ax.bar(bin_edges[:-1], hist, width=width)
ax.set_xlim(bin_edges[0], date2num(Dates[-1]))
ax.set_ylabel('Numero de eventos')
ax.set_title('Ocurrencia de Eventos')
ax.xaxis.set_major_locator(AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax.xaxis.set_minor_locator(MonthLocator())
ax.format_xdata = DateFormatter('%Y-%m-%d')
ax.grid(True)
fig.autofmt_xdate()
plt.savefig('figura6.pdf')
plt.show()
