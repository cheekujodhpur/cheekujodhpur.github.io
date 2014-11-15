#!/usr/bin/env python

#Project: AviPulse
#Author: Riddhish et. al. (matlab)
#Translation: Kumar Ayush (python)
#Methodology: You need a web form to post a syllable file in .wav format in multipart encoding.

#import CGI libraries
import cgi
import cgitb

#numpy
import numpy as np

#to read a wave
from scikits.audiolab import wavread

#Python math library
import math

#To read an excel file
import xlrd

#The Gaussian Naive Bayes Machine Learner Class
from sklearn.naive_bayes import GaussianNB as GNB

#To load the saved model state
from sklearn.externals import joblib

#Enable errors
#use log directory for logdir, set display=0 if don't want error display on browser, or require a custom message
cgitb.enable(display=1, logdir="/home/cheeku/log")

#Define the cgi form object
form = cgi.FieldStorage()

#HTML headers
print "Content-type: text/html\n\n"

#Write the multipart sound data to a temporary file
tmpf = open("tmp.wav","wb")
tmpf.write(form['wav'].value)
tmpf.close()

#Variable initializations
scmed = 0	#Spectral Centroid Median
scmean = 0	#Spectral Centroid Mean
scmax = 0	#Spectral Centroid Max
scmin = 0	#Spectral Centroid Min
sfluxmed = 0	#Spectral Flux Median
sfluxmean = 0	#Spectral Flux Mean
intmode = 0	
pitmean = 0	#Pitch Mean
pitmed = 0	#Pitch Median
flatmean = 0	#Spectral Flatness Mean
flatmed = 0	#Spectral Flatness Median

#Read the sound, stored in the temporary file
#'s' is data,'enc' is encoding
s,fs,enc = wavread("tmp.wav")
s = np.array(s)
s = s/max(abs(s))	#normalization, to imitate matlab's wavread

Frame_size=20.0		#Parameter of computation
Frame_shift = 10.0	#Parameter of computation

#Variable recasts and normalizers, prep for computation
y = s		
reconsine = y
Frame_size = Frame_size/1000.0
Frame_shift = Frame_shift/1000.0

#Empty lists
secondpeak = []
scarr = []	#Spectral Centroid Array
spcroll = []
spflux = []	#for Spectral Flux calculaion
spcrest = []
spflatness = []	#for Spectral Flatness calculation
spspread = []
amplitude = []	#for Amplitude calculation
pitch = []
pitch1 = []	#for Pitch calculations
dip_bin = []
dip_amp = []
max_amp_bin = []
max_amp = []
peaks = []
peakpeak = []
max2_amp = []
max2_bin = []
atimbre = []

#Re-normalization
max_value = max(abs(y))
y = y/max_value

#Scale Frame size and length
Frame_length = Frame_size*fs
sample_shift = Frame_shift*fs

w = np.hamming(Frame_length)	#create a hamming window of given length

dftylast = 0	#empty variable to store dft result for previous computation
for i in range(int(math.floor(len(y)/sample_shift)-math.ceil(Frame_length/sample_shift))):
	#Fourier Transform with data scaled using a sliding hamming window, sliding across frames
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
	
	#computation, computation, computation	
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

	#convolutions and computations
	s = 0
	length = len(yyy)
	acf_clip = np.correlate(yyy[:len(yyy)/2],yyy[:len(yyy)/2],"full")
	lenacf_clip = len(acf_clip)
	max_acfclip,max_acfclip_bin = max(acf_clip),np.argmax(acf_clip)
	for acfclip_bin in range(max_acfclip_bin,lenacf_clip-1):
		if acf_clip[acfclip_bin-1]>=acf_clip[acfclip_bin] and acf_clip[acfclip_bin+1]>=acf_clip[acfclip_bin]:
			dip_bin = np.append(dip_bin,acfclip_bin)
			dip_amp = np.append(dip_amp,acf_clip[acfclip_bin])
	
	dip_bin = np.array(dip_bin)[np.newaxis].T	#row to column vector
	dip_amp = np.array(dip_amp)[np.newaxis].T	#row to column vector
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

	np.sort(peakpeak,axis=0)	#sort ascending
	peakpeaksorted = np.flipud(peakpeak)	#reverse, effectively sort descending
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
	
	dftylast = dfty	#current dfty to dftylast assignment

	#populate result arrays
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

#Since we have no good way of seperating syllables in a sound file
#the following code gets the length of the file in seconds
#assuming it is a single syllable
import wave
import contextlib
fname = 'tmp.wav'
with contextlib.closing(wave.open(fname,'r')) as f:
	frames = f.getnframes()
	rate = f.getframerate()
	duration = frames / float(rate)

tmp = [duration,np.median(pitch1),np.median(scarr),np.median(spflux)]	#store relevant values in an array
testdata = np.array(tmp)	#prepare testdata
y_fit = joblib.load('model.pkl')	#load model from file
y_pred = y_fit.predict(testdata)	#get predicted label

#Print predicted label
print "Prediction: "
#print y_pred[0]

#open workbook and load relevant sheet
workbook = xlrd.open_workbook('data2.xlsx')
datasheet = workbook.sheet_by_name('data without outliers manual')

#print name of bird based on id
i = 0
while datasheet.cell_value(i,6) != int(y_pred[0]):
	i = i+1

print datasheet.cell_value(i,0)

#close the output
print "</html>"
