import pandas as pd # Import pandas
pd.options.mode.chained_assignment = None

from dateutil.parser import parse
import matplotlib.pyplot as plt


def generate_legend_labels_for_piechart_with_triangle(df_asset_class_monthly_sum_others, # this dataframe is required to have asset class as index and have columns "sub_pct", "sum"
                                            sum_column = "sum",
                                            pct_column = "sub_pct",
                                        space_len_long = 5,
                                        space_len_short = 1,
                                        pct_len = 4,
                                        kwh_len = 8):

    labels = []

    label_space_long = "," + " "*space_len_long 
    label_space_short = "," + " "*space_len_short

    for index, item in df_asset_class_monthly_sum_others.iterrows():

        label_pct_str = str(round(abs(item[pct_column])*100))
        label_pct_pad = ' ' *int((pct_len - len(label_pct_str))*2) + " "*label_pct_str.count('.')
        

        label_kwh_str = f'{item[sum_column]/1000:1.1f} MWh'
        label_kwh_pad = ' ' *int((kwh_len - len(label_kwh_str))*2) 
        label_kwh = label_kwh_pad + label_kwh_str

        # print(f"item[{pct_column}]: ", item[pct_column])

        if item[pct_column] > 0: # abs(item["sub_pct"]) < 0.05: label_arrow_str = r'$\sim$' elif
            label_arrow_str = r'${\blacktriangle}$'

        else:
            label_arrow_str = r'$\:\!\triangledown\:\!$'
        
        label_arrow_pad = ' '
        label_arrow = label_arrow_pad + label_arrow_str

        label_index = index

        label = label_kwh + label_space_short + label_arrow+ " " +label_pct_str + r"%" + label_space_short + label_pct_pad + label_index

        labels.append(label)
        
    return labels


def piechart_comparison_design(df_asset_class_monthly_sum_others, 
                                sum_column = "sum",
                                pct_column = "sub_pct"):

    fig, ax = plt.subplots(1, 1, figsize=(9, 3.9))

    colors = ['#6DC2B3', '#FF836A', '#FED6D2', '#9F9D9C', '#B6E4E1', '#FEF8C8', '#CFCDCD', '#9DE7BE']
    other_colours = ['k', 'w']

    df_asset_class_monthly_sum_others[sum_column].plot.pie(ax=ax, autopct='%1.0f%%', colors=colors,
                                                      textprops={"color": other_colours[0], "fontsize": 13}, pctdistance=0.77,
                                                      wedgeprops={'linewidth': 1, "edgecolor": other_colours[0]}, labels=None)

    df_asset_class_monthly_sum_others[sum_column].plot.pie(ax=ax, colors="k", radius=0.53,
                                                        wedgeprops={'linewidth': 1.5, "edgecolor": other_colours[0]}, labels=None)

    ax.legend(labels=generate_legend_labels_for_piechart_with_triangle(df_asset_class_monthly_sum_others, sum_column=sum_column, pct_column=pct_column),
              loc="center right",  edgecolor=other_colours[1], facecolor='white',
              bbox_to_anchor=(1.27, 0, 1, 1), fontsize=13,  ncol=1, handleheight=1.2, labelspacing=0.6, title=None)

   
    ax.set_ylabel("")

    my_circle = plt.Circle((0, 0), .5, color=other_colours[1], edgecolor=other_colours[0], linewidth=4)
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # sum_cur = df_asset_class_monthly_sum_others.sum()["sum"]/1000
    # sum_pre = df_asset_class_monthly_sum_others.sum()["sum_pre"]/1000
    # sub_pct = ((sum_cur - sum_pre)/sum_pre) * 100

    # text_kwargs = dict(ha='center', va='center', fontsize=14, color='k')
    fig.tight_layout(pad=1.2, rect=[-0.05,0.1,0.72, 0.95])
