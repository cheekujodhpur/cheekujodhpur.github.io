#!usr/bin/env/python

import xlrd
import numpy as np
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.externals import joblib

workbook = xlrd.open_workbook('data2.xlsx') #open excel file
testsheet = workbook.sheet_by_name('test data')
tmp = []
for i in range(1,testsheet.nrows):
	tmp.append([testsheet.cell_value(i,j) for j in range(2,6)])

testdata = np.array(tmp)

y_fit = joblib.load('model.pkl')
y_pred = y_fit.predict(testdata)

print "Prediction is Bird Number %d" %(y_pred[0])

