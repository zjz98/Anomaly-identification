import pandas as pd
import numpy as np
from config import config



#读取数据，并将id和产出数据分离
def read_data(dir):
    dataset = pd.read_csv(dir, engine='python')
    id = dataset.iloc[:,np.r_[0]]
    outcomes = dataset.iloc[:,np.r_[1:dataset.shape[1]]]
    return id, outcomes

# 逆指标正向化，需参考华为数据实现，如bug数量这样的指标越小越好，需要进行正向化。
def reverse(data):
	pass

# topsis
def topsis(id, data, weight=None):
	# 归一化
	data = data / np.sqrt((data ** 2).sum())

	# 指标正向化
	# data = reverse(data)

	# 最优最劣方案
	Z = pd.DataFrame([data.min(), data.max()], index=['负理想解', '正理想解'])

	# 距离
	weight = entropyWeight(data) if weight is None else np.array(weight)
	Result = data.copy()
	Result['正理想解'] = np.sqrt(((data - Z.loc['正理想解']) ** 2 * weight).sum(axis=1))
	Result['负理想解'] = np.sqrt(((data - Z.loc['负理想解']) ** 2 * weight).sum(axis=1))

	# 综合得分指数
	Result['综合得分指数'] = Result['负理想解'] / (Result['负理想解'] + Result['正理想解'])
	Result = Result[['综合得分指数']]
	Result = np.column_stack((pd.DataFrame(id), pd.DataFrame(Result)))
	Result = pd.DataFrame(Result)
	Result.columns = ['id', 'score']
	Result = Result.sort_values(by='score', ascending=False)

	return Result


# 熵权法
def entropyWeight(data):
	data = np.array(data)
	# 归一化
	P = data / data.sum(axis=0)

	# 计算熵值
	E = np.nansum(-P * np.log(P) / np.log(len(data)), axis=0)

	# 计算权系数
	return (1 - E) / (1 - E).sum()


#主执行函数
def get_rank(dir):
	id, dataset = read_data(dir)
	result = topsis(id,dataset)
	print(result)


if __name__ == '__main__':
	get_rank(config.TOPSIS_Dir)