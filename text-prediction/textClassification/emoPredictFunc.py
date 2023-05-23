import pickle

import jieba
import numpy as np
from gensim.models import Word2Vec

def predict(sentence):
    # 分词
    words = jieba.cut(sentence)
    # 加载词向量模型
    w2v_model = Word2Vec.load('w2v_model_300_for_create_vector.pkl')
    size = 300
    sen_vec = np.zeros(size).reshape((1, size))
    # 制作句向量
    count = 0
    for word in words:
        try:
            sen_vec += w2v_model.wv[word].reshape((1, size))
            count += 1
        except KeyError:
            continue
    if count != 0:
        sen_vec /= count
    # 加载forest模型
    with open('forestmodel.pickle', 'rb') as f:
        saved_forest = pickle.load(f)
    predict_result = saved_forest.predict(sen_vec)

    return predict_result

if __name__ == '__main__':
    # 测试
    print(predict("平安银行：融资净买入4474.76万元，融资余额42.93亿元"))
