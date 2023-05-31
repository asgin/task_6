import argparse
import datetime
from pathlib import Path
from tabulate import tabulate


def add_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files')
    parser.add_argument('--driver')
    parser.add_argument('--desc', action='store_true')
    args = parser.parse_args()
    return args


def calculate_time(time1, time2):
    time_format = '%H:%M:%S.%f'
    datetime1 = datetime.datetime.strptime(time1.strip(), time_format)
    datetime2 = datetime.datetime.strptime(time2.strip(), time_format)
    time_diff = abs(datetime1 - datetime2)
    return str(time_diff)

def read_abbreviations(fil_p):
    with open(Path(f'{fil_p}/abbreviations.txt'), 'r') as f:
        racers = [i.strip() for i in f.readlines()]
        s = {}
        for i in racers:
            s[i.split('_')[0]] = i.split('_')[1:]
        return s


def calculate(file_p):
    with open(Path(f'{file_p}/start.log'), 'r') as f:
        with open(Path(f'{file_p}/end.log'), 'r') as fi:
            file_start = sorted([i.split('_') for i in f.readlines()], key=lambda x: x[0].strip())
            file_end = sorted([i.split('_') for i in fi.readlines()], key=lambda x: x[0].strip())
            s = {}
            del file_start[0]
            for i, j in zip(file_start, file_end):
                s[i[0]] = calculate_time(j[1], i[1])
    return s

def return_res(diction, dict2):
    dict2 = dict(sorted(dict2.items(), key=lambda x: x[0]))
    diction = dict(sorted(diction.items(), key=lambda x: x[0]))
    list_time = [['_'.join(dict2[abr]), diction[r]] for abr, r in zip(dict2.keys(), diction.keys())]
    list_time = sorted(list_time, key=lambda x: x[1])
    return list_time

def read_args(args):
    if args.desc and not args.driver and args.files:
        hears = ['Racer', 'Time']
        res = return_res(calculate(args.files), read_abbreviations(args.files))[::-1]
        print(tabulate(res, headers=hears, tablefmt='grid', stralign='center'))
    if args.desc == False and not args.driver and args.files:
        hears = ['Racer', 'Time']
        print(tabulate(return_res(calculate(args.files), read_abbreviations(args.files)), headers=hears, tablefmt='grid', stralign='center'))
    if args.driver and args.files:
        print(f'{args.driver} -- {dict(return_res(calculate(args.files), read_abbreviations(args.files)))[args.driver]}')

read_args(add_args())
