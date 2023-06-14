from deep_translator import GoogleTranslator
import time
import json
def translateTerm(term,sourceLang='ug',targetLang='en'):
    return GoogleTranslator(source=sourceLang, target=targetLang).translate(term)
cachedTranslatedTerms=dict()
def translateTermList(termList,overwriteSource=dict(),sourceLang='ug',targetLang='en'):
    translatedTerms={**overwriteSource,**cachedTranslatedTerms}
    for term in termList:
        if(term not in translatedTerms.keys()):
            try:
                translatedTerm=translateTerm(term,sourceLang=sourceLang,targetLang=targetLang)
                translatedTerms[term]=translatedTerm
                cachedTranslatedTerms[term]=translatedTerm
                print(translatedTerm)
            except:
                print("FAILED",termca)
            time.sleep(2)
    return translatedTerms
# def removeDuplicateTerms()
# TODO get terms from unicode range?
# roughTranslations=json.dump(translatedTerms,'./roughTranslations.json')
def cleanupTermList(termlist,dels=[],strips=[],splits=[]):
    splitted=[] 
    stripped=[]
    deld=[]
    remd=[]
    if(len(splits)>0):
        for val in termlist:
            isAdded=False
            for split in splits:
                if split in val:
                    for retVal in val.split(split):
                        splitted.append(retVal)
                        isAdded=True
            if not isAdded:
                splitted.append(val)
    else:
        splitted=termlist
    if(len(strips)>0):
        for val in splitted:
            retVal = val
            for strip in strips:
                retVal=retVal.strip(strip)
            stripped.append(retVal)
    else:
        stripped=splitted
    if(len(dels)>0):
        for val in stripped:
            retVal=val
            for d in dels:
                retVal=retVal.replace(d,'')
            deld.append(retVal)
    
        for val in deld:
            if(val!=''):
                remd.append(val)
    else:
        remd=stripped
    return remd

def rawTextToTermList(rawText):
    termList = cleanupTermList(rawText.split(' '),DEL,STRIP,SPLIT)
    dedupedList = list(set(termList))
    return dedupedList
DEL=['0','1','2','3','4','5','6','7','8','9','\n','»','-']
STRIP=['"','\n','،','«','»','.',',','\u200f',';',':','؛','“',')','(','-']
SPLIT=['\n','-',' ','<','>']