import pandas as pd # import the data as dataframe and manipulate the data
import datetime # to create data-time variables
import matplotlib # to visualize the dataset
import matplotlib.pyplot as plt
import numpy as np
import pickle
import calendar
import seaborn as sns
from matplotlib import dates # used in function plot_signal_with_action

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
from sklearn.linear_model import LinearRegression

# set ggplot style
plt.style.use('ggplot')
pd.options.mode.chained_assignment = None

def plot_in_3d(df_sample_period, concerned_value = 'H1', asset_name=None, vertical_scale=9, address_to_savefig=None, year=None):
    # create a pivot table for plotting figures
    df_sample_period_pivot = df_sample_period.pivot(
        index='time_of_day', columns='day_of_year')[concerned_value]
    
    reference_value_for_z_axis = max(df_sample_period[concerned_value].quantile(.89) * vertical_scale, 5)
    
    if not asset_name:
        asset_name = concerned_value

    fig = plt.figure(figsize=(9, 6))
    ax = fig.gca(projection='3d')

    z_label_name = concerned_value

    considered_number_of_days = len(df_sample_period_pivot.columns)
    xs = np.arange(len(df_sample_period_pivot.index))
    zs = np.arange(considered_number_of_days)
    value_array = np.transpose(np.array(df_sample_period_pivot))
    verts = []

    for z in zs:
        ys = value_array[z]
        ys[0], ys[-1] = 0, 0
        verts.append(list(zip(xs, ys)))

    palette_1 = sns.color_palette("husl", considered_number_of_days)
    poly = PolyCollection(verts, edgecolors='black', facecolors=palette_1)

    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_title(asset_name +
                 ' - daily consumption 3D plot \n',
                 pad=40)
    ax.set_xlabel('Time')
    ax.set_xlim3d(np.min(xs) - 10, np.max(xs) + 10)
    ax.set_ylabel('Day of Year 2021')
    ax.set_ylim3d(0, considered_number_of_days)
    ax.set_zlabel(z_label_name)
    ax.set_zlim3d(0, reference_value_for_z_axis)

    time_interval_mins = np.max(xs) - np.min(xs) + 1
    number_of_ticks = 6
    time_tick_interval_mins = int(time_interval_mins / number_of_ticks)

    time_range = xs[0::time_tick_interval_mins]
    ax.set_xticks(time_range)
    time_list = [str(x) for x in df_sample_period_pivot.index[0::time_tick_interval_mins]]
    ax.set_xticklabels(time_list) 

    date_tick_interval_days = 7
    date_range = zs[0::date_tick_interval_days]
    ax.set_yticks(date_range)
    date_list = [str(x) for x in df_sample_period_pivot.columns[0::date_tick_interval_days]]
    ax.set_yticklabels(date_list) 
    # ax.view_init(elev=view_init_elev, 
    #              azim=view_init_azim)
    plt.tight_layout() # make room for the xlabel
    
    if address_to_savefig:
        plt.savefig(address_to_savefig + '/' + asset_name + ' - ' + '3D' + ' - ' + concerned_value)



def plot_in_heatmap(df_sample_period, concerned_value = 'H1', asset_name=None, max_current=None, min_current=None, year=None, address_to_savefig=None):
    # create a pivot table for plotting figures
    df_sample_period_pivot = df_sample_period.pivot(
        index='time_of_day', columns='day_of_year')[concerned_value]
    
    if not asset_name:
        asset_name = concerned_value
    
    if not max_current:
        max_current = max(df_sample_period[concerned_value].quantile(0.997), 1)
        
    if not min_current:
        min_current = df_sample_period[concerned_value].quantile(0.003)

    fig = plt.figure(figsize=(10,6))
    sns.heatmap(df_sample_period_pivot, cmap="Greens", 
                vmin=min_current,
                vmax=max_current,
                cbar_kws={'label': concerned_value})
    plt.title(asset_name +' - daily consumption heatmap \n', 
              pad=10)
    plt.xlabel('Day of Year 2021')
    plt.ylabel('Time of the day')
    plt.tight_layout() # make room for the xlabel
    
    if address_to_savefig:
        plt.savefig(address_to_savefig + '/' + asset_name + ' - ' + 'heatmap' + ' - ' +concerned_value)