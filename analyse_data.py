import csv
import matplotlib.pyplot as plt
import numpy as np


def get_height(final_h_list):
    # 得到高度
    threshold = 50
    final_height = min(final_h_list)
    if len(final_h_list) <= 15:
        for id, h in enumerate(final_h_list):
            if h > final_height:
                if id == 0 or id == len(final_h_list) - 1:
                    continue
                if 0 < h - final_h_list[id - 1] < 50:
                    final_height = h
    else:
        for id, h in enumerate(final_h_list):
            if h > final_height:
                if id <= 3 or id >= len(final_h_list) - 4:
                    continue
                diff1 = final_h_list[id-3]-final_h_list[id-4]
                diff2 = final_h_list[id-2]-final_h_list[id-3]
                diff3 = final_h_list[id-1]-final_h_list[id-2]
                diff4 = h - final_h_list[id-1]

                diff5 = final_h_list[id+1]-h
                diff6 = final_h_list[id+2]-final_h_list[id+1]
                diff7 = final_h_list[id+3]-final_h_list[id+2]
                diff8 = final_h_list[id+4]-final_h_list[id+3]

                diff_front = diff1+diff2+diff3+diff4
                diff_behind = diff5+diff6+diff7+diff8
                diff_front_abs = abs(diff1)+abs(diff2)+abs(diff3)+abs(diff4)
                diff_behind_abs = abs(diff5)+abs(diff6)+abs(diff7)+abs(diff8)
                if 100 > diff_front >= 0 and -100 < diff_behind <= 0 and diff_behind_abs < 100 and diff_front_abs < 100:
                    # final_height = max(final_height, h)
                    final_height = h
                    print(h)

    return final_height


if __name__ == '__main__':
    data_list = []
    with open('tobesolved_list/data.csv', 'r', encoding='utf-8') as fp:
        csv_reader = csv.reader(fp)
        data_list = list(csv_reader)
    for i, data in enumerate(data_list):
        # if i != len(data_list) - 1:
        #     continue
        np_i = np.array(range(len(data)))
        np_data = np.array([int(float(item)) for item in data])
        # print(np_i)
        print(np_data)
        plt.subplot(10, 10, i + 1)
        plt.plot(np_i, np_data, 'o', markersize = 1)
        # print(get_height([int(item) for item in data]))
        height = get_height([int(float(item)) for item in data])
        tmp = list([height] * len(data))
        tmp = np.array(tmp)
        plt.plot(np_i, tmp, 'r')

    plt.show()

