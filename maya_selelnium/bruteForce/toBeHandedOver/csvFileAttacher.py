# ./csvFileAttacher.py targetFile sourceFile01 sourceFile02 ...

import sys

targetFileName = sys.argv[1]
targetFile = open(targetFileName, 'a+', encoding='utf-8')
headerLine = targetFile.readline()
if not headerLine:
    targetFile.write('tag,ques,ans\n')
elif 'tag,ques,ans' not in headerLine:
    targetFile.write('tag,ques,ans\n')

for sourceFileName in sys.argv[2:]:
    i = 0
    writeCount = 0
    defectedLines = []
    defectedLineCount = 0
    with open(sourceFileName, 'r', encoding='utf-8') as sourceFile:          
        while True:
            try:
                line = sourceFile.readline()
                if not line:
                    break

                if 'tag,ques,ans' in line: continue

                # all of these works    
                # if line == '\n': continue
                # if len(line) == 1: continue
                if len(line) < 5: continue

                targetFile.write(line)
                # print(writeCount, line, end='')
                writeCount+=1
            except:
                defectedLines.append(i)
                defectedLineCount+=1
            
            i+=1
        
        print('wrote',writeCount,'and could not write',defectedLineCount,'data from',sourceFileName,'to',targetFileName)
        sourceFile.close()

targetFile.close()