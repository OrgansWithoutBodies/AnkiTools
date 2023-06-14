from bs4 import BeautifulSoup
import json

# TODO add on if already exists
def parseITalkiChatlog(filePath):
    parsedFile=BeautifulSoup(open(filePath,'r'),features="html.parser")
    messages=parsedFile.findAll('div',id=lambda x: x and x.startswith('Message-'))
    for ii in range(len(messages)):
        msg=messages[ii]
        if msg.find('div',{'class':lambda x:x and x.find('Template01')!=-1}):
            msg.decompose()
 
    parsedMessages=[msg.text.strip('\n').strip(' ').strip('\n').replace('  ',' ') for msg in messages]
    filtered=[]
    for msg in parsedMessages:
        if msg!='':
            filtered.append(msg)
    return filtered
    
def writeItalkiChatlog(messages,filePath):
    try:
        with open(filePath,'r') as existingFile:
            existingMessages=json.load(existingFile)
            messages=existingMessages+messages
    except:
            pass
    with(open(filePath,'w')) as file:
        json.dump(messages, file)

def parseThenWrite(filePath):
    folder=filePath.split('Nachrichten italki.html')[0]
    messages=parseITalkiChatlog(filePath)
    writeItalkiChatlog(messages, folder+'chatlog.json') 