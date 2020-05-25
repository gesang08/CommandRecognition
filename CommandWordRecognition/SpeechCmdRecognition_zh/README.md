### 命令词识别（中文zh）
#### 主要环境
1、CUDA10.0.130  
2、cudnn7.6.0  
3、python3.6.7  
4、anaconda4.2.0  
5、tensorflow-gpu1.12.0  
6、keras2.2.4  

#### 命令词表
- 总共79个词+unknown，即80个，具体可见keywords.txt
 
#### 模型架构
- CNN + LSTM + Attention

#### 测试结果
- 在dev上的acc=95.69%
- 在test上的acc=95.63%
- 类别性能评估可见混淆矩阵picConfMatrix.png

