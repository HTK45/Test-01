import streamlit as st      #version: 0.79.0
from bokeh.plotting import figure   #version: 2.2.2
import numpy as np
import pandas as pd
import openpyxl
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

import STEP10
import STEP20
import STEP30


def main():
    st.title('Data Analysis for Time series')
    st.write('■ 連続したステップの地面反力データから任意の変数の平均値を計算するツール')
    st.write('使い方: https://github.com/HTK45/TimeSeries-GRF の分析WEBアプリ説明書.pdfをチェック')

    st.sidebar.button('Reflesh')
    #動画アップロード
    st.sidebar.title('1. Select Excell File')
    st.sidebar.write('>>GRFファイルのアップロード')
    uploaded_file_01 = st.sidebar.file_uploader("データアップロード①", type='xlsx')
    # uploaded_file_01 = ('/Users/keiichirohata/Desktop/Python/Streamlit/TimeSeries_GRF/Sample_main.xlsx')
    st.sidebar.write('>>その他分析ファイルのアップロード')
    uploaded_file_02 = st.sidebar.file_uploader("データアップロード②", type='xlsx')
    # uploaded_file_02 = ('/Users/keiichirohata/Desktop/Python/Streamlit/TimeSeries_GRF/Sample_extra.xlsx')

    ### Setting ###
    # 変数の取得
    st.sidebar.title('  ')
    st.sidebar.title('1-2. Select Variables:File1')
    Var1 = st.sidebar.text_input('GRFxの変数名を入力', value='GRFx')
    Var1_Check = st.sidebar.checkbox('GRFxを平均値化する', value=False)
    Var2 = st.sidebar.text_input('GRFyの変数名を入力', value='GRFy')
    Var2_Check = st.sidebar.checkbox('GRFyを平均値化する', value=True)
    Var3 = st.sidebar.text_input('GRFzの変数名を入力', value='GRFz')
    Var3_Check = st.sidebar.checkbox('GRFzを平均値化する', value=True)
    Time1 = st.sidebar.text_input('ファイル①のTimeの変数名を入力', value='Time')
    st.sidebar.title('  ')
    st.sidebar.title('1-3. Select valiables:File2')
    ex_Var1 = st.sidebar.text_input('その他の変数名1を入力', value='DATA_A')
    ex_Var1_Check = st.sidebar.checkbox('変数1を平均値化する', value=True)

    ex_Time = st.sidebar.text_input('ファイル②のTimeの変数名を入力', value='Time')
    st.sidebar.title('  ')
    st.sidebar.title('2. Analysis Setting')
    # Filter_Set = st.sidebar.number_input(label='GRFz フィルター設定', value=20)
    # st.sidebar.write('4th Butterworth Filter: ', Filter_Set)

    #GRFz閾値設定の変数
    Thlethould_Set = st.sidebar.number_input(label='GRFz 閾値設定', value=20)
    # st.sidebar.write('設定された閾値: ', Thlethould_Set)
    Thlethould_Set2 = st.sidebar.number_input(label='GRFz 仮の閾値設定', value=80)
    # st.sidebar.write('設定された仮の閾値: ', Thlethould_Set2)
    th_add = st.sidebar.number_input(label='GRFz補間時の個数 (5~8)', value=5)
    # st.sidebar.write('設定された仮の閾値: ', Thlethould_Set2)

    #分析範囲
    AnalysisPeriod = st.sidebar.number_input(label='分析区間の範囲（n何歩目から）', value=2)
    st.sidebar.write('分析区間: ', AnalysisPeriod)

    #分析歩数
    STEP10_Check = st.checkbox('分析歩数 10歩', value=False)
    STEP20_Check = st.checkbox('分析歩数 20歩', value=False)
    STEP30_Check = st.checkbox('分析歩数 30歩', value=False)


    if STEP10_Check:
        STEP10.Sub10(uploaded_file_01, uploaded_file_02, Time1, Var1, Var2, Var3,Thlethould_Set, Thlethould_Set2, th_add, AnalysisPeriod, Var1_Check, Var2_Check, Var3_Check, ex_Var1, ex_Var1_Check, ex_Time)
    if STEP20_Check:
        STEP20.Sub20(uploaded_file_01, uploaded_file_02, Time1, Var1, Var2, Var3,Thlethould_Set, Thlethould_Set2, th_add, AnalysisPeriod, Var1_Check, Var2_Check, Var3_Check, ex_Var1, ex_Var1_Check, ex_Time)
    if STEP30_Check:
        STEP30.Sub30(uploaded_file_01, uploaded_file_02, Time1, Var1, Var2, Var3,Thlethould_Set, Thlethould_Set2, th_add, AnalysisPeriod, Var1_Check, Var2_Check, Var3_Check, ex_Var1, ex_Var1_Check, ex_Time)


if __name__ == '__main__':
    main()
