import os
from copy import deepcopy
import numpy as np
import audioUtils
basePath = 'kws_data'

def getCategs():
    keywordFile = basePath + "/keywords.txt"
    keywords79 = {"unknown": 0}
    numKeyWordCategs = 79
    num = 1
    with open(keywordFile, 'r', encoding='utf-8') as f:  # 获取词表
        for line in f.readlines():
            line = line.strip("\n").strip()
            keywords79[line] = num
            num += 1
    return numKeyWordCategs, keywords79

def prepareKeyword(basePath):
    numKeyWordCategs, keywords79 = getCategs()
    print('Converting train set WAVs to numpy files')
    trainFolders = os.listdir(basePath+'/train')
    trainWAVs = []
    #traintxts = []
    for trainFolder in trainFolders:
        root = basePath + '/train/'+trainFolder
        if not os.path.isdir(root):
            continue
        # 如果.wav.npy文件存在，表明.wav文件转换成了.npy无需再次转换
        npyFile = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.wav.npy')]
        #traintxt = [os.path.join(root, f) for f in os.listdir(root) if "seg" in f]  # 通过seg.txt去对应utterance.wav，删除没有.wav文件的冗余seg.txt
        #traintxts.extend(traintxt)
        if npyFile:
            trainWAVs.extend(npyFile)
            continue
        # 如果.wav.npy文件不存在，则转换.wav文件
        audioUtils.WAV2Numpy(root)
        npyFile = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.wav.npy')]
        trainWAVs.extend(npyFile)
    
    #trainWAVtxt = [os.path.join(os.path.dirname(f), os.path.basename(f).split("seg")[0] + "utterance.wav.npy") for f in traintxts]
    #wav_txt(trainWAVtxt)
    #trainNpy = [len(np.load(x)) for x in trainWAVs]
    #print("最大长度：%s， 最小长度：%s，平均长度：%s" % (max(trainNpy),min(trainNpy), sum(trainNpy)/len(trainNpy)))
    trainWAVs = bad_audio_fn(deepcopy(trainWAVs))
    print('Converting test set WAVs to numpy files')
    testFolders = os.listdir(basePath + '/test')
    testWAVs = []
    #testtxts = []
    for testFolder in testFolders:
        if testFolder != "0800":  # 一个文件一个文件测试
            root = basePath + '/test/' + testFolder
            if not os.path.isdir(root):
                continue
            # 如果.wav.npy文件存在，表明.wav文件转换成了.npy无需再次转换
            npyFile = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.wav.npy')]
            #testtxt = [os.path.join(root, f) for f in os.listdir(root) if "seg" in f]  # 通过seg.txt去对应utterance.wav，删除没有.wav文件的冗余seg.txt
            #testtxts.extend(testtxt)
            if npyFile:
                testWAVs.extend(npyFile)
                continue
            # 如果.wav.npy文件不存在，则转换.wav文件
            audioUtils.WAV2Numpy(root)
            npyFile = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.wav.npy')]
            testWAVs.extend(npyFile)

    #testWAVtxt = [os.path.join(os.path.dirname(f), os.path.basename(f).split("seg")[0] + "utterance.wav.npy") for f in testtxts]
    #wav_txt(testWAVtxt)
    #testNpy = [len(np.load(x)) for x in testWAVs]
    #print("最大长度：%s， 最小长度：%s，平均长度：%s" % (max(testNpy),min(testNpy), sum(testNpy)/len(testNpy)))
    testWAVs = bad_audio_fn(deepcopy(testWAVs))

    print('Converting dev set WAVs to numpy files')
    devFolders = os.listdir(basePath + '/dev')
    devWAVs = []
    #devtxts = []
    for devFolder in devFolders:
        root = basePath + '/dev/' + devFolder
        if not os.path.isdir(root):
            continue
        # 如果.wav.npy文件存在，表明.wav文件转换成了.npy无需再次转换
        npyFile = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.wav.npy')]   
        #devtxt = [os.path.join(root, f) for f in os.listdir(root) if "seg" in f]  # 通过seg.txt去对应utterance.wav，删除没有.wav文件的冗余seg.txt
        #devtxts.extend(devtxt)
        if npyFile:
            devWAVs.extend(npyFile)
            continue
        # 如果.wav.npy文件不存在，则转换.wav文件
        audioUtils.WAV2Numpy(root)
        npyFile = [os.path.join(root, f) for f in os.listdir(root) if f.endswith('.wav.npy')]
        devWAVs.extend(npyFile)
    
    #devWAVtxt = [os.path.join(os.path.dirname(f), os.path.basename(f).split("seg")[0] + "utterance.wav.npy") for f in devtxts]
    #wav_txt(devWAVtxt)
    #devNpy = [len(np.load(x)) for x in devWAVs]
    #print("最大长度：%s， 最小长度：%s，平均长度：%s" % (max(devNpy),min(devNpy), sum(devNpy)/len(devNpy)))
    devWAVs = bad_audio_fn(deepcopy(devWAVs))
    # 准备训练数据的Label
    trainLabelFiles = [os.path.join(os.path.dirname(f), os.path.basename(f).split("utterance")[0] + "seg.txt") for f in
                       trainWAVs]
    trainLabels = encodeLabel(trainLabelFiles, keywords79)
    testLabelFiles = [os.path.join(os.path.dirname(f), os.path.basename(f).split("utterance")[0] + "seg.txt") for f in
                       testWAVs]
    testLabels = encodeLabel(testLabelFiles, keywords79)
    devLabelFiles = [os.path.join(os.path.dirname(f), os.path.basename(f).split("utterance")[0] + "seg.txt") for f in
                       devWAVs]
    devLabels = encodeLabel(devLabelFiles, keywords79)
    testWAVlabelsDict = dict(zip(testWAVs, testLabels))
    devWAVlabelsDict = dict(zip(devWAVs, devLabels))
    trainWAVlabelsDict = dict(zip(trainWAVs, trainLabels))

    #correspond(testWAVlabelsDict, keywords79, basePath + "/testList.txt")
    #correspond(devWAVlabelsDict, keywords79, basePath + "/devList.txt")
    #correspond(trainWAVlabelsDict, keywords79, basePath + "/trainList.txt") # 将train,dev,test数据集的文件路径及标签写到txt文件中
    correspond(trainWAVlabelsDict, keywords79, basePath + "/all_text.txt") # 将train,dev,test数据集的文件路径及标签写到txt文件中
    correspond(devWAVlabelsDict, keywords79, basePath + "/all_text.txt")
    correspond(testWAVlabelsDict, keywords79, basePath + "/all_text.txt")



    trainInfo = {'files': trainWAVs, 'labels': trainWAVlabelsDict}
    valInfo = {'files': devWAVs, 'labels': devWAVlabelsDict}
    testInfo = {'files': testWAVs, 'labels': testWAVlabelsDict}
    
    gscInfo = {'train': trainInfo, 'test': testInfo, 'val': valInfo}
    
    print("Done Keywords data set prepare.")
    return gscInfo, numKeyWordCategs+1, keywords79

def bad_audio_fn(WAVs, sample_rate=16000,min_duration=0.3, max_duration=6):
    fileNpy = [len(np.load(x)) for x in WAVs]

    durations = [lt/sample_rate for lt in fileNpy]
    #print("最大时长：%s， 最小时长：%s，平均时长：%s" % (max(durations),min(durations), sum(durations)/len(durations)))
    #for i, t in enumerate(durations):
    #    if t > max_duration or t < min_duration:  # 限制原生.wav文件的时长
    #        del WAVs[i]

    res = [WAVs[i] for i, t in enumerate(durations) if t >= min_duration and t <= max_duration]
    fileDel = [fileNpy[i] for i, t in enumerate(durations) if t >= min_duration and t <= max_duration]
    print("最大长度：%s， 最小长度：%s，平均长度：%s" % (max(fileDel),min(fileDel), sum(fileDel)/len(fileDel)))
    print("样本数量：%s" % len(res))
    return res

def correspond(WAVlabelsDict, keywords79, file):
    keywords79 = dict(zip(keywords79.values(), keywords79.keys()))
    with open(file, "a+") as f:
        for k, v in WAVlabelsDict.items():
            if v==0:
                continue
            #line = k[:-4] + "\t" + k[:-4].split("utterance")[0] + "seg.txt" + "\t" + keywords79[v] + "\n"
            line = k[:-8].split("/")[-1] + " " + keywords79[v] + "\n"
            f.write(line)
def wav_txt(wavs):
    for f in wavs:
        try:
            x = np.load(f)
        except FileNotFoundError:
            print("没有.wav文件：%s" % f)
            os.remove(f.split("utterance")[0] + "seg.txt")

def encodeLabel(trainLabelFiles, keywords79):
    trainLabels = []
    for f in trainLabelFiles:
        try:
            with open(f, "r", encoding="utf-8") as fObj:
                label = fObj.readline().strip("\n")
                if label == "":
                    label = "unknown"
                 #   print("UNK:%s"%f)
        except FileNotFoundError:
            label = "unknown"
            #if "BAC" not in f:
            #    print("UNK:%s"%f)
        try:
            trainLabels.append(keywords79[label])
        except KeyError:
            print(f, label)
            for key in keywords79.keys():
                if label in key:
                    label = key
                    trainLabels.append(keywords79[label])
                    break
    return trainLabels

#prepareKeyword(basePath)
