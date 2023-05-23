import tensorflow as tf
from tensorflow.keras.layers import Dropout, Dense, SimpleRNN, LSTM, GRU
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os

from data_acquisition.get_ch_name import get_ch_name


def predictor(stock_name, today_time):
    # 创建当天的预测文件夹
    save_path = "./predict_data/" + today_time + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    rate_save_path = "./predict_rate/" + today_time + "/"
    if not os.path.exists(rate_save_path):
        os.makedirs(rate_save_path)

    stock_file = pd.read_csv('./data/' + stock_name + '.csv')  # 读取股票文件
    # 选择模型类型
    model_type = "LSTM"  # options: RNN, LSTM, GRU; default: RNN

    # stock_file.shape[0]返回数据行数，shape[1]返回列数
    training_set = stock_file.iloc[0:stock_file.shape[0] - 60, [2, 5]].values

    test_set = stock_file.iloc[stock_file.shape[0] - 60:, [2, 5]].values

    # 归一化
    sc = MinMaxScaler(feature_range=(0, 1))  # 定义归一化：归一化到(0，1)之间
    training_set_scaled = sc.fit_transform(training_set)  # 求得训练集的最大值，最小值这些训练集固有的属性，并在训练集上进行归一化
    test_set_one = sc.transform(test_set)  # 利用训练集的属性对测试集进行归一化

    # 构建模型参数
    if model_type == "LSTM":
        # LSTM 模型
        model = tf.keras.Sequential([
            LSTM(80, return_sequences=True),
            Dropout(0.2),
            LSTM(100),
            Dropout(0.2),
            Dense(1)
        ])
    elif model_type == "GRU":
        # GRU 模型
        model = tf.keras.Sequential([
            GRU(80, return_sequences=True),
            Dropout(0.2),
            GRU(100),
            Dropout(0.2),
            Dense(1)
        ])
    else:
        # RNN 模型
        model = tf.keras.Sequential([
            SimpleRNN(80, return_sequences=True),
            Dropout(0.2),
            SimpleRNN(100),
            Dropout(0.2),
            Dense(1)
        ])

    # 根据选取的模型种类，调用各自保存的模型参数信息
    if model_type == "LSTM":
        checkpoint_save_path = "./checkpoint/LSTM_stock" + stock_name + ".ckpt"
    elif model_type == "GRU":
        checkpoint_save_path = "./checkpoint/stock" + stock_name + ".ckpt"
    else:
        checkpoint_save_path = "./checkpoint/rnn_stock" + stock_name + ".ckpt"

    model.load_weights(checkpoint_save_path)

    ################## predict ######################
    # 增加一个维度（之前以组的形式送入，这次就是1组）
    test_set_a = test_set_one[tf.newaxis, ...]
    # 输入60天数据进行预测
    predicted_stock_price = model.predict(test_set_a)
    # 反归一化
    predicted_stock_price = np.column_stack((predicted_stock_price, np.zeros(predicted_stock_price.shape[0])))
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)[:, 0][0]
    # 将预测的数据加入样本再进行预测

    print(test_set)
    print("predict:")
    print(predicted_stock_price)
    # 将日期信息写入文件
    f = open(save_path + stock_name + "predict.txt", 'w')
    f.write('[')
    for item in stock_file.iloc[stock_file.shape[0] - 60:, 0:1].values:
        f.write('\'' + item[0] + '\',')
    f.write('\'predict\']\n')
    # 将数据写入文件
    f.write('[')
    for item in test_set:
        f.write('%.2f,' % item[0])
    f.write(str(predicted_stock_price) + ']')
    f.close()
    with open(rate_save_path + stock_name + "rate.txt", 'w') as g:
        # 直接写入中文名
        st_ch = stock_name + get_ch_name(stock_name)
        g.write(st_ch + ',' + str((predicted_stock_price - test_set[59][0]) / test_set[59][0]))
    return 0


if __name__ == '__main__':
    predictor('000001', 'test')
