import genanki
import random
import csv
import requests
from io import StringIO
italkiIds={
    'UY':593886596,
    'VN':599225666,
    'ES':479850695,
    'LT':251303196,
    'ZH':820550840,
    }
def generateAnkiDeck(deckName,terms,tranTerms,romTerms=[],examples=[],segmentations=[],fixedID=None,subDir=''):
    inclRomanization=len(romTerms)>0
    inclExamples=len(examples)>0
    deckId = random.randint(0,999999999) if fixedID == None else fixedID
    modelId = random.randint(0,999999999) if fixedID == None else fixedID

    modelFields = [
                            {'name': 'Term'},
                            {'name': 'Translation'},
                          ]
    
    modelTemplates=[
            {'name':"target>english",
             'qfmt':"{{Term}}",
             'afmt':'{{FrontSide}}<hr id="answer">{{Translation}}'
             },
            {'name':"english>target",
             'qfmt':"{{Translation}}",
             'afmt':'{{FrontSide}}<hr id="answer">{{Term}}'
             },
            
        ]
    if(inclRomanization):
        modelFields.append({'name':'Romanization'})
        modelTemplates[0]['qfmt']="{{Term}}<hr id='romanization'>{{Romanization}}"
        modelTemplates[1]['afmt']="{{FrontSide}}<hr id='answer'>{{Term}}<hr id='romanization'>{{Romanization}}"
    if(inclExamples):
        modelFields.append({'name':'Example'})
        
        #TODO terrible pattern
    ignoreSegmentations=segmentations==[]
    usingSegmentations=[1] if ignoreSegmentations else set(segmentations)
    print(usingSegmentations)
    for ss in usingSegmentations:
        try:
            
            if(int(ss)>0):
                usingDeckName=deckName if ignoreSegmentations else deckName+'::'+'segment-'+ss
                deck=genanki.Deck(deckId,usingDeckName)
                model=genanki.Model(modelId,
                                    '{}-model'.format(deckName),
                                     fields=modelFields,
                                     templates=modelTemplates
                                    )
                for ii in range(len(terms)):
                    if(ignoreSegmentations or segmentations[ii]==ss):
                        fields=[terms[ii],tranTerms[ii]]
                        if(inclRomanization):
                            fields.append(romTerms[ii])
                        deck.add_note(genanki.Note(model=model,fields=fields))
                
                genanki.Package(deck).write_to_file(subDir+'{0}{1}.apkg'.format(deckName,'' if ignoreSegmentations else '-'+ss))
        except:
            pass

def getTermDictsFromCSV(file,deckName,termColumn,englishColumn,romanizationColumn=None,exampleColumn=None,segmentationColumn=None,ignoreRows=[]):
    terms=[]
    englishes=[]
    romanizations=[]
    examples=[]
    segmentations=[]
    
    reader=csv.reader(file)
    ii=0
    for line in reader:
    
        if ignoreRows.count(ii)==0: 
            terms.append(line[termColumn])
            englishes.append(line[englishColumn])
            if(romanizationColumn):
                romanizations.append(line[romanizationColumn])
            if(exampleColumn):
                examples.append(line[exampleColumn])
            if(segmentationColumn):
                segmentations.append(line[segmentationColumn])
        ii=ii+1
    return [deckName,terms,englishes,romanizations,examples,segmentations]
    # TODO orderColumn? (IE rearrange everything by order in this column, for gradual ramp up in difficulty)
def ankiDeckFromCSV(deckName,csvFilePath,termColumn,englishColumn,romanizationColumn=None,exampleColumn=None,segmentationColumn=None,ignoreRows=[]):
    
    with open(csvFilePath,'r') as file:
      [deckName,terms,englishes,romanizations,examples,segmentations]= getTermDictsFromCSV(file,deckName,termColumn,englishColumn,romanizationColumn,exampleColumn,segmentationColumn,ignoreRows)
    generateAnkiDeck(deckName,terms=terms,tranTerms=englishes,romTerms=romanizations,examples=examples,segmentations=segmentations)
 
def ankiDeckFromGoogleSheet(deckName,googleSheetUrl,termColumn,englishColumn,romanizationColumn=None,exampleColumn=None,segmentationColumn=None,ignoreRows=[]):
    
    response = requests.get(googleSheetUrl+'/export?format=csv')
    assert response.status_code == 200, 'Wrong status code'
    print(response.content)
    
    content = response.content.decode()
    pseudoFile = StringIO(content)
    [deckName,terms,englishes,romanizations,examples,segmentations]= getTermDictsFromCSV(pseudoFile,deckName,termColumn,englishColumn,romanizationColumn,exampleColumn,segmentationColumn,ignoreRows)
    generateAnkiDeck(deckName,terms=terms,tranTerms=englishes,romTerms=romanizations,examples=examples,segmentations=segmentations)
 