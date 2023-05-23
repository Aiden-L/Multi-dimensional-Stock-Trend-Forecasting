# Multi-dimensional Stock Trend Forecasting

> 该项目适用于多特征的 RNN, LSTM, GRU 神经网络的应用，以及基于词向量/随机森林的文本情感分析
> 
> 版权声明：该项目遵循 GPL3.0 开源协议，未经授权不得抄袭，转载

## 软件架构
* Python 3.7
* Tensorflow 2.1

## 安装说明
1. 安装依赖`pip install -r requirements.txt`
2. 深度学习框架请使用conda安装
    * `conda install cudatoolkit=10.1`
    * `conda install cudnn=7.6`
    * `pip install tensorflow==2.1`
    * `pip install numpy==1.18.5`
    * `conda install gensim`
   
   tensorflow 安装教程详见 <https://blog.csdn.net/weixin_46065314/article/details/109571907>

## 模型说明
该项目分为两个部分，价格相关数据的预测和文本情感相关的预测

### 价格相关数据预测
该部分在文件夹`price-prediction`中，运用 RNN, LSTM, GRU 探究多个特征对股票预测准确度的影响

#### 1. 制作数据集
数据爬取方面正在整理中，后续更新，敬请期待

数据格式可以参考`price-prediction/data`中的形式，因模型可以针对多特征构建，根据`price-prediction/model_builder.py`中注释提示即可根据需要，将所需多列作为多维特征训练和应用模型，因此，每列代表的意义也无需完全按照模板对应（开盘价，收盘价等）

#### 2. RNN, LSTM, GRU 模型构建及预测应用
模型训练，断点建立`price-prediction/model_builder.py`
应用模型进行预测`price-prediction/predictor.py`

### 文本情感预测

该部分在文件夹`text-prediction`中，运用词向量/随机森林预测评论情感倾向

#### 1. 制作数据集
1. 运行`makedataset/get300code.py`获得`makedataset/300code.json`存有沪深300股票代号数组
2. 运行`makedataset/getdata.py`获得300支股票的资讯文本信息，包括【内容，作者，时间】，300份csv文件存储在`makedataset/data`文件夹下
3. 运行`makedataset/getkStockPriceData.py`获得300支股票的价格和时间对应数据信息，索引为`priceobj["seq"]`包括字典所有索引的数组，
便于之后遍历获得前后日期关系，字典为`priceobj["pricedict"]`，可以方便通过时间取值（获取当天收盘价），300份csv文件存储在
`makedataset/savedpricedata`文件夹下
4. 运行`makedataset/makeDataset.py`制作情感分类数据集，生成`makedataset/dataset/neg.csv`和`makedataset/dataset/pos.csv`，
结合标签的组合型csv`makedataset/dataset/combined.csv`

#### 2. 词向量/随机森林预测
1. 运行`textClassification/trainVectorModelCreator.py`通过`combined.csv`训练词向量模型，存为
`textClassification/w2v_model_300_for_create_vector.pkl`
2. 运行`textClassification/generateVectors.py`读取`combined.csv`将其中的所有句子转化为词向量存为npy，放在
`textClassification/traindata`下（此文件夹不要在编译器打开，文件量超40W，打开编译器巨卡！）标签为文件名下划线后数字，
例如`99968_0.npy`，标签为0
3. 运行`textClassification/forestModelGenerator.py`使用traindata中数据训练随机森林模型，通过pickle存储为`forestmodel.pickle`
4. `textClassification/emoPredictFunc.py`中包含引用词向量/随机森林模型进行预测的函数（单句/多句），并包含单例测试demo，输入为字符串，输出预测结果，
`[0]`为消极，`[1]`为积极
5. 使用时仅需`emoPredictFunc.py`和两个训练好的模型`w2v_model_300_for_create_vector.pkl`，`forestmodel.pickle`，使用
`emoPredictFunc.py`中的predict函数
