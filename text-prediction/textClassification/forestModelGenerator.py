import os
import pickle

import numpy as np
from sklearn.ensemble import RandomForestClassifier

NPY_FILE_DIR = "traindata"

trainx = []
trainy = []

count = 0
total = len(os.listdir(NPY_FILE_DIR))
for file in os.listdir(NPY_FILE_DIR):
    # 从文件名加载标签
    label = int(file.split("_")[1].split(".")[0])
    # 从文件加载词向量(取一维)
    vector = np.load(os.path.join(NPY_FILE_DIR, file))[0]
    trainx.append(vector)
    trainy.append(label)
    # 进度条
    count += 1
    print(count, "/", total)

# print(trainx, trainy)

forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit(trainx, trainy)

# 保存模型
with open('forestmodel.pickle', 'wb') as f:
    pickle.dump(forest, f)

# 加载模型
with open('forestmodel.pickle', 'rb') as f:
    saved_forest = pickle.load(f)

# 以下为测试：
testvec = np.load(os.path.join(NPY_FILE_DIR, "108801_0.npy"))
predict_result = saved_forest.predict(testvec)
print(predict_result)

