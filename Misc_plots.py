
import json
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
import os
import shutil


def get_dtype_groups(data_types):
    float_unis = []
    object_unis = []
    int_unis = []
    for i, v in data_types.items():
        if i == np.dtype('float64') or i == np.dtype('float32'):
            float_unis.append(v)
        if i == np.dtype('O'):
            object_unis.append(v)
        if i == np.dtype('int64') or i == np.dtype('int32') or i == np.dtype('int16'):
            int_unis.append(v)

    return float_unis, object_unis, int_unis


def findsubsets(s, n):

    return list(itertools.permutations(s, n))


def plot_3d(data, headers, data_types, filename):

    dirpath = 'saved_plots/{}_Misc_Plots'.format(filename)
    sub_folders = ['scatter_3dPlots']
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    os.makedirs(dirpath)
    for i in sub_folders:
        if os.path.exists(i) and os.path.isdir(i):
            shutil.rmtree(i)

        os.makedirs(dirpath+'/'+i)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    float_unis, object_unis, int_unis = get_dtype_groups(data_types)
    palette = itertools.cycle(sns.color_palette())

    if len(float_unis) > 0:
        if len(int_unis) > 0:
            cols = float_unis[0]+int_unis[0]
            if len(cols) > 4:
                cols = cols[:4]
            pairs_3d = findsubsets(cols, 3)
        else:
            cols = float_unis[0]
            if len(cols) > 4:
                cols = cols[:4]
            pairs_3d = findsubsets(cols, 3)

        try:
            for j in pairs_3d:
                fig = plt.figure()
                ax = plt.axes(projection='3d')
                ax.scatter(data[j[0]], data[j[1]],
                           data[j[2]], color=next(palette))
                ax.legend()
                x = j[0]
                ax.set_xlabel(x, fontsize=20)
                ax.set_ylabel(j[1], fontsize=20)
                ax.set_zlabel(j[2], fontsize=20, rotation=0)
                fig.set_size_inches(18.5, 10.5)
                plt.savefig(
                    './{}/scatter_3dPlots/{}_{}_{}_set.png'.format(dirpath, j[0], j[1], j[2]))
        except Exception as e:
            print(e)
            print('error occured while plotting {} columns.'.format(j))


def plot_groupby(data, headers, data_types, filename):
    dirpath = 'saved_plots/{}_Misc_Plots'.format(filename)
    float_unis, object_unis, int_unis = get_dtype_groups(data_types)

    try:
        if len(object_unis) > 0:
            for j in object_unis[0]:
                df = data.groupby(j).mean()
               # print(df)
                fig, ax = plt.subplots()
                df.plot(kind='bar')
                fig.set_size_inches(18.5, 10.5)
                unique_values = len(pd.unique(data[j]))
                if unique_values > 30:
                    continue
                plt.savefig('./{}/groupby_{}_bar_plot.png'.format(dirpath, j))
    except Exception as e:
        print(e)
        print('error occured while plotting groupby by {} column.'.format(j))
