import os
import csv


if __name__ == '__main__':
    file = './tire_info/tire_info.csv'
    filepath = '/home/zhy/readcsv_test_program/save/record/record/'
    filename = filepath + '2/test4/0.dat'
    start_idx = 55
    end_idx = 145
    # with open(file, 'a', encoding='utf-8') as fp:
    #     csv_writer = csv.writer(fp)
    #     csv_writer.writerow(['FilePath', 'Start idx', 'End idx'])
    with open(file, 'a', encoding='utf-8') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow([filepath, start_idx, end_idx])
