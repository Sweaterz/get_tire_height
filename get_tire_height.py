import csv
import math
import os

import numpy as np
from matplotlib import pyplot as plt

import vis

filepath = "./"


def chooseDataDG(filepath):
    use_data = []
    with open(filepath, 'r') as fopen:
        lines = fopen.readlines()
        for idx, line in enumerate(lines):
            line_data = line.split(" ")
            if line_data[0] != 'FC':
                continue
            if len(line_data) < 1813:
                print('this scan data is not enough, discard it!')
                continue
            num_points = int(line_data[19], 16) * 256 + int(line_data[18], 16)
            assert num_points * 2 + 49 - 1 == 1810
            use_data.append(line_data[49: 1810])
    return use_data


def get_heights(filepath, savepath, idx1, idx2):
    lidarAngleStep = 0.125
    start_idx = 0
    end_idx = idx2
    all_data = []
    all_data2 = []
    h_list = []
    l_list = []
    all_all_data = []
    flag = False

    # chooseData
    # idx1 = 2565
    # idx2 = 2614
    use_data = chooseDataDG(filepath)

    if len(use_data) < 30:
        print("this data is not right! please check it! filePath is %s" % filepath)
        return
    # 标定开始
    iHorizontalAngle = 59.20
    iHorizontalHeight = 1685
    min_l = 770
    max_l = 3750
    # 标定结束

    for idx, data in enumerate(use_data):
        size = len(data)
        intend_tire_h = []
        all_data = []
        if idx > idx2 or idx < idx1:
            continue
        for i in range(int(size / 2)):
            MSB = data[i * 2 + 1]
            LSB = data[i * 2]
            distance = int(MSB, 16) * 256 + int(LSB, 16)
            # if data[i * 2 + 4]:
            #     MSB2 = data[i * 2 + 3]
            #     LSB2 = data[i * 2 + 2]
            #     distance2 = int(MSB2, 16) * 256 + int(LSB2, 16)
            if distance < 100:
                continue
            angle0 = i * lidarAngleStep
            # h = int(math.sin(math.radians(angle0)) * distance) + iHorizontalHeight
            # l = int(math.cos(math.fabs(angle0) * math.pi / 180) * distance)
            if angle0 < iHorizontalAngle:
                angle = iHorizontalAngle - angle0
                h = iHorizontalHeight - int(math.sin(math.radians(angle)) * distance)
                l = int(math.cos(math.fabs(angle) * math.pi / 180) * distance)

            elif angle0 > iHorizontalAngle:
                angle = angle0 - iHorizontalAngle
                h = iHorizontalHeight + int(math.sin(math.radians(angle)) * distance)
                l = int(math.cos(math.fabs(angle) * math.pi / 180) * distance)
            else:
                h = iHorizontalHeight
                l = distance
            if 300 < l < 6000 and 5000 > h > 0:  # if l > 300 and l < 4000 and  h < 5000 and h > 0:
                if start_idx == 0:
                    start_idx = idx
                end_idx = idx
            #     all_data.append([idx, l / 20.0, h / 20.0, 150])  # all_data.append([idx, h, l, 150, i])
            if h < 0:
                continue
            # if h > 1195:
            #     continue
            if min_l < l < max_l:
                all_data.append([idx, l, h, 150])

        # filterDiscretePoints
        newScan = []
        for pointIdx, point in enumerate(all_data):
            if all_data[0][2] < 450.0:
                newScan.append(all_data[0])
            if 1 <= pointIdx <= len(all_data) - 2:
                # if point[2] > 450.0:
                preDiffH = abs(point[2] - all_data[pointIdx - 1][2])
                afterDiffH = abs(all_data[pointIdx + 1][2] - point[2])
                if preDiffH > 15.0 or afterDiffH > 15.0:
                    continue
                newScan.append(point)
        if len(newScan):
            all_data = newScan
        all_all_data += all_data
    all_data = all_all_data
    tire_height = 0
    tire_height_list = []
    new_llist = []
    new_hlist = []
    x = idx1
    entire_h_list = []
    for item in all_data:
        idx = item[0]
        if idx == x:
            if len(l_list) == 0:
                pre_h = item[2]
                pre_l = item[1]
            # new_llist.append(item[1])
            # new_hlist.append(item[2])
            if item[2] < pre_h:
                continue
            l_list.append(item[1])
            h_list.append(item[2])
            # print(f'l:{item[1]}    h:{item[2]}')
            if 800 > abs(item[2] - pre_h) > 40 and abs(item[1] - pre_l) < 500 and 1200 > pre_h > 500:
                # print(f'h{pre_h}')
                tire_height_list.append(pre_h)
                # tire_height = pre_h
                # break
            # if 800 > abs(item[2] - pre_h) > 50 and abs(item[1] - pre_l) > 40 and 1200 > item[2] > 600:
            #     print(f'h{item[2]}')
            #     tire_height = item[2]
            pre_h = item[2]
            pre_l = item[1]

        else:
            if len(tire_height_list) != 0:
                entire_h_list.append(max(tire_height_list))
            else:
                entire_h_list.append(0)
            tire_height_list = []
            x += 1
            if x == idx2+1:
                break
            pre_h = item[2]
            pre_l = item[1]

        all_data2.append(item)
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
    # 显示如下
    # np_l = np.array(l_list)
    # np_x = np.array(range(len(l_list)))
    # np_h = np.array(h_list)
    # np_new_l = np.array(new_llist)
    # np_new_x = np.array(range(len(new_llist)))
    # np_new_h = np.array(new_hlist)
    # plt.subplot(2, 10, (11, 12))
    # plt.scatter(np_new_x, np_new_l, s=0.3)
    # plt.ylim(0,2000)
    # plt.ylabel("previous l value")
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (14, 15))
    # plt.scatter(np_new_x, np_new_h, s=0.3)
    # plt.ylabel("previous h value")
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (17, 18))
    # plt.scatter(np_new_x, np_new_l, s=0.3)
    # plt.scatter(np_new_x, np_new_h, s=0.3)
    # # plt.subplot(2, 10, (11,20))
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (19, 20))
    # plt.scatter(np_new_l, np_new_h, s=1)
    # plt.xlim(1000, 3000)
    # plt.ylim(-50, 3000)
    # # plt.axis('equal')
    # plt.xlabel("l value")
    # plt.ylabel("h value")
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (1, 2))
    # plt.scatter(np_x, np_l, s=0.3)
    # plt.ylim(0,2000)
    # plt.ylabel("l value")
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (4, 5))
    # plt.scatter(np_x, np_h, s=0.3)
    # plt.ylabel("h value")
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (7, 8))
    # plt.scatter(np_x, np_l, s=0.3)
    # plt.scatter(np_x, np_h, s=0.3)
    # # plt.subplot(2, 10, (11,20))
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    # plt.subplot(2, 10, (9,10))
    #
    # plt.scatter(np_l, np_h, s=1)
    # plt.xlim(1000, 3000)
    # plt.ylim(-50, 3000)
    # # plt.axis('equal')
    # plt.xlabel("l value")
    # plt.ylabel("h value")
    # plt.grid(visible=True, axis='y', linewidth=0.3)
    #
    # plt.show()
    # print("read format: the file:%s, start_idx:%d, end_idx:%d" % (filepath, start_idx, end_idx))
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
    filepath = "/home/zhy/get_tire_height/1.dat"
    if not os.path.exists(filepath):
        # os.mkdir(filepath.replace("/tire.dat", ""))
        print("can't find tire.dat")
        exit(0)

    savepath = "./get_tire_height/bin"
    idx1 = 31 # 100
    idx2 = 52

    tire_height = get_tire_height(filepath, savepath, idx1, idx2)
    a = vis.visScan()
    filename = filepath.split('/')[-1].replace('dat', 'bin')
    print(f'final height: {tire_height}')

    a.show(savepath + '/' + filename)


