# ./lineCount.py fileName

import sys

countFileName = sys.argv[1]

i = 1
lineCount = 0
defectedLineCount = 0
defectedLines = []
with open(countFileName, 'r', encoding='utf-8') as countFile:
    while True:
        try:
            line = countFile.readline()
            if not line:
                break
            if line == '\n': continue
            lineCount+=1
            # print(lineCount,line,end='')
        except:
            defectedLines.append(i)
            defectedLineCount+=1
        i+=1

    countFile.close()

print('line count :', lineCount)
print("couldn't read :", defectedLineCount)
print(defectedLines)