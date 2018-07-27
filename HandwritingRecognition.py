import numpy as np
from os import listdir
import operator
from numpy.ma import zeros

# 图像矩阵转换为二进制向量
# 本例中读取文本文件的前32行和前32列，即32x32的矩阵，转换为1x1024的向量

def img2vector(filemane):
    returnVect = zeros((1,1024))
    fr = open(filemane)
    for i in range(32):
        linStr = fr.readline() #得到文本的行数
        for j in range(32):
            returnVect[0,32*i+j] = int(linStr[j])
    return returnVect


# knn算法:
# in_X 用于分类的输入向量
# data 训练样本集
# labels 标签向量
# k 选择最近邻的数量
def knnClassify(in_X, data, labels, k):
    data_size = data.shape[0]
    diff_mat = np.tile(in_X, (data_size, 1)) - data
    sq_diff = diff_mat ** 2
    sq_distance = sq_diff.sum(axis=1)
    distance = sq_distance ** 0.5
    sorted_dist = distance.argsort()
    class_count = {}
    for i in range(k):
        vote_label = labels[sorted_dist[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


# 手写数字识别
def handwritingTest():
    hw_labels = []
    training_list = listdir("trainingDigits") #返回文件夹中的文件名称
    num_files = len(training_list)
    training =  zeros((num_files, 1024))
    for i in range(num_files):
        # 文件名 0_1.txt，从文件名中解析分类数字，此例为0
        file = training_list[i]
        file_string = file.split(".")[0]
        number = int(file_string.split("_")[0])
        hw_labels.append(number)
        training[i, :] = img2vector("trainingDigits/%s" % file)
    testing_list = listdir('testDigits')
    error_count = 0.0
    num_test = len(testing_list)
    for i in range(num_test):
        t_file = testing_list[i]
        t_file_string = t_file.split('.')[0]
        t_number = int(t_file_string.strip('_')[0])
        t_vector = img2vector('testDigits/%s' % t_file)
        result = knnClassify(t_vector, training, hw_labels, 20)
        if result != t_number:
            error_count += 1
            print("分类结果： %d , 实际值： %d" % (result, t_number))
    print("\n 识别错误的数目：%d" % error_count)
    print("\n 错误率： %f" % (error_count / float(t_number)))


if __name__ == '__main__':
    handwritingTest()