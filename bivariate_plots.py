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


def plot_bi(data, headers, data_types, filename):

    dirpath = 'saved_plots/{}_Bivariate_Plots'.format(filename)
    sub_folders = ['scatter_2d_plots', 'line_2d_plots',
                   'scatter_2d_plots_with_hue', 'line_2d_plots_with_hue']
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    os.makedirs(dirpath)
    for i in sub_folders:
        if os.path.exists(i) and os.path.isdir(i):
            shutil.rmtree(i)

        os.makedirs(dirpath+'/'+i)

    palette = itertools.cycle(sns.color_palette())
    float_unis, object_unis, int_unis = get_dtype_groups(data_types)

    ###################################### PAIR PLOT W/O HUE ############################################

    try:
        fig, ax = plt.subplots()
        if len(data.columns) > 4:
            data = data[:, :4]
        sns.pairplot(data)
        plt.savefig('./{}/pair_plot_without_hue.png'.format(dirpath))
    except Exception as e:
        print(e)
        print('error occured while plotting pairplot without hue.')

    ####################################### PAIR PLOT WITH HUE ##########################################

    try:
        fig, ax = plt.subplots()
        if len(object_unis) > 0:
            for i in object_unis[0]:
                unique_values = len(pd.unique(data[i]))
                if unique_values > 20:
                    continue
                print('making hue of ', i)
                if len(data.columns) > 4:
                    data = data[:, :4]
                sns.pairplot(data, hue=i)
                fig.set_size_inches(18.5, 10.5)
                plt.savefig('./{}/pair_plot_w_{}_hue.png'.format(dirpath, i))
                print('saved hue')
    except Exception as e:
        print(e)
        print('error occured while plotting {} column.'.format(i))

    ###################################### SCATTER SEPARATED WITHOUT HUE #########################################
    if len(float_unis) > 0:
        if len(int_unis) > 0:
            cols = float_unis[0]+int_unis[0]
            if len(cols) > 4:
                cols = cols[:4]
            pairs_2d = findsubsets(cols, 2)
        else:
            cols = float_unis[0]
            if len(cols) > 4:
                cols = cols[:4]
            pairs_2d = findsubsets(cols, 2)

        try:
            print('here are 2d pairs ', pairs_2d)
            for j in pairs_2d:
                fig, ax = plt.subplots()

                sns.scatterplot(data=data, x=data[j[0]], y=data[j[1]])
                fig.set_size_inches(18.5, 10.5)
                plt.savefig(
                    './{}/scatter_2d_plots/scatter_plot_{}_with_{}_without_hue.png'.format(dirpath, j[0], j[1]))

                fig, ax = plt.subplots()
                sns.lineplot(data=data, x=data[j[0]], y=data[j[1]])
                fig.set_size_inches(18.5, 10.5)
                plt.savefig(
                    './{}/line_2d_plots/line_plot_{}_with_{}_without_hue.png'.format(dirpath, j[0], j[1]))

        except Exception as e:
            print(e)
            print('error occured while plotting {} column.'.format(j))
            
   ###################################### SCATTER SEPARATED WITH HUE #########################################

        try:
            for j in pairs_2d:
                if len(object_unis) > 0:
                    for k in object_unis[0]:
                        unique_values = len(pd.unique(data[k]))
                        if unique_values > 20:
                            continue
                        fig, ax = plt.subplots()
                        sns.scatterplot(
                            data=data, x=data[j[0]], y=data[j[1]], hue=data[k])
                        fig.set_size_inches(18.5, 10.5)
                        plt.savefig(
                            './{}/scatter_2d_plots_with_hue/scatter_plot_{}_with_{}_hue.png'.format(dirpath, j[0], j[1]))

                        fig, ax = plt.subplots()
                        sns.lineplot(
                            data=data, x=data[j[0]], y=data[j[1]], hue=data[k])
                        fig.set_size_inches(18.5, 10.5)
                        plt.savefig(
                            './{}/line_2d_plots_with_hue/line_plot_{}_with_{}_with_hue.png'.format(dirpath, j[0], j[1]))
        except Exception as e:
            print(e)
            print('error occured while plotting {} column with {} column.'.format(j, k))
