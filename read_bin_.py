import csv
import math
import os

import numpy as np
from matplotlib import pyplot as plt

import vis

filepath = "./"


def get_from_bin(path, idx1, idx2):

    pointcloud = np.fromfile(path, dtype=np.float32).reshape(-1, 4)
    my_data = pointcloud.tolist()
    new_data = [data for data in my_data if idx1<=data[0]<=idx2]
    return new_data


def get_heights(filepath, savepath, idx1, idx2):
    h_list = []
    l_list = []
    all_data = get_from_bin(filepath, idx1, idx2)
    tire_height = 0
    tire_height_list = []
    new_llist = []
    new_hlist = []
    x = idx1
    entire_h_list = []
    l_average_list = []
    for data in all_data:
        if data[0] < (idx1+idx2)//2:
            continue
        elif data[0] == (idx1+idx2)//2 and data[2]<600:
            l_average_list.append(data[1])
        else:
            break
    l_average_list.remove(max(l_average_list))
    l_average_list.remove(min(l_average_list))
    average_l = sum(l_average_list)/len(l_average_list)
    for item in all_data:
        idx = item[0]
        if idx == x:
            if len(l_list) == 0:
                pre_h = item[2]
                pre_l = item[1]
            # new_llist.append(item[1])
            # new_hlist.append(item[2])
            if item[2] < pre_h or abs(item[1] - average_l) > 400:# or abs(pre_l - item[1]) > 250
                continue
            l_list.append(item[1])
            h_list.append(item[2])
            # print(f'l:{item[1]}    h:{item[2]}')
            if 800 > abs(item[2] - pre_h) > 40 and abs(item[1] - pre_l) < 800 and 1200 > pre_h > 500:
                print(f'h{pre_h}')
                tire_height_list.append([pre_h, pre_l])
                # tire_height = pre_h
                # break
            # if 800 > abs(item[2] - pre_h) > 50 and abs(item[1] - pre_l) > 40 and 1200 > item[2] > 600:
            #     print(f'h{item[2]}')
            #     tire_height = item[2]
            pre_h = item[2]
            pre_l = item[1]

        else:
            if len(tire_height_list) != 0:
                if len(entire_h_list) == 0:
                    final_h = tire_height_list[0][0]
                    tmp_l = tire_height_list[0][1]
                    for item_h, item_l in tire_height_list:
                        if item_l < tmp_l:
                            tmp_l = item_l
                            final_h = item_h
                    entire_h_list.append(final_h)
                    # entire_h_list.append(max(tire_height_list))
                else:
                    temp_for_h = []
                    for index_h, item_hl in enumerate(tire_height_list):
                        temp_for_h.append(abs(entire_h_list[-1] - item_hl[0]))
                    final_index = temp_for_h.index(min(temp_for_h))
                    entire_h_list.append(tire_height_list[final_index][0])
                print('')
            else:
                entire_h_list.append(0)
            tire_height_list = []
            x += 1
            if x == idx2+1:
                break
            pre_h = item[2]
            pre_l = item[1]

        # all_data2.append(item)
    # all_data2.append(item)

    # if len(tire_height_list) != 0:
    #     tire_height = max(tire_height_list)
    # print(f'tire height:{tire_height}')
    print(entire_h_list)
    write_flag = False
    write_flag = True
    if write_flag:
        with open('/home/zhy/get_tire_height/tobesolved_list/data.csv', 'a', encoding='utf-8') as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerow(entire_h_list)
            print('写入成功')

    if savepath is not "":
        if not os.path.exists(savepath):  # 如果路径不存在
            os.makedirs(savepath)
        binpc = np.array(all_data)
        binpc = binpc.reshape(-1, 4).astype(np.float32)
        filename = filepath.split('/')[-1].replace('dat', 'bin')
        binpc.tofile(savepath + '/' + filename)
    return entire_h_list


def get_tire_height(filepath, savepath, idx1, idx2):
    final_h_list = []
    h_list = get_heights(filepath, savepath, idx1, idx2)

    # 去掉h_list中的0
    # for h in h_list:
    #     if h != 0:
    #         final_h_list.append(h)
    # 取中位数作为标准
    tmp = []
    tmp += final_h_list
    tmp.sort()
    if len(final_h_list) == 0:
        return
    else:
        final_height = tmp[len(final_h_list) // 2]
    print('standard:', final_height)
    # 用于得到连续有效值
    flag_num_list = []
    # flag_num = final_h_list[2]
    if len(final_h_list)< 4:
        print('h_list < 4')
        return
    for item in range(4):
        flag_num_list.append(final_h_list[item])
    flag_num_list.remove(max(flag_num_list))
    flag_num_list.remove(min(flag_num_list))
    flag_num = sum(flag_num_list) / len(flag_num_list)
    print(f'initiative flag_num:{flag_num}')
    if flag_num > 800:
        threshold = 75
    else:
        threshold = 120
    for id, h in enumerate(final_h_list):
        if 1200 > h > 500:
            if h > final_height and abs(flag_num - h) < threshold:
                    final_height = h
                    # print('final_height:{}'.format(h))
                    flag_num = h
                    # print('flag_num:', flag_num)
            elif abs(flag_num - h) < threshold:
                flag_num = h
                # print('flag_num:', flag_num)
            if h > 800:
                threshold = 75
            else:
                threshold = 120
    # for id, h in enumerate(final_h_list):
    #     if 1200 > h > 500:
    #         if h > final_height and abs(flag_num - h) < threshold:
    #             print('')
    return final_height


if __name__ == '__main__':
    filepath = "/home/zhy/get_tire_height/10.bin"
    if not os.path.exists(filepath):
        # os.mkdir(filepath.replace("/tire.dat", ""))
        print("can't find tire.dat")
        exit(0)

    savepath = "./get_tire_height/bin"
    idx1 = 13 # 100
    idx2 = 24

    tire_height = get_tire_height(filepath, savepath, idx1, idx2)
    a = vis.visScan()
    filename = filepath.split('/')[-1].replace('dat', 'bin')
    print(f'final height: {tire_height}')

    a.show(savepath + '/' + filename)


