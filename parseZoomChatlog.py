import json

import re
reMatcher="[0-9][0-9]:[0-9][0-9]:[0-9][0-9] From  Nguyen Khoa Do  to  Everyone"

name='Nguyen Khoa Do'
def splitTextByMessage(filePath):
    with open(filePath,'r') as file:
        messages=[]
        nextLineMessage=False
        for line in file:
            if(nextLineMessage):
                messages.append(line.strip('\t').strip('\n'))
                nextLineMessage=False
            if(re.match(reMatcher, line)!=None):
                nextLineMessage=True
            
    return messages


def writeZoomChatlog(messages,filePath):
    try:
        with open(filePath,'r') as existingFile:
            existingMessages=json.load(existingFile)
            messages=existingMessages+messages
    except:
            pass
    with(open(filePath,'w')) as file:
        json.dump(messages, file)

def parseThenWrite(filePath):
    folders=filePath.split('/')[0:-1]
    folder='/'.join(folders)+'/'
    messages=splitTextByMessage(filePath)
    
    writeZoomChatlog(messages, folder+'zoomChatlog.json') 