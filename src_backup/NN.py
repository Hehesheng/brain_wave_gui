import numpy as np
from keras.layers import Dense
from keras.models import Sequential
import keras
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import StandardScaler


class NN(object):
    def __init__(self, trainx, trainy, testx, testy, normalizedata=True, weights_save_dir='./NN/emotion.h5'):

        self.trainx = trainx
        self.trainy = trainy
        self.testx = testx
        self.testy = testy
        self.Modelcheckpoint = ModelCheckpoint(
            weights_save_dir, save_best_only=True, monitor='val_acc', verbose=1)
        self.Earlystop = EarlyStopping(
            monitor='val_acc', patience=100)  # 如果100次验证集准确度没有提升, 终止训练
        self.scaler = StandardScaler()  # 高斯归一化
        if normalizedata:
            self.scaler1 = self.scaler.fit(trainx)
            self.trainx = self.scaler1.transform(self.trainx)
            self.testx = self.scaler1.transform(self.testx)

    # 不需要调用
    def initial_network(self):
        '''
            模型结构
        '''
        self.model = Sequential()
        self.model.add(Dense(64, activation='relu',
                             input_dim=self.trainx.shape[1], name='Dense1'))
        self.model.add(Dense(64, activation='relu', name='Dense2'))
        self.model.add(Dense(64, activation='relu', name='Dense3'))
        self.model.add(Dense(4, activation='softmax', name='Classification'))
        self.model.compile(loss=keras.losses.sparse_categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

    # 不需要调用
    def initial_train(self, epoch=50, batch_size=32):
        self.initial_network()
        self.model.fit(self.trainx, self.trainy, epochs=epoch, batch_size=batch_size,
                       validation_data=(self.testx, self.testy), callbacks=[
                           self.Modelcheckpoint, self.Earlystop],
                       shuffle=True)

    # 实时训练用
    def finetune(self, new_trainx, new_trainy, freeze_layer=2, finetune_epoch=5, weights_save_dir='./NN/emotion.h5', batch_size=32):
        '''
            new_trainx和new_trainy是新数据, freeze_layer锁定前n层的训练参数, finetune_epoch微调回合, weights_save_dir读取原始模型参数
        '''
        layer_name = []
        new_trainx = self.scaler1.transform(new_trainx)
        self.initial_network()
        self.model.load_weights(weights_save_dir)
        for l in self.model.layers[:freeze_layer]:
            l.trainable = False
            layer_name.append(l.name)
        print('Freezeing training Layer:', layer_name)
        self.model.fit(new_trainx, new_trainy, epochs=finetune_epoch, batch_size=batch_size,
                       validation_data=(self.testx, self.testy), callbacks=[
                           self.Modelcheckpoint, self.Earlystop],
                       shuffle=True)

    # 预测用
    def predict(self, testx, weights_save_dir='./NN/emotion.h5'):
        '''
        读取weights_save_dir的参数, 并且对testx按照原输入trainx统计信息进行归一化, 得到预测结果
        '''
        self.initial_network()
        self.model.load_weights(weights_save_dir)
        testx = self.scaler1.transform(testx)
        if len(testx.shape) > 1:
            return self.model.predict_classes(testx)
        else:
            return self.model.predict_classes(np.expand_dims(testx, 0))[0]


if __name__ == "__main__":
    # 必须导入，原始数据
    trainx = np.load('./NN/TGAM/TGAM_testx.npy')
    trainy = np.load('./NN/TGAM/TGAM_trainy.npy') - 1  # 标签从零开始
    testx = np.load('./NN/TGAM/TGAM_testx.npy')
    testy = np.load('./NN/TGAM/TGAM_testy.npy') - 1
    # 新数据输入
    newtestx = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # newtestx.expand_dims()
    newtestx = newtestx.reshape((1, 10))
    newtesty = np.array([1])
    newtesty = newtesty.reshape((1, 1))

    # 初始模型训练
    model = NN(trainx, trainy, testx, testy)  # 导入原始数据
    # print(model.finetune(newtestx, newtesty))  # 实时学习
    # model.finetune(newtestx, newtesty)
    # print(model.predict(newtestx))  # 预测结果
    model.predict(newtestx)

    # print(confusion_matrix(newtesty, model.predict(newtestx)))  # 混淆矩阵
