import os.path
import sys
from collections import deque

tunnel = input('Please enter the name of the file you want to get data from: ')
check_tunnel = os.path.exists(tunnel)
if not check_tunnel:
    print('Sorry, there is no such file.')
    sys.exit()

def check_file(file_name):  # 这个函数负责检查打开的文件里面的行是否有问题
    with open(file_name) as t_file:
        rows = []  # 这个list用来存行
        lines = t_file.readlines()  # 读取每一行
        for _ in range(len(lines)):
            if '\n' in lines:  # 检查是否添加了空行
                lines.remove('\n')  # 添加了就把空行移除
            else:
                break
        for row in lines:
            if row.split() != '\n':  # 如果这一行里面是有东西的
                rows.append(row)  # 那么就把这一行添加到list里面

        # print(lines)

    element_list = []
    if len(rows) != 0:  # 如果存在行
        if len(lines) == 2:  # 如果行数是严格等于2的
            element_list_1 = deque()  # 创建一个放置天花板的deque
            for element1 in rows[0]:
                element_list_1 += element1.split()  # 用split分开装进list
            for index1 in range(len(element_list_1)):
                if not element_list_1[index1].isdigit():  # 如果这个行里面有不是数字的元素
                    element_list_1.clear()  # 就把装行1的list清空，然后结束这个for循环
                    break
            for index1_1 in range(len(element_list_1)):  # 进行str-int转换
                item1 = element_list_1[index1_1]
                element_list_1.remove(element_list_1[index1_1])  # 先去除这个str型的元素
                element_list_1.appendleft(int(item1))  # 再把这个元素的int型从左边添加到deque里面
            element_list_1 = list(element_list_1)[::-1]  # 转换成list，再翻转顺序

            # print(element_list_1)

            element_list_2 = deque()  # 第二行的操作同第一行
            for element2 in rows[1]:
                element_list_2 += element2.split()  # 用split分开装进list
            for index2 in range(len(element_list_2)):
                if not element_list_2[index2].isdigit():  # 如果这个行里面有不是数字的元素
                    element_list_2.clear()  # 就把装行2的list清空，然后结束这个for循环
                    break
            for index2_2 in range(len(element_list_2)):
                item2 = element_list_2[index2_2]
                element_list_2.remove(element_list_2[index2_2])
                element_list_2.appendleft(int(item2))
            element_list_2 = list(element_list_2)[::-1]

            # print(element_list_2)

            if len(element_list_1) == len(element_list_2):  # 如果两行元素个数一致才正确
                if len(element_list_1) > 1:  # 如果每一行的元素大于1个，才正确
                    element_list.append(element_list_1)  # 将两行添加到二维列表中
                    element_list.append(element_list_2)
                    for index in range(len(element_list_1)):  # 检查天花板是不是严格高于地面
                        if element_list_1[index] <= element_list_2[index]:
                            element_list.clear()
                            break

            # print(element_list)
    return element_list

def check_left_most_distance(list):  #计算从西边看进来的最大距离
    left_most_distance = 0
    up_smallest = list[0][0]
    down_smallest = list[1][0]
    for index in range(1, len(list[0])):
        if list[0][index] <= down_smallest or list[1][index] >= up_smallest:
# 如果有一个天花板低于前面这个索引值之前的最高地面，或者有一个地面高于前面这个索引值之前的最低天花板
            left_most_distance += index  # 则停止循环，此时的index就是最大的距离
            break
        if list[0][index] < up_smallest:  # 如果此时的天花板比前面索引值的天花板低，则此时索引的天花板是最低的
            up_smallest = list[0][index]
        if list[1][index] >up_smallest:
            down_smallest = list[1][index]  # 如果此时的地面比前面索引值的地面高，则此时索引的地面是最高的
    return left_most_distance

def check_inside_longest_space(list):  # 找到通道内部的平行最长距离
    max_space = 1  # 初始化一个最大距离，方便后面对比
    space = 1
    for index1 in range(1, len(list[0])):
        up = list[0][index1]  # 找到当前位置的天花板高度
        down = list[1][index1]  # 找到当前位置的地面高度
        for item in range(down + 1, up + 1):  # 通道高度在天花板和地面之间
            for index2 in range(1, len(list[0]) - index1 + 1):  # 往后推移位置
                if index2 != len(list[0]) - index1:  # 还没到通道最后
                    if list[1][index1 + index2] < item <= list[0][index1 + index2]: # 如果当前的高度大于后一位的地面，小于和后一位的天花板
                        space += 1  # 就把距离+1
                    else:
                        if space > max_space:  # 当此时的高度不符合条件时，将它的水平距离与最大值对比
                            max_space = space  # 如果此时的水平距离更大，则取代原来的最大距离
                        space = 1  # 复位原始距离，方便下一个高度计算水平距离
                        break  # 结束循环，跳到更上一层的高度
                else:  # 到达通道最后
                    if space > max_space:  # 同样与最大距离对比
                        max_space = space  # 更大则取代
                    space = 1  # 复位原始距离
                    break  # 结束循环，跳到更上一层的高度
    return max_space

after_check = check_file(tunnel)  # 检查读取文件的每一行和其中的值
if len(after_check) != 0:  # 当检查完文件之后，得到的二维list不是空时，才继续
    from_west = check_left_most_distance(after_check)  # 调用计算从西看最大水平距离函数
    print("From the west, one can into the tunnel over a distance of", from_west)
    maximum_distance = check_inside_longest_space(after_check)  # 调用计算内部最大水平距离函数
    print("Inside the tunnel, one can into the tunnel over a maximum distance of", maximum_distance)
else:  # 否则输出文件内容错误信息
    print('Sorry, input file does not store valid data.')