import json

import jieba
import numpy as np
from gensim.models.word2vec import Word2Vec
import pandas as pd

CSV_PATH = '../makedataset/dataset/combined.csv'  # 存有正面/负面的数据信息

# 数据集获取
dataset = pd.read_csv(CSV_PATH, names=['contents', 'value']).astype(str)
# 分词
cw = lambda x: list(jieba.cut(x))
dataset["words"] = dataset['contents'].apply(cw)
dataset['vector'] = dataset['words']

total_length = len(dataset['vector'])

counting = 0
for line in dataset['vector']:
    # 词向量模型加载
    w2v_model = Word2Vec.load('w2v_model_300_for_create_vector.pkl')
    size = 300
    sen_vec = np.zeros(size).reshape((1, size))

    count = 0
    for word in line:
        try:
            sen_vec += w2v_model.wv[word].reshape((1, size))
            count += 1
        except KeyError:
            continue
    if count != 0:
        sen_vec /= count
        dataset['vector'][counting] = sen_vec
    # 将结果存入文件train和label
    np.save("traindata/"+str(counting)+"_"+str(dataset['value'][counting])+".npy", dataset['vector'][counting])
    # with open("traindata/trainx.txt", 'a') as f:
    #     f.write(json.dumps(dataset['vector'][counting]) + "\n")
    # with open("traindata/trainy.txt", 'a') as f:
    #     f.write(str(dataset['value'][counting]) + "\n")
    # print(counting, "/", total_length, dataset['value'][counting], dataset['vector'][counting])
    print(counting, "/", total_length)
    counting += 1
