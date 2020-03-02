#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

# Getting devices from recommendation list (feb 2019)

def get_recommended_list():
    import os
    os.chdir("C:/Users/pcle008/Box Sync/IOT Trial/DashApp/Data/")
    device_info = pd.read_csv('device_info.csv')
    recomms = pd.read_csv('recommendations_feb19.csv')
    recomms.rename(columns={'Equipment Name': 'Device'}, inplace=True)
    filt_list = pd.merge(device_info, recomms, how='inner', on=['Device'])

    df = pd.DataFrame(columns=['socket_ids', 'Device'])
    df['socket_ids'] = filt_list['socket_ids']
    df['Device'] = filt_list['Device']
    return df


def get_device_list():
    import os
    os.chdir("C:/Users/pcle008/Box Sync/IOT Trial/DashApp/Data/")
    device_info = pd.read_csv('device_info.csv')

    df = pd.DataFrame(columns=['socket_ids', 'Device'])
    df['socket_ids'] = device_info['socket_ids']
    df['Device'] = device_info['Device']

    return df
