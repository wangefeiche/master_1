from sklearn.linear_model import ElasticNet
import csv
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib
#处理csv文件-------------------------------------------
#df = pd.read_csv('example.csv')
#df = df[(True^df['dlrxmcs'].isin([0]))]
#df = df[(True^df['ulrxmcs'].isin([0]))]
#df_data = df.iloc[:,1:12]
#df_time = df.iloc[:,0]
#df_label = df.iloc[:,12]
#df_norm = (df.iloc[:,1:12] - df.iloc[:,1:12].min()) / (df.iloc[:,1:12].max() - df.iloc[:,1:12].min())
#result = pd.concat([df_time, df_norm,df_label], axis=1)
#result.to_csv('example_norm.csv',index=None)
np.random.seed(0)

df_1 = pd.read_csv('MPC_train_1.csv')
df_2 = pd.read_csv('MPC_train_2.csv')
df_3 = pd.read_csv('MPC_train_3.csv')
df_4 = pd.read_csv('MPC_train_4.csv')

Folder_Path = 'MPC_train_'
file_list = [1,2,3,4]

df = pd.read_csv(Folder_Path + str(file_list[0]) + '.csv')   #编码默认UTF-8，若乱码自行更改
 
#将读取的第一个CSV文件写入合并后的文件保存
df.to_csv('MPC_train.csv',encoding="utf_8_sig",index=False)
 
#循环遍历列表中各个CSV文件名，并追加到合并后的文件
for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + str(file_list[0]) + '.csv')
    df.to_csv('MPC_train.csv',encoding="utf_8_sig",index=False, header=False, mode='a+')


df = pd.read_csv('MPC_train.csv').sample(frac=1)

n_samples_train = 80000

X = df.iloc[:,0:8].values.tolist()
y = df.iloc[:,8].values.tolist()
 
# Split train and test data
X_train, X_test = X[:n_samples_train], X[n_samples_train:]
y_train, y_test = y[:n_samples_train], y[n_samples_train:]
 
###############################################################################
# Compute train and test errors
alphas = np.logspace(-5, 1, 60)
enet = ElasticNet(l1_ratio=1)
train_errors = list()
test_errors = list()
for alpha in alphas:
    enet.set_params(alpha=alpha)
    enet.fit(X_train, y_train)
    train_errors.append(enet.score(X_train, y_train))
    test_errors.append(enet.score(X_test, y_test))
 
i_alpha_optim = np.argmax(test_errors)
alpha_optim = alphas[i_alpha_optim]
print("Optimal regularization parameter : %s" % alpha_optim)
 
# Estimate the coef_ on full data with optimal regularization parameter
enet.set_params(alpha=alpha_optim)

joblib.dump(enet,"train_model.m")
###############################################################################
# Plot results functions
 

plt.subplot(1, 1, 1)
plt.semilogx(alphas, train_errors, label='Train')
plt.semilogx(alphas, test_errors, label='Test')
plt.vlines(alpha_optim, plt.ylim()[0], np.max(test_errors), color='k',
           linewidth=3, label='Optimum on test')
plt.legend(loc='lower left')
plt.ylim([0, 1.2])
plt.xlabel('Regularization parameter')
plt.ylabel('Performance')
plt.show()


