# importing required modules
import pandas as pd
import PyPDF2
import tabula
import camelot
testFP = '/home/v/Projects/langs/uyghur/italki/resources/Hazirki zaman uygur tili kollanmisi-1.pdf'


def getFileReader(filePath):
    # creating a pdf file object
    pdfFileObj = open(filePath, 'rb')

    # creating a pdf reader object
    return PyPDF2.PdfReader(pdfFileObj)

    # # printing number of pages in pdf file
    # print(len(pdfReader.pages))

    # # creating a page object
    # pageObj = pdfReader.pages[32]

    # # extracting text from page
    # print(pageObj.extract_text())

    # # closing the pdf file object
    # pdfFileObj.close()

def extractTable(filePath,pages):
    tables = camelot.read_pdf(testFP, pages=pages)
    dfs = [table.df for table in tables]
    wholeTable = pd.concat(dfs,ignore_index=True) 
    return wholeTable 

def parseTable(wholeTable: pd.DataFrame): 

    wholeTable.columns = wholeTable.iloc[0]
    wholeTable = wholeTable.drop(wholeTable.index[0])
    wholeTable['Less.'] = wholeTable['Less.'].replace(
        'intro', '0').replace('', '-1').astype(int)
    wholeTable = wholeTable.sort_values('Less.')
    fixedScript = [term[::-1] for term in wholeTable['Arabic-script Uyghur']]
    wholeTable['Arabic-script Uyghur'] = fixedScript

    wholeTable.to_csv('uyghur-book-terms-camelot.csv') 

endOfBookTableUYEN = '263-293'
endOfBookTableENUY = '295-326'
# wholeTable=pd.concat(dfs)
# wholeTable.columns=wholeTable.iloc[0]
# wholeTable=wholeTable.drop(wholeTable.index[0])
# wholeTable=wholeTable['Less.'].replace('intro','0').replace('','-1').astype(int)
# wholeTable=wholeTable.sort_values('Less.')


def cleanupTable():
    # put terms matching regex str into appropriate column
    # fix reversed parens
    pass
