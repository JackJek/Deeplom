from nltk.tokenize import sent_tokenize #разбиение на предложения
from rutermextract import TermExtractor #ключевые слова для темы
from django.conf import settings
import os
import re
import time
tm = str(int(time.time()))
themestr = ''
library = {
            'numbr':[],
            'opred':['называется', 'известен, как','- это', '– это', '–', 'образуют'],
            'types':['виды', 'вида', 'тип', 'таковы', 'такие, как', 'Функци', 'свойства'],
            #predOpr предложение, которое несет суть предложения содержащего определение.
            'predOpr' :['является', 'пример', 'вследствие', 'результатом', 'этого', 'таким образом', 'В нем', 'Оно', 'Такой', 'Такое', 'из них', 'их', 'где', 'В частности','Эта', 'В случае','Его','они','Отсюда следует', 'Потом', 'Затем']
}


def tokenize(f):
    for num in range(0, 40): #prep
        library['numbr'].append(str(num + 1) + '.')

    tempFile = open(settings.MEDIA_ROOT+ tm + 'temp.txt','w')
    InFile = open(f, 'r+') #создать свой текстовый
    OutFile = open(settings.MEDIA_ROOT + tm + 'Ref.txt', 'w')

    text = InFile.read()
    sentences = sent_tokenize(text)
    for sents in sentences:
        sents = sents.replace('(от лат.', '')
        tempFile.write(sents.strip() + '\n')
    tempFile.close()
    tempFile = open(settings.MEDIA_ROOT + tm + 'temp.txt','r')
    for line in tempFile:
        for i in range(0, len(library['numbr'])):
            if library['numbr'][i] in line:
                line = re.sub(r'\n', '', line)
        OutFile.write(line)
    OutFile.close()
    InFile.close()
    tempFile.close()
    os.remove(settings.MEDIA_ROOT + tm + 'temp.txt')
    os.remove(f)

def summar(deep):
    prevLine = ''
    InFile = open(settings.MEDIA_ROOT + tm + 'Ref.txt', 'r+')
    OutFile = open(settings.MEDIA_ROOT + tm + 'Refing.txt', 'w')
    step = 1
    t = 0  # отступ+ защит от повторов в абзацах
    ruse = 0  # от повторов если и определение и виды
    # Глубин 0
    for line in InFile:
        for i in range(0, len(library['numbr'])):
            if library['numbr'][i] in line:
                if i > 9:
                    t -= 1
                t += 1
        if t > 0:
            ruse += 1
            OutFile.write((t - 1) * '  ' + line)
        t = 0

        if deep == 0:
            ruse = 0
            continue
        # Глубина 1
        for i in range(0, len(library['opred'])):
            if library['opred'][i] in line and ruse == 0:
                OutFile.write(3 * '  ' + line)
                ruse += 1

        if deep == 1:
            ruse = 0
            continue
        # Глубина 2
        for i in range(0, len(library['types'])):
            if library['types'][i] in line and ruse == 0:
                OutFile.write(4 * '  ' + line)
                ruse += 1

        if deep == 2:
            ruse = 0
            continue

        if deep == 3:
            step = 2
        else:
            step = 1
        # Глубина 3-4
        for i in range(0, len(library['predOpr']), step):
            if library['predOpr'][i] in line and ruse == 0:
                OutFile.write(3 * '  ' + prevLine.replace('\n', '') + line)
                prevLine = ''
                ruse += 1
        if ruse == 0:
            prevLine = line
        ruse = 0
    OutFile.close()
    InFile.close()
    os.remove(settings.MEDIA_ROOT + tm + 'Ref.txt')
    return  settings.MEDIA_ROOT + tm + 'Refing.txt'


def theme(theme):
    term_extractor = TermExtractor()
    themestr = term_extractor(theme, nested=True, strings=True)
    InFile = open (settings.MEDIA_ROOT + tm + 'Ref.txt','r')
    OutFile = open (settings.MEDIA_ROOT + tm + 'Refing.txt','w')
    for line in InFile:
        ruse = 0
        for i in range (0,len(themestr)):
            for k in range(0, len(library['predOpr']), 1):
                if themestr[i].lower() in line.lower() and ruse == 0 and library['predOpr'][k] in line:
                    OutFile.write(3 * '  ' + prevLine.replace('\n', '') + line)
                    prevLine = ''
                    ruse+=1
                elif themestr[i].lower() in line.lower() and ruse == 0:
                    OutFile.write(line)
                    ruse += 1
        if ruse == 0:
            prevLine = line
    OutFile.close()
    InFile.close()
    os.remove(settings.MEDIA_ROOT + tm + 'Ref.txt')
