#!/usr/bin/env python
from time import sleep
from drive import RosAriaDriver

from math import sin, cos, sqrt
from random import randint

import numpy as np
import pylab as pl
from matplotlib import collections  as mc

robot=RosAriaDriver('/PIONIER1')
skan=robot.ReadLaser()

s=3	# liczba losowanych punktow
c=70	# pewnosc
blad=0.05# blad
n=15	# liczba prob
pomiary=[] # tablica
x=0
y=0
tf=[]	# branie pod uwage punktu
taba=[]
tabb=[]


def wyliczxy(wiazka, odleglosc):
	kat=wiazka*0.36-90
	krad=kat*3.14/180
	x=odleglosc*cos(krad)
	y=odleglosc*sin(krad)
	return(x,y)

# Zbieranie pomiarow pojedynczych punktow
i=0
while i<512:
	#print(i)
	pomiary.append(skan[i])
	#print(pomiary[i])
	if pomiary[i]<6:
		tf.append(True)
	else:
		tf.append(False)
	#print(tf[i])
	i=i+1

# Zamiana na x i y
i=0
pomiaryx=[]
pomiaryy=[]
while i<512:
	(x,y)=wyliczxy(i, pomiary[i])
	pomiaryx.append(x)
	pomiaryy.append(y)
	#print(pomiaryx[i], pomiaryy[i])
	i=i+1

# Start petli

k=0
while(k<n):

	# Losowanie trzech punktow

	A = randint(0,511)
	B = randint(0,511)
	C = randint(0,511)
	licznikbezpieczenstwa=0
	while(tf[A]==False or tf[B]==False or tf[C]==False):
		if(tf[A]==False):
			A=randint(0,511)
		if(tf[B]==False):
			B=randint(0,511)
		if(tf[C]==False):
			C=randint(0,511)
		licznikbezpieczenstwa=licznikbezpieczenstwa+1
		if(licznikbezpieczenstwa>5000):
			break;
	#print(tf[A], tf[B], tf[C])


	# Wyliczanie wszystkich sum do wzoru na aproksymacje
	sumax=pomiaryx[A]+pomiaryx[B]+pomiaryx[C]
	sumay=pomiaryy[A]+pomiaryy[B]+pomiaryy[C]
	sumax2=pomiaryx[A]**2+pomiaryx[B]**2+pomiaryx[C]**2
	sumaxy=pomiaryx[A]*pomiaryy[A]+pomiaryx[B]*pomiaryy[B]+pomiaryx[C]*pomiaryy[C]
	
	# Metoda najmniejszych kwadratow
	a=(sumax*sumay-sumaxy*s)/(sumax**2-sumax2*s)
	print(a)
	b=(sumax*sumaxy-sumax2*sumay)/(sumax**2-sumax2*s)
	print(b)

	# Odleglosc punktu od prostej
	# Rownanie y=ax+b => ax-y+b=0
	i=0
	licznik=0
	indeksy=[]
	while i<512:
		if(tf[i]==True):
			d=abs(a*pomiaryx[i]-1*pomiaryy[i]+b)/sqrt(a**2+1)
			if(d<blad):
				licznik=licznik+1
				indeksy.append(i)
		i=i+1
	print("Liczba punktow w okolicy prostej: ")
	print(licznik)
	# Jezeli wiecej niz 5 punktow, zamieniamy true na false
	if licznik>=c:
		i=0
		taba.append(a)	
		tabb.append(b)
		while(i<len(indeksy)):
			tf[indeksy[i]]=False
			i=i+1
	k=k+1

i=0
fig, ax = pl.subplots()
while(i<len(taba)):
	a=taba[i]
	b=tabb[i]
	x1=-5
	x2=5
	y1=x1*a+b
	y2=x2*a+b
	lines=[[(x1,y1),(x2,y2)]]
	lc=mc.LineCollection(lines, colors=[0,0,0],linewidths=1)
	ax.add_collection(lc)
	ax.margins(0.1)
	i=i+1
pl.scatter(pomiaryx, pomiaryy)
ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
pl.show()

	
