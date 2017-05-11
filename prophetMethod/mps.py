# -*- coding: utf-8 -*-
# -*- coding: cp936 -*-
import csv
import numpy as np
import os
import json





# 单天预测函数
def forecast_one(forecast_date, filename):
    # type: (object, object) -> object
    # 读取CSV文件并将字符串转化为浮点数存入数组
    # the para filename is the path to the file from the root
    # filename = os.path.join('.', 'ExampleData.csv')

    data = csv.reader(file(filename, 'rb'))
    demand = []
    date = []
    hour = []

    for line in data:
        date.append(line[0])
        hour.append(line[1])
        demand.append(line[2])

    date = date[1:]
    hour = hour[1:]
    demand = demand[1:]
    hour = map(float, hour)
    demand = map(float, demand)

    # 取标幺
    date_location = date.index(forecast_date)-24
    hour_use = hour[date_location-24*14:date_location]
    demand_use = demand[date_location-24*14:date_location]

    groups = len(hour_use)/24
    demand_use_average = []
    demand_use_total = []
    for i in range(groups):
        demand_use_total.append(sum(demand_use[24*i:(23+24*i)])/24)
        for j in range(23):
            demand_use_average.append(demand_use[24*i+j]/demand_use_total[i])

    # print demand_use_average
    a = 0.58
    Day = 24
    P = []
    k = []
    Px = []
    error = []
    for m in range(16):
        k.append(a*(1-a)**m)

    for i in range(24):
        Pt = 0
        A1t = 0
        A2t = 0
        for j in range(13):
           Pt += k[j+2]*demand_use[-(j+1)*Day+i]

        Pt = Pt - k[8]*demand_use[-6*Day+i] - k[15]*demand_use_average[-13*Day+i] + k[0]*demand_use_average[-6*Day+i] + k[1]*demand_use_average[-13*Day+i]

        for j in range(6):
            A1t += k[j]*demand_use[-(j+1)*Day]
            A2t += k[j]*demand_use[-(j+7)*Day]
        Px.append(A1t * demand_use[-(6 * Day) + i] / A2t)
        P.append(Pt)

    # 计算拟合误差
    error.append(((demand[date_location + 24 + i] - Px[i]) / demand[date_location + 24 + i]) ** 2)
    sum_error = np.sum(error)
    error_ave = (1 - np.sqrt(sum_error / 24)) * 100
    truth_demand = demand[(date_location + 24):(date_location + 48)]

    return Px, truth_demand, sum_error


# 多天预测的函数
def forecast_more(first_day, num_of_day, filename,file_write_name):
    csvfile=file(filename, 'rb')
    data = csv.reader(csvfile)
    date = []
    str_day = []
    for line in data:
        date.append(line[0])
    csvfile.close()

    date = date[1:]
    for i in range(len(date)/24):
        str_day.append(date[i*24])
    day_location = str_day.index(first_day)
    forecast_day = str_day[day_location:(day_location + num_of_day)]
    fore_demand = []
    truth_demand = []
    error_fore = []
    time = []   # store the time for write_file
    for date in forecast_day:
        for iter in range(1,25):
            time.append(date + "/" + str(iter))
        [fore_day_demand, truth_day_demand, error_day] = forecast_one(date,filename)
        print error_day
        fore_demand += fore_day_demand
        truth_demand += truth_day_demand
        error_fore.append(error_day)
    error_ave = (1 - np.sqrt(np.sum(error_fore) / (24 * num_of_day))) * 100

    resultCsv = file(file_write_name,'wb')
    writer = csv.writer(resultCsv)
    writer.writerow(['time','forecast_demand','real_demand'])
    for iter in range(0,len(time)):
        writer.writerow([time[iter], fore_demand[iter], truth_demand[iter]])
    resultCsv.close()

    # do the json structure
    data = []
    for iter in range(0, len(time)):
        dict = {"yy-mm-dd-hour":time[iter],"predictDemand":fore_demand[iter],\
                "realDemand":truth_demand[iter]}
        data.append(dict)
    dataJson = json.dumps(data)
    return dataJson

# 计算所有的误差值
def error_print(filename,file_write_name):
    #filename = os.path.join('..', 'ExampleData.csv')
    data = csv.reader(file(filename, 'rb'))
    date = []
    str_day = []
    dry_temper = []
    wet_temper = []
    for line in data:
        date.append(line[0])
        dry_temper.append(line[3])
        wet_temper.append(line[4])
    date = date[1:]
    dry_temper = dry_temper[361:]
    wet_temper = wet_temper[361:]
    for i in range(len(date)/24):
        str_day.append(date[i*24])

    str_day = str_day[15:]
    fore_demand = []
    truth_demand = []
    error_fore = []
    for date in str_day:
        [fore_day_demand, truth_day_demand, error_day] = forecast_one(date,filename)
        fore_demand += fore_day_demand
        truth_demand += truth_day_demand
        error_fore += [error_day]


    delta_demand = [x-y for x, y in zip(truth_demand, fore_demand)]
    csvfile = csv.writer(file(file_write_name, "wb"))
    csvfile.writerow(['forecast', 'truth', 'delta', 'drytemper', 'wettemper'])
    for i in range(len(fore_demand)):
        data = [fore_demand[i]] + [truth_demand[i]] + [delta_demand[i]] + [dry_temper[i]] + [wet_temper[i]]
        csvfile.writerow(data)
        # print data
    csvfile.close()
    return 0


# 计算最小误差的a
def calculate(fit_a,filename):
    #filename = os.path.join('..', 'ExampleData.csv')
    data = csv.reader(file(filename, 'rb'))
    date = []
    str_day = []
    hour = []
    demand = []
    for line in data:
        date.append(line[0])
        hour.append(line[1])
        demand.append(line[2])

    date = date[1:]
    for i in range(len(date)/24):
        str_day.append(date[i*24])

    str_day = str_day[15:]
    hour = hour[1:]
    demand = demand[1:]
    hour = map(float, hour)
    demand = map(float, demand)
    sum_error = []
    for forecast_date in str_day:
        # 取标幺
        date_location = date.index(forecast_date) - 24
        hour_use = hour[date_location - 24 * 14:date_location]
        demand_use = demand[date_location - 24 * 14:date_location]

        groups = len(hour_use) / 24
        demand_use_average = []
        demand_use_total = []
        for i in range(groups):
            demand_use_total.append(sum(demand_use[24 * i:(23 + 24 * i)]) / 24)
            for j in range(23):
                demand_use_average.append(demand_use[24 * i + j] / demand_use_total[i])

        # print demand_use_average

        Day = 24
        P = []
        k = []
        Px = []
        error = []
        for m in range(16):
            k.append(fit_a * (1 - fit_a) ** m)

        for i in range(24):
            Pt = 0
            A1t = 0
            A2t = 0
            for j in range(13):
                Pt += k[j + 2] * demand_use[-(j + 1) * Day + i]

            Pt = Pt - k[8] * demand_use[-6 * Day + i] - k[15] * \
                demand_use_average[-13 * Day + i] + k[0] * demand_use_average[\
                -6 * Day + i] + k[1] * demand_use_average[-13 * Day + i]
            for j in range(6):
                A1t += k[j] * demand_use[-(j + 1) * Day]
                A2t += k[j] * demand_use[-(j + 7) * Day]
            Px.append(A1t * demand_use[-(6 * Day) + i] / A2t)
            P.append(Pt)

        # 计算拟合误差
        error.append(((demand[date_location + 24 + i] - Px[i])\
                      / demand[date_location + 24 + i]) ** 2)
        temp = np.sum(error)
        sum_error.append(temp)

    calculate_error = np.sum(sum_error)
    # print len(sum_error)

    return calculate_error

def main():
    dataJson = forecast_more('2004/10/20', 2,\
                             "../ExampleData.csv","../ExampleResult.csv")
    print(json.loads(dataJson))


if __name__== '__main__':
    main()
#error_print("../ExampleData.csv","../Example_result.csv")
# error_05 = calculate(0.8)
# print error_05

# forecast_one('2003/3/15')
# Question: 为什么不能预测2003/3/15

# error01 = []
# a = np.arange(0.5, 1, 0.01)
# for x in a:
#     error_temp = calculate(x)
#     error01.append(error_temp)
#
# print error01
# 上面的计算表示a = 0.58 是最好

