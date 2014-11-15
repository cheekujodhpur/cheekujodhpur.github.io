#!/usr/bin/env python

import cgi
import cgitb
import numpy as np
from scikits.audiolab import wavread
import math
import xlrd
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.externals import joblib
cgitb.enable(display=1, logdir="/home/cheeku/log")

form = cgi.FieldStorage()
print "Content-type: text/html\n\n"
tmpf = open("tmp.wav","wb")
tmpf.write(form['wav'].value)
tmpf.close()
scmed = 0
scmean = 0
scmax = 0
scmin = 0
sfluxmed = 0
sfluxmean = 0
intmode = 0
pitmean = 0
pitmed = 0
flatmean = 0
flatmed = 0

s,fs,enc = wavread("tmp.wav")
s = np.array(s)
s = s/max(abs(s))

Frame_size=20.0
Frame_shift = 10.0

y = s
reconsine = y
Frame_size = Frame_size/1000.0
Frame_shift = Frame_shift/1000.0

secondpeak = []
scarr = []
spcroll = []
spflux = []
spcrest = []
spflatness = []
spspread = []
amplitude = []
pitch = []
pitch1 = []
dip_bin = []
dip_amp = []
max_amp_bin = []
max_amp = []
peaks = []
peakpeak = []
max2_amp = []
max2_bin = []
atimbre = []

max_value = max(abs(y))
y = y/max_value

Frame_length = Frame_size*fs
sample_shift = Frame_shift*fs

#code for 'w = hamming(...)' comes here, needed before I proceed.

w = np.hamming(Frame_length)
dftylast = 0
for i in range(int(math.floor(len(y)/sample_shift)-math.ceil(Frame_length/sample_shift))):
	k,jj = 0,0
	yy = []
	yyy = []
	for j in range(int(i*sample_shift),int(i*sample_shift+Frame_length)):
		yy.insert(k,y[j]*w[jj])
		yyy.insert(k,y[j])
		jj,k = jj+1,k+1
	dfty = abs(np.fft.fft(yy))
	yy = np.array(yy)
	dftyp = []
	for it in range(len(yy)):
		dftyp.append(math.atan2(yy[it].imag,yy[it].real))
		
	scn,scd,add,sf,ismax = 0,0,0,0,0
	q,sctimbre,geo,jj = 0,0,1,0
	M = len(dfty)/2
	for p in range(M):
		scn = scn + (p+1)*dfty[p]*dfty[p]
		scd = scd + dfty[p]*dfty[p]
		add = add + dfty[p]
		geo = geo*dfty[p]
		if dfty[p]>ismax:
			ismax = dfty[p]
		else:
			ismax = ismax
		if p>0 and p<M-1:
			if dfty[p]>dfty[p-1] and dfty[p]>dfty[p+1]:
				peaks.insert(q,[])
				peaks[q].insert(1,p)
				peaks[q].insert(0,dfty[p])
				peaks[q].insert(2,dftyp[p])
				sctimbre = sctimbre + dftyp[p]
				q = q+1	
		if i>0:
			sf = sf + (dfty[p]-dftylast[p])*(dfty[p]-dftylast[p])
		else:
			sf = 0
	s = 0
	length = len(yyy)
	acf_clip = np.correlate(yyy[:len(yyy)/2],yyy[:len(yyy)/2],"full")
	lenacf_clip = len(acf_clip)
	max_acfclip,max_acfclip_bin = max(acf_clip),np.argmax(acf_clip)
	for acfclip_bin in range(max_acfclip_bin,lenacf_clip-1):
		if acf_clip[acfclip_bin-1]>=acf_clip[acfclip_bin] and acf_clip[acfclip_bin+1]>=acf_clip[acfclip_bin]:
			dip_bin = np.append(dip_bin,acfclip_bin)
			dip_amp = np.append(dip_amp,acf_clip[acfclip_bin])
	
	dip_bin = np.array(dip_bin)[np.newaxis].T
	dip_amp = np.array(dip_amp)[np.newaxis].T
	dipMin_amp,Min_bin = min(dip_amp),np.argmin(dip_amp)
	dipMin_bin = dip_bin[Min_bin]
	max2_amp.insert(i,max(acf_clip[int(dipMin_bin):lenacf_clip]))
	max2_bin.insert(i,np.argmax(acf_clip[int(dipMin_bin):lenacf_clip]))
	max2_bin[i] = max2_bin[i] + dipMin_bin - 1 - max_acfclip_bin
	if i == 0:
		max2_bin[i] = max2_bin[i]
	else:
		max2_bin[i] = (max2_bin[i-1]+max2_bin[i])/2.0
	pitch1 = np.append(pitch1,fs*(1.0/(max2_bin[i]+1)))

	for r in range(1,q-1):
		if peaks[r][0]>peaks[r-1][0] and peaks[r][0]>peaks[r+1][0]:
			peakpeak.insert(s,[])
			peakpeak[s].insert(1,peaks[r][1])
			peakpeak[s].insert(0,peaks[r][0])
			peakpeak[s].insert(2,peaks[r][2])
			s = s+1

	np.sort(peakpeak,axis=0)
	peakpeaksorted = np.flipud(peakpeak)
	np.sort(peaks,axis=0)
	peakssorted = np.flipud(peaks)
	energy = float(add)/M
	sc = float(scn)/scd
	ssn = 0
	sctimbre = sctimbre - q*peaks[1][1]
	for p in range(M):
		ssn = ssn + (p+1-sc)*(p+1-sc)*dfty[p]
	ss = float(ssn)/scd
	ss = ss**0.5
	geo = geo**(1.0/M)
	
	sfl = float(geo)/energy
	spc = float(ismax)/energy
	add = 0.85*add
	scc = 0
	for p in range(M):
		scc = scc + dfty[p]
		if scc>=add:
			break	
	
	dftylast = dfty
	amplitude.insert(i,20*math.log10(add/0.85))
	pitch.insert(i,peakpeaksorted[0][1]/Frame_size)
	secondpeak.insert(i,peakpeaksorted[1][1]/Frame_size)
	spcroll.insert(i,scc)
	scarr.insert(i,sc)
	spflux.insert(i,sf)
	spcrest.insert(i,spc)
	spflatness.insert(i,sfl)
	spspread.insert(i,ss)
	atimbre.insert(i,sctimbre)

import wave
import contextlib
fname = 'tmp.wav'
with contextlib.closing(wave.open(fname,'r')) as f:
	frames = f.getnframes()
	rate = f.getframerate()
	duration = frames / float(rate)

tmp = [duration,np.median(pitch1),np.median(scarr),np.median(spflux)]
testdata = np.array(tmp)
y_fit = joblib.load('model.pkl')
y_pred = y_fit.predict(testdata)

print "Prediction: "
print y_pred[0]

print "</html>"
