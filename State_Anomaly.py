# State_Anomaly.py
# 输入：外包员工名单
# 步骤：
#     list = null
#     for e in employee_set：
#         get dataset of e （获取员工e月度的产出序列数据）
#         count = Isolation_forest.get_anomaly_count (调用Isolation_forest文件构建孤立森林，并得到异常点计数)
#         if count > treshold:
#             list.add(e)
# 输出：个人状态异常的外包员工名单
# 备注：对识别出的个人状态异常的员工，后续需要回调Isolation_forest.py进行画图展示等

# 根据数据存储情况实现
