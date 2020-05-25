# coding=utf-8
import os

# 将文件名修改成规范格式，例如将001_6_utterance.wav修改成001_006_utterance.wav
basePath = 'kws_data'
#basePath = basePath + '/train/'
#basePath = basePath + '/dev/'
basePath = basePath + '/test/'
allFiles = []
for root, dirs, files in os.walk(basePath):
    allFiles += [os.path.join(root, f) for f in files if "utterance" in f or "seg" in f]
for i, v in enumerate(allFiles):
    s = v.split("_")
    if len(s[2]) == 1:
        s[2] = "00" + s[2]
    elif len(s[2]) == 2:
        s[2] = "0" + s[2]
    else:
        continue
    new_s = "_".join(s)
    os.rename(v, new_s)
    allFiles[i] = new_s
