#coding=utf-8
"""
从decodeRes.log文本中获取如下格式信息：
wav_path decode_info
data/000000.wav 	 so in college i was a government major which means i had to write a lot of
data/000032.wav 	 now here's my brain
data/000113.wav 	 let's start with an example of that
"""
import os
import json
import sys

if len(sys.argv[1:]) != 3:
    print('Usage: python3 %s <file_path> <wav_dir> <label_file>' % sys.argv[0])
    print('eg: python3 reslove.py decodeRes.log data/onepos text79')
    sys.exit()
filePath = sys.argv[1]  # decodeRes.log文件路径
wavdir = sys.argv[2]  # wavdir对应的目录
text = sys.argv[3]  # label文件


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


def wav2Label(res):
    wav2ref = 'ref_%s.txt' % text
    wav2hyp = 'hyp_%s.txt' % text
    if os.path.exists(wav2ref):
        os.system('rm -rf %s' % wav2ref)
        os.system('rm -rf %s' % wav2hyp)
    hypDict = {}
    for k, v in res.items():
        wavId = os.path.basename(k)[:-4]
        hypDict[wavId] = v.strip()
        hyp = wavId + " " + v.strip()
        os.system("grep %s %s >>%s" % (wavId, text, wav2ref))  # 抽取wav对应的label存放wav2ref中
        os.system("echo %s >>%s" % (hyp, wav2hyp))
    refList = []
    with open(wav2ref, 'r') as refFile:
        refContent = refFile.readlines()
        for refline in refContent:
            refline = refline.strip('\n')
            ref = refline.split(" ")
            wav = os.path.join(wavdir, ref[0] + '.wav')
            refLabel = str(ref[1])
            refList.append(ref[0] + " " + refLabel)
    return refList, hypDict


if __name__ == '__main__':
    res = resolved(filePath)  # 解析出结果
    refList, hypDict = wav2Label(res)   # 获取wav对应的label
    for value in refList:
        wav = value.split(' ')[0]
        label = value.split(' ')[1]
        out = wav + "\thyp:\t" + hypDict[wav] + "\tref:\t" + label + "\tresult:\t" + str(hypDict[wav].strip() == label)
        print(out)
