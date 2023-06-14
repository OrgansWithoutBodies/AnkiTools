import camelot
import math
import PyPDF2 as pdf
santi = r'/home/v/Downloads/三体 ( PDFDrive ).pdf'

reader=pdf.PdfReader(santi) 

oddStr=' \n 地球往事·\n三体'
evenStr=' \n 中国科幻基石丛书'


chapterPages=[reader.get_destination_page_number(dest) for dest in reader.outline[6] ]
postScriptPageStart=reader.get_destination_page_number(reader.outline[7]) 
for ii in range(len(chapterPages)):
    text=[]

    chapterStart=chapterPages[ii]
    nextChapterStart=chapterPages[ii+1] if ii<len(chapterPages)-1 else postScriptPageStart
    for page in range(chapterStart,nextChapterStart):
        
        pageTextRaw=reader.pages[page].extract_text()
        pageTextPretty=pageTextRaw.strip(evenStr).strip(oddStr).replace(' \n',"{{NEWLINEPRE}}").replace('\n ','{{NEWLINEPOST}}').replace('\n','').replace("{{NEWLINEPRE}}",' \n').replace('{{NEWLINEPOST}}','\n ')
        text.append(pageTextPretty)
        
 
    textStr=''.join(text) 

    with open('santi/santi-chapter-'+str(ii+1   )+'.txt','w') as file:
        file.write(textStr)