import os, glob, shutil
import time as t
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def format(value):
    return '%.2f' % value


def stock_market_analysis():
    data_path = r'C:\Users\dgato\Desktop\stock market\sp500_1887-2018_mothly.csv'

    all_data = pd.read_csv(data_path)
    data = all_data.iloc[:,0:2]
    time = np.array(data.iloc[:,0])
    snp = np.array(data.iloc[:,1])

    from_time = 12*57+3 ## caculate over 100 years
    time_period = 12 ## year
    mean_time_period = 10
    window = time_period*mean_time_period ## ten years

    snp = snp[from_time:]
    snp_dif_percent = np.zeros((len(snp)-time_period,1))
    for d in range(len(snp)-time_period):
        snp_dif_percent[d] = 100*(snp[d+time_period]-snp[d])/snp[d]

    snp_ten_year_means = np.zeros((len(snp_dif_percent)-window,1))
    zero_line = np.copy(snp_ten_year_means)
    for i in range(len(snp_dif_percent)-window):
        snp_ten_year_means[i] = np.mean(snp_dif_percent[i:i+window])


    print('minimal average over window is: ' + format(np.min(snp_ten_year_means)) + '%')
    print('maximal average over window is: ' + format(np.max(snp_ten_year_means)) + '%')
    print('mean of average over window is: ' + format(np.mean(snp_ten_year_means)) + '%')
    print('percent under 0%: ' + format(100*np.mean(snp_ten_year_means<0)) + '%; under 4%: '
          + format(100*np.mean(snp_ten_year_means<4)) + '%')
    print('percent over 7%: ' + format(100*np.mean(snp_ten_year_means>7)) + '%; over 10%: '
          + format(100*np.mean(snp_ten_year_means>10)) + '%')

    time_years = np.copy(time[from_time:])
    for idx, t_y in enumerate(time_years):
        time_years[idx] = t_y.split('/')[-1]

    fig, ax = plt.subplots(2,1, figsize=(19,14))
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    ax[0].plot(snp)
    ax[0].set_xlim([0, len(snp)]), ax[0].set_ylim([np.min(snp),np.max(snp)+20])
    ax[0].set_xticks(np.arange(0,len(snp),120)), ax[0].set_xticklabels(time_years[::120])

    ax[1].plot(snp_ten_year_means)
    ax[1].plot(zero_line, label='0%'), ax[1].plot(zero_line+4, label='4%')
    ax[1].plot(zero_line+7, label='7%'), ax[1].plot(zero_line+10, label='10%')
    ax[1].legend()
    ax[1].set_xlim([0, len(snp)]), ax[1].set_ylim([np.min(snp_ten_year_means)-0.2,np.max(snp_ten_year_means)+0.2])
    ax[1].set_xticks(np.arange(0,len(snp),120)), ax[1].set_xticklabels(time_years[::120])

    ax[0].set_title('S&P from ' + time[from_time] + ' to ' + time[-1], fontsize=15),
    ax[1].set_title('S&P ten year means', fontsize=15)
    plt.tight_layout(h_pad=2.5)
    plt.show()


def main():
    stock_market_analysis()


if __name__ == '__main__':
    main()

