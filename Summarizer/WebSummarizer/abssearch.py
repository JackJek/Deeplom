import os
import re
library = {
            'numbr':[],
            'opred':['называется', 'известен, как','- это', '– это', 'образуют'],
            'types':['виды', 'вида', 'тип', 'таковы', 'такие, как', 'функци', 'свойства'],
            #predOpr предложение которое несет суть предложения содержащего определение.
            'predOpr' :['является', 'пример', 'вследствие', 'результатом', 'этого', 'таким образом', 'В нем', 'Оно', 'Такой', 'Такое', 'из них', 'их', 'где', 'В частности']

}
#убираем перенос после числа с точкой
def prep():
    for num in range(0, 30):
        library['numbr'].append(str(num + 1) + '.')

def abs():
    InFile = open('../ref.txt', 'r+')
    OutFile = open('../refing.txt', 'w')
    for line in InFile:
        for i in range(0, len(library['numbr'])):
            if library['numbr'][i] in line:
                line = re.sub(r'\n', '', line)
        OutFile.write(line)
    InFile.close()
    os.remove('../ref.txt')
    OutFile.close()



#коррекция на сокращение от лат.
'''убирает перенос в заголовках'''