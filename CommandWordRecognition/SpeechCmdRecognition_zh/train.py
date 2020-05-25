# coding=utf-8
import tensorflow as tf
import numpy as np
import math
import os
from keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from keras.models import load_model, Sequential
from kapre.time_frequency import Melspectrogram
from kapre.utils import Normalization2D
from sklearn.metrics import confusion_matrix  # 获取多分类的混淆矩阵
import audioUtils
#解决问题：Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2'
# 在使用多进程时，同一时刻可能会对同一对象（文件）进行操作，但是由于有锁机制，同一时刻就不能对同一对象进行操作，使程序报错，将文件锁机制取消就可以了
os.environ["HDF5_USE_FILE_LOCKING"] = 'FALSE'

os.environ["CUDA_VISIBLE_DEVICES"] = "3, 4"


import SpeechGenerator
import SpeechModels
import kws
sr = 16000  # we know this one for google audios
iLen = 40000
saveModel="./modelFile/model-attRNN40000gai.hdf5"

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.
    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph

def step_decay(epoch):
    initial_lrate = 0.001
    drop = 0.4
    epochs_drop = 10.0
    lrate = initial_lrate * math.pow(drop,
                                     math.floor((1 + epoch) / epochs_drop))

    if (lrate < 4e-5):
        lrate = 4e-5

    print('Changing learning rate to {}'.format(lrate))
    return lrate

# 获取train,validation,test,testREAL各部分数据集
gscInfo, nCategs,keywords79 = kws.prepareKeyword("kws_data")

trainGen = SpeechGenerator.SpeechGen(gscInfo['train']['files'], gscInfo['train']['labels'],dim=iLen, shuffle=True)
# handle the fact that number of samples in validation may not be multiple of batch_size with shuffle=True
valGen = SpeechGenerator.SpeechGen(gscInfo['val']['files'], gscInfo['val']['labels'], dim=iLen, shuffle=True)
# use batch_size = total number of files to read all test files at once
testGen = SpeechGenerator.SpeechGen(gscInfo['test']['files'], gscInfo['test']['labels'],dim=iLen, shuffle=False, batch_size=len(gscInfo['test']['files']))
#testGen = SpeechGenerator.SpeechGen(gscInfo['test']['files'], gscInfo['test']['labels'],dim=iLen, shuffle=False)
#testRGen = SpeechGenerator.SpeechGen(gscInfo['testREAL']['files'], gscInfo['testREAL']['labels'], shuffle=False, batch_size=len(gscInfo['testREAL']['files']))


#model = SpeechModels.AttRNNSpeechModel(nCategs, samplingrate=16000, inputLength=None)
#model.compile(optimizer='adam', loss=['sparse_categorical_crossentropy'], metrics=['sparse_categorical_accuracy'])
#print('模型结构：')
#model.summary()

#lrate = LearningRateScheduler(step_decay)
#earlystopper = EarlyStopping(monitor='val_sparse_categorical_accuracy', patience=10, verbose=1)
#checkpointer = ModelCheckpoint('model-attRNN.h5', monitor='val_sparse_categorical_accuracy', verbose=1, save_best_only=True)
#results = model.fit_generator(trainGen, validation_data=valGen, epochs=40, use_multiprocessing=True, workers=4, verbose=1,
#                    callbacks=[earlystopper, checkpointer, lrate])

if not os.path.exists(saveModel):
    model = SpeechModels.AttRNNSpeechModel(nCategs, samplingrate=16000, inputLength=iLen)
    model.compile(optimizer='adam', loss=['sparse_categorical_crossentropy'], metrics=['sparse_categorical_accuracy'])
    print('模型结构：')
    model.summary()
    lrate = LearningRateScheduler(step_decay)
    earlystopper = EarlyStopping(monitor='val_sparse_categorical_accuracy', patience=10, verbose=1)
    checkpointer = ModelCheckpoint(saveModel, monitor='val_sparse_categorical_accuracy', verbose=1, save_best_only=True)
    results = model.fit_generator(trainGen, validation_data=valGen, epochs=40, use_multiprocessing=True, workers=4, verbose=1,
                        callbacks=[earlystopper, checkpointer, lrate])

melspecModel = Sequential()
melspecModel.add(Melspectrogram(n_dft=1024, n_hop=128, input_shape=(1, iLen),
                         padding='same', sr=sr, n_mels=160,
                         fmin=40.0, fmax=sr/2, power_melgram=1.0,
                         return_decibel_melgram=True, trainable_fb=False,
                         trainable_kernel=False,
                         name='mel_stft'))

melspecModel.add(Normalization2D(int_axis=0))
melspecModel.summary()

model = load_model(saveModel, custom_objects={'Melspectrogram': Melspectrogram, 'Normalization2D': Normalization2D })
#model.summary()

#print("训练集准确率：")
#trainEval = model.evaluate_generator(trainGen, use_multiprocessing=True, workers=3, verbose=1)
#print(trainEval)
print("验证集准确率：")
valEval = model.evaluate_generator(valGen, use_multiprocessing=True, workers=3, verbose=1)
print(valEval)						
print("测试集准确率：")
#testEval = model.evaluate_generator(testGen, use_multiprocessing=True, workers=3,verbose=1)
#print(testEval)
x_test, y_test = testGen.__getitem__(0)
y_pred = model.predict(x_test, verbose=1)
print(y_pred.shape, y_test.shape)

keywords79 = dict(zip(keywords79.values(), keywords79.keys()))
y_pred_label = np.argmax(y_pred, axis=1)
corr_num = 0
for i in range(len(y_test)):
    if y_pred_label[i] == y_test[i]:
        #print("预测正确，预测为：%s，标签为：%s"%(keywords79[y_pred_label[i]], keywords79[y_test[i]]))
        corr_num += 1
    else:
        print(testGen.list_IDs[i],len(np.load(testGen.list_IDs[i]))/16000)
        print("预测错误，预测为：%s，标签为：%s"%(keywords79[y_pred_label[i]], keywords79[y_test[i]]))
print("测试集准确率：%s/%s=%s" % (corr_num, len(gscInfo['test']['files']), corr_num/len(gscInfo['test']['files'])))



def get_confusion_matrix(y_test, y_pred, keywords):
    cm = confusion_matrix(y_test, np.argmax(y_pred,1))
    keywordList = list(keywords.keys())
    audioUtils.plot_confusion_matrix(cm, keywordList, normalize=True)


get_confusion_matrix(y_test, y_pred, keywords79)
