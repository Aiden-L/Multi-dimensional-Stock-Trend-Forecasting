from gensim.models.word2vec import Word2Vec
import pandas as pd
import jieba

CSV_PATH = '../makedataset/dataset/combined.csv'
# 读取数据
train_data = pd.read_csv(CSV_PATH, names=['contents', 'value']).astype(str)

cw = lambda x: list(jieba.cut(x))
train_data['words'] = train_data['contents'].apply(cw)

# W2V训练模型
w2v_model = Word2Vec(train_data['words'], sg=1, vector_size=300, min_count=10, hs=0)
w2v_model.save('w2v_model_300_for_create_vector.pkl')

print("Model saved at: w2v_model_300_for_create_vector.pkl")
