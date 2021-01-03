import os.path
import sys

from collections import defaultdict

# This 4 line copied from Eric Martin - 20T2 COMP9021 quiz_1
data_file_name = input('Please enter the name of the file you want to get data from: ')
if not os.path.exists(data_file_name):
    print('Sorry, there is no such file.')
    sys.exit()

def check_file_line(file_name):  # 这个函数负责检查打开的文件里面的行是否有问题
    rows = []  # 这个list用来存行
    elements = defaultdict(list)  # 创建一个用来装每一行的字典
    with open(file_name) as file:   # 打开文件
        lines = file.readlines()  # 读取每一行
        for row in lines:
            if row.split():   # 如果这一行里面是有东西的
                rows.append(row)  # 那么就把这一行添加到list里面
    if len(rows) > 1:  # 如果行数大于1，才对
        element_list = []  # 这个list用来装每一行的那些数字
        for element in rows:
            element_list += element.split()   # 用split分开装进list
        for index in range(len(element_list)):
            if not element_list[index].isdigit(): # 如果这个行里面有不是数字的元素
                elements.clear()   # 就把装行的字典清空，然后结束这个for循环
                break
            else:
                elements[element_list[index]] = 1  # 如果全是数字，就把该数字元素作为key，添加到字典里
    else:  # 如果行数小于等于1
        elements.clear()  # 清空字典
    return elements

def check_file_data(dict):  # 这个函数用来判断打开的文件里面的数字是不是按要求排序的
    dict_keys = []   # 这个用来存放每一个字典的key，也就是打开文件中的每一个数字
    for keys in dict.keys():  # 将数字添加到list里
        dict_keys.append(keys)
    for index in range(1, len(dict_keys)):
        if int(dict_keys[index]) - int(dict_keys[index - 1]) <= 0:  # 如果第一个数字大于第二个数字，那么
            dict_keys = []  # 清空存放数字的list，结束for循环
            break
    return dict_keys

def translation(list):  # 把一个list里面的所有元素转换成int值，
    new_list = []
    for item in list:  # 主要用于转换上一个函数所获得的key，因为添加时都是str
        new_list.append(int(item))
    return new_list

def find_ride(list):  # 这个函数用来找到所有数字之间，前后两个的差值
    new_list = translation(list)  # 先把所有元素转换成int
    distance_list = []  # 用来存放原始文件里数字的差值
    for index in range(1, len(new_list)):  # 循环查找，前后相减，差值添加到list
        distance = new_list[index] - new_list[index - 1]
        distance_list.append(distance)
    distance_counter = 1  # 下面这些是寻找连续相同的差值的长度，初始为1
    distance_counter_list = []  # 这个list用来存放长度
    for i in range(len(distance_list) - 1):
        if distance_list[i] == distance_list[i + 1]: # 如果前后两个差值相等
            distance_counter += 1 # 那么自定义计数变量+1
        else:
            distance_counter_list.append(distance_counter)  # 否则的话，就把记录好的长度添加到list里面
            distance_counter = 1  # 然后把自定义长度计数变量重置为1
    distance_counter_list.append(distance_counter)  # 如果所有的差值都相等的情况下，上面的for循环永远不会到else去，所以要在最后添加以下长度
    return distance_counter_list

'''

    key_length = []
    for values in equivalence_list_dict.values():
        key_length.append(len(values))
    biggest_minus = max(key_length)


        for index2 in range(index1, max_distance):
            number2 = new_list[index2]
            equivalence_number = number2 - number1
'''

def find_biggest_minus(list_1):  # 这个函数用来找到文件的所有数字中，最长的一个等差数列，也就是后面要减掉的最大值
    new_list = translation(list_1)  # 先把传进来的key转成int
    max_distance = new_list[-1] - new_list[0] + 1  # 找到一个最大的寻找等差次数，就是最后一个值减第一个值
    equivalence_list = []  # 这个list用来存放找到的所有的等差值
    # 下面for找所有等差值
    for index in range(len(new_list) - 1):
        number1 = new_list[index]
        for add_number in range(1, max_distance):  # 从数字1开始实验，累计与原始数字相加
            if int(number1) + add_number in new_list:  # 如果相加的和存在于原始key的list中，就把实验数字添加到list中，因为是一个差值
                equivalence_list.append(add_number)
    # 创建一个defaultdict， key是原list存在的所有等差值，value是这个等差值对应的list
    equivalence_list_dict = defaultdict(list)
    for i in range(len(equivalence_list)):  #第一重for循环，用来找第一个原始数和其存在的等差数列
        if new_list[0] + equivalence_list[i] in new_list: # 从等差的list中一个个取出来
            equivalence_list_dict[equivalence_list[i]].append(new_list[0]) # 如果存在，就把差值作为key，原始数字作为value
            for j in range(len(new_list)):  # 第二重for循环，用来检验后面的原始数是否有等差数列存在
                if (new_list[j] + equivalence_list[i]) in new_list: # 如果有
                    count = 1 # 设置一个强行循环中止条件
                    for k in range(1, len(new_list) - 1):  # 第三重循环，找到一个差值对应的所有原始数，添加到字典中相应差值为key的value中
                        if (new_list[j] + k * equivalence_list[i]) in new_list and \
                            (new_list[j] + k * equivalence_list[i]) not in equivalence_list_dict[equivalence_list[i]]:
                            equivalence_list_dict[equivalence_list[i]].append(new_list[j] + k * equivalence_list[i])
                        else:
                            count = 0  # 直到找不到差值对应的等差数列的原始数，将强行终止条件设置为0
                            break # 首先终止第三层for循环
                    if count == 0:  # 再强行中止第二层for循环
                        break
                else:  # 原始数不存在等差数列，终止第二层for循环
                    break
    return equivalence_list_dict


after_check_line = check_file_line(data_file_name)  # 检查读取文件的每一行
after_check_data = check_file_data(after_check_line)  # 检查没一行的元素是否合格
if len(after_check_data) > 1:  # 同时判断了多个条件：是否只有一行，是否元素严格递增，是否元素全是数字
    if len(find_ride(after_check_data)) == 1:  # 检查有多少种间隔，如果只有一种
        print("The ride is perfect!")  # 就是完美的等差文件
        good_ride_number = max(find_ride(after_check_data)) # 最长的连续等差值，就是唯一的最大值
        print("The longest good ride has a length of:", good_ride_number)
        print("The minimal number of pillars to remove to build a perfect ride from the rest is: 0") # 所以不需要移除元素
    else:  # 否则，就需要移除一些元素，创建最长的完美等差数列
        print("The ride could be better...")
        good_ride_number = max(find_ride(after_check_data)) # 最长的连续等差值，还是find_ride返回的list中的最大值
        print("The longest good ride has a length of:", good_ride_number)
        value_length = []  # 这个list用来存放最长的等差数列的长度
        for v in find_biggest_minus(after_check_data).values(): # 每一个等差数列的元素组成了类型为list的value
            value = sorted(set(v))  # 由于find_biggest_minus中，没有强行终止第一个for，所以会有一些value里面多添加了很多原始数列的第一个数，所以要去重了再排序
            value_length.append(len(value))  # 此时计算的长度才是真实的每一个等差数列的长度
        smallest_remove = len(after_check_data) - max(value_length)  # 用原始数列的总长度，减去最长的等差数列的长度，得到需要移除的元素的个数
        print("The minimal number of pillars to remove to build a perfect ride from the rest is:", smallest_remove)
else:
    print('Sorry, input file does not store valid data.')

