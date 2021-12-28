import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
from config import config
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)

#set variable
rs = np.random.RandomState(169);


#读取数据并分割
def read_data(dir):
    dataset = pd.read_csv(dir, engine='python')
    date = dataset.iloc[:,np.r_[0]]
    outcomes = dataset.iloc[:,np.r_[1:dataset.shape[1]]]
    return date, outcomes


#训练并返回样本及其异常值
#n_estimators  iTree数量
#max_sample  每棵树的样本数
#max_features 最大特征数,若为int即特征数，若为float即特征占比
#contamination 异常值占比

def train(outcomes, date):
    ifm = IsolationForest(n_estimators=100, verbose=2, n_jobs=2, #contamination=0.1,
                          max_samples=outcomes.shape[0], random_state=rs, max_features=1.0)
    ifm.fit(outcomes)
    scores_pred = ifm.decision_function(outcomes) #该函数得出的异常分数在 -0.5~0.5 之间，越靠近-0.5越可能是异常点
    # scores_pred = -ifm.score_samples(outcomes)
    result = np.column_stack((pd.DataFrame(date), pd.DataFrame(scores_pred)))
    result = pd.DataFrame(result)
    result.columns = ['date', 'score']
    return result


#获取异常点计数
#当该时间点异常分数小于阈值时，被判定为异常点，进行计数

def get_anomaly_count(dir):
    date, outcomes = read_data(dir)
    scoreset = train(outcomes, date)
    scoreset = scoreset.sort_values(by='score',ascending=True)
    scoreset = scoreset[scoreset['score'] < config.Treshold_Time]
    count =  scoreset.shape[0]
    return count

if __name__ == '__main__':
    count = get_anomaly_count(config.TOPSIS_Dir)
    print(count)


    # 绘图
    # threshold = stats.scoreatpercentile(scores_pred, 100 * 0.1)
    # # 使用预测值取5%分位数来定义阈值（基于小概率事件5%）
    # # 根据训练样本中异常样本比例，得到阈值，用于绘图
    #
    # # matplotlib
    # # plot the line, the samples, and the nearest vectors to the plane
    # xx, yy = np.meshgrid(np.linspace(nmlz_a, nmlz_b, 50), np.linspace(nmlz_a, nmlz_b, 50))  # 画格子
    # Z = ifm.decision_function(np.c_[xx.ravel(), yy.ravel()])
    # Z = Z.reshape(xx.shape)
    # plt.title("IsolationForest ")# plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)
    # otl_proportion = int(0.1 * len(dataset['Date']))
    # plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, otl_proportion), cmap=plt.cm.hot)# 绘制异常点区域，值从最小的到阈值的那部分
    # a = plt.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors='red')# 绘制异常点区域和正常点区域的边界
    # plt.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors='palevioletred')
    # # palevioletred 紫罗兰
    # # 绘制正常点区域，值从阈值到最大的那部分
    #
    # for i in scores_pred:
    #     if i <= threshold:
    #         #print(i)
    #         test_data.append(1)
    #         anomaly.append(i)
    #     else:
    #         test_data.append(0)
    #
    # ano_lable = np.column_stack(((dataset['Date'],dataset['data'],x,y,scores_pred, test_data)))
    # df = pd.DataFrame(data=ano_lable, columns=['Date','data','x', 'y', 'IsoFst_Score','label'])
    #
    # b = plt.scatter(df['x'][df['label'] == 0], df['y'][df['label'] == 0], s=20, edgecolor='k',c='white')
    # c = plt.scatter(df['x'][df['label'] == 1], df['y'][df['label'] == 1], s=20, edgecolor='k',c='black')
    # plotlist = df.to_csv('Iso_list.csv')
    #
    # plt.axis('tight')
    # plt.xlim((nmlz_a, nmlz_b))
    # plt.ylim((nmlz_a, nmlz_b))
    # plt.legend([a.collections[0], b, c],
    #            ['learned decision function', 'true inliers', 'true outliers'],
    #            loc="upper left")
    # print("孤立森林阈值  ：",threshold)
    # print("全量数据样本数：",len(dataset),"个")
    # print("检测异常样本数：",len(anomaly),"个")
    # plt.show()
