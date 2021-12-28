
class  config:

    #TOPSIS参数
    #Topsis需要用到的文件（某个月的所有外包员工的产出表）
    TOPSIS_Dir = './customers_nums.csv'
    #需要识别的优秀异常占比
    Excellent_Anomaly_Rate = 0.1
    #需要识别的较差异常占比
    Inferior_Anomaly_Rate = 0.1


    #iForest参数
    #iForest需要用到的数据 1）外包员工名单  2）
    iForest_Dir = None
    #判定为异常点的域值，小于该值则认为该时间点为异常 （-0.5 ~ 0.5间设定）
    Treshold_Time = -0.1
    #需要识别的异常员工占比
    State_Anomaly_Rate = 0.1
    #异常点计数阈值，若某员工异常点数超过该阈值，则被判断为异常员工
    Treshold_Count = 5




