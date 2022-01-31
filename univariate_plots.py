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


def plot_uni(data, headers, data_types, filename):

    dirpath = 'saved_plots/{}_Univariate_Plots'.format(filename)
    sub_folders = ['histograms', 'distplots', 'count_plots']
    if os.path.exists(dirpath) and os.path.isdir(dirpath):

        shutil.rmtree(dirpath)

        os.makedirs(dirpath)
    for i in sub_folders:
        if os.path.exists(i) and os.path.isdir(i):
            shutil.rmtree(i)

        os.makedirs(dirpath+'/'+i)

    float_unis, object_unis, int_unis = get_dtype_groups(data_types)

    palette = itertools.cycle(sns.color_palette())

    ####################################### FOR FLOAT COlUMNS ################################################
    if len(float_unis) > 0:
        try:
            for j in range(len(float_unis[0])):
                if j == 4:
                    break
                fig, ax = plt.subplots()

                sns.histplot(data=data, x=float_unis[0][j], color=next(
                    palette), ax=ax, label=float_unis[0][j], kde=True)
                fig.set_size_inches(18.5, 10.5)
                plt.savefig(
                    './{}/histograms/hist_plot_{}.png'.format(dirpath, float_unis[0][j]))
        except Exception as e:
            print(e)
            print('error occured while plotting {} column.'.format(
                float_unis[0][j]))

        try:

            fig, ax = plt.subplots()
            for j in range(len(float_unis[0])):
                if j == 4:
                    break
                sns.histplot(data=data, x=float_unis[0][j], color=next(
                    palette), ax=ax, label=float_unis[0][j], kde=True)
            fig.set_size_inches(18.5, 10.5)
            plt.legend()
            plt.savefig('./{}/histograms/hist_plot.png'.format(dirpath))

        except Exception as e:
            print(e)
            print('error occured while plotting {} column.'.format(
                float_unis[0][j]))

        try:
            for j in range(len(float_unis[0])):
                if j == 4:
                    break
                fig, ax = plt.subplots()

                sns.distplot(data[float_unis[0][j]], color=next(
                    palette), ax=ax, label=float_unis[0][j], kde=True)
                fig.set_size_inches(18.5, 10.5)
                plt.savefig(
                    './{}/distplots/dist_plot_{}.png'.format(dirpath, float_unis[0][j]))

        except Exception as e:
            print(e)
            print('error occured while plotting {} column.'.format(
                float_unis[0][j]))

        try:
            fig, ax = plt.subplots()
            for j in range(len(float_unis[0])):
                if j == 4:
                    break

                sns.distplot(data[float_unis[0][j]], color=next(
                    palette), ax=ax, label=float_unis[0][j], kde=True)
            fig.set_size_inches(18.5, 10.5)
            plt.legend()
            plt.savefig('./{}/distplots/dist_plot.png'.format(dirpath))
        except Exception as e:
            print(e)
            print('error occured while plotting {} column.'.format(
                float_unis[0][j]))

        X_axis = []
        for j in range(len(data)):
            X_axis.append(j)
        # data=data[:,:4]
        df = data[float_unis[0]]
        df['X_axis'] = X_axis
        # print(df)
        try:
            dfm = df.melt('X_axis', var_name='cols', value_name='vals')
            fig, ax = plt.subplots()

            box_plot = sns.boxplot(
                data=data, ax=ax, linewidth=0.5, fliersize=1)
            plt.xticks(rotation=60, ha='right', size=10)
            fig.set_size_inches(18.5, 10.5)
            plt.savefig('./{}/box_plot.png'.format(dirpath))
        except Exception as e:
            print(e)
            print('error occured while plotting box plot')

    ###################################### FOR OBJECT COLUMNS ##############################################

    try:

        fig, ax = plt.subplots()
        if len(object_unis) > 0:
            for i in object_unis[0]:

                unique_values = len(pd.unique(data[i]))

                if unique_values > 30:
                    top_20 = data[i].value_counts()[:20].index.tolist()

                    tmp_data = data[data[i].isin(top_20)]

                else:
                    tmp_data = data
                sns.countplot(x=i, data=tmp_data)

                plt.xticks(rotation=60, ha='right', size=10)
                fig.set_size_inches(18.5, 10.5)
                plt.savefig(
                    './{}/count_plots/count_plot_{}.png'.format(dirpath, i))

    except Exception as e:
        print(e)
        print('error occured while plotting {} column.'.format(i))

    ##################################### FOR INTEGER COLUMNS ##############################################
    if len(int_unis) > 0:
        X_axis = []
        for j in range(len(data)):
            X_axis.append(j)
        df = data[int_unis[0]]
        df['X_axis'] = X_axis
        # print(df)
        dfm = df.melt('X_axis', var_name='cols', value_name='vals')
