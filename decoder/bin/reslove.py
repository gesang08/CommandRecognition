#coding=utf-8
"""
从lll.log文本中获取如下格式信息：
wav decode_info
lll/000000.wav 	 so in college i was a government major which means i had to write a lot of
lll/000032.wav 	 now here's my brain
lll/000113.wav 	 let's start with an example of that
"""
import os
import json
import sys

def resolved(filePath):
    resDict={}
    with open(filePath, 'r') as fileObj:
        content = [v.strip('\n').strip() for v in fileObj.readlines()]
        for idx, line in enumerate(content):
            if line.endswith('.wav'):
                retList = []
                wavPath = line.split()[-1]
                resDict[wavPath]=''
            elif 'alignment_info' in line:
                lineDict = json.loads(line)  # 自动将false转成bool:False,true转成bool:True
                if lineDict['final'] is True and len(lineDict['ret']) != 0:
                    retList.append(lineDict['ret'])
                    resDict[wavPath] = resDict[wavPath] + ' ' + lineDict['ret']
                elif lineDict['final'] is True and len(lineDict['ret']) == 0:
                    try:
                        lineDict = json.loads(content[idx-1])  # 取上一行final=false,rect!=''的rect
                        if lineDict['final'] is False and len(lineDict['ret']) != 0:
                            retList.append(lineDict['ret'])
                            ret = ' '.join(retList)
                            resDict[wavPath] = ret
                    except:
                        pass
            else:
                pass
    return resDict

file = sys.argv[1]
res = resolved(file)
for k,v in res.items():
    print(k,'\t',v.strip())
