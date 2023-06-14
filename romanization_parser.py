import csv
import json
rawFile = '/home/v/Projects/langs/uyghur/raw_romanization_table.csv'
ipaDict=dict()
UYYDict=dict()
ALALCDict=dict()
ULYDict=dict()
n=0
def addTerm(dct,ky,vl):
    dct[ky.strip('\u200e').strip(' ')]=vl.strip(' ').split(' ')[-1]
with open(rawFile) as csvFile:
    reader=csv.reader(csvFile)
    for row in reader: 
        if(n>0):
            addTerm(ipaDict,row[1],row[0])
            addTerm(UYYDict,row[1],row[2])
            addTerm(ALALCDict,row[1],row[3])
            addTerm(ULYDict,row[1],row[4])

        n=n+1
# TODO remove duplicate terms
json.dump(ipaDict,open('./ipaRomanization.json','w'))
json.dump(UYYDict,open('./UYYRomanization.json','w'))
json.dump(ALALCDict,open('./ALALCRomanization.json','w'))
json.dump(ULYDict,open('./ULYRomanization.json','w'))
