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

def enrich_time(df_resample):
    
    df_resample['time_of_day'] = df_resample['time'].dt.time
    df_resample['time_of_day_in_float'] = df_resample['time_of_day'].apply(lambda x: x.hour+x.minute/60+x.second/3600)
    df_resample['date'] = df_resample['time'].dt.date
    df_resample['quarter_&_hour_of_day_with_date'] = df_resample['time'].dt.round('5min')
    df_resample['quarter_&_hour_of_day'] = df_resample['quarter_&_hour_of_day_with_date'].dt.time
    df_resample['hour_of_day'] = df_resample['time'].dt.hour
    df_resample['date'] = df_resample['time'].dt.date
    df_resample['day_of_month'] = df_resample['time'].dt.day
    df_resample['day_of_year'] = df_resample['time'].dt.dayofyear
    df_resample['day_of_week'] = df_resample['time'].dt.weekday
    df_resample['day_of_week_name'] = df_resample['day_of_week'].apply(lambda x: str(calendar.day_name[x]))
    df_resample['day_of_week_abbr_name'] = df_resample['day_of_week'].apply(lambda x: str(calendar.day_abbr[x]))
    df_resample['month_year'] = df_resample['time'].dt.strftime('%b-%Y')
    
    return df_resample