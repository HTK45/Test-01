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


def Sub10(uploaded_file_01, uploaded_file_02, Time1, Var1, Var2, Var3,Thlethould_Set, Thlethould_Set2, th_add, AnalysisPeriod, Var1_Check, Var2_Check, Var3_Check, ex_Var1, ex_Var1_Check, ex_Time):
    file = pd.ExcelFile(uploaded_file_01)
    df = pd.read_excel(file, sheet_name = 0)
    Time = df[Time1]
    GRFx = df[Var1]
    GRFy = df[Var2]
    GRFz = df[Var3]
    """
    #     #
    #     ## ▶︎ 1. ファイル1の結果
    #     ## 1-1: データ参照
    #
    """
    st.title('')
    st.title('▶︎ 1. ファイル1の結果')


    ## STEP 1: 閾値設定 ##___________________________________________________________________________________________________________________________________________________________________________
    ## GRFzの値の閾値(thleshould 1)を設定し一歩ごとのGRFzデータを取得する ##
    thlethould1 = Thlethould_Set    # 分析用の閾値
    thlethould2 = Thlethould_Set2   # 外れ値の除去用

    ## STEP 2: 閾値の範囲を取得する ##_________________________________________________________________________________________________________________________________________________________________
    ## thlethoud 2の閾値を基準にGRFzデータを間引く
    th = np.append(np.diff(GRFz < thlethould2),0)
    th_point = pd.DataFrame(th)
    setframe = range(GRFz.size)
    df.insert(0,'SetFrame',setframe)
    Frame = df['SetFrame']
    df.insert(2,'Thlethould_Point',th_point)
    th_Time = df.query('Thlethould_Point == 1')['Time'] #dfから任意の値の場所の変数の値を取得
    th_Frame = df.query('Thlethould_Point == 1')['SetFrame']

    # GRFzで一歩ごとに区切る関数
    def GRFz_n_Func(InitialContactFrame, ToeOffFrame):
        Time_n = []
        Frame_n =[]
        GRFz_n = []
        GRFy_n = []
        GRFx_n = []
        for i in range(th_Frame.iloc[InitialContactFrame],th_Frame.iloc[ToeOffFrame]):
            T = Time[i]
            F = Frame[i]
            Gz = GRFz[i]
            Gy = GRFy[i]
            Gx = GRFx[i]
            Time_n.append(T)
            Frame_n.append(F)
            GRFz_n.append(Gz)
            GRFy_n.append(Gy)
            GRFx_n.append(Gx)

        Time_n.pop(0)
        Frame_n.pop(0)
        GRFz_n.pop(0)
        GRFy_n.pop(0)
        GRFx_n.pop(0)

        ## STEP 2-2: 閾値（thlethould 1）を基準にしたGRFzデータを取得
        ## thlethould 2で間引いたデータ（GRFz_n）の前後の閾値以上の値を追加する
        for i in range(1,th_add,1):
            # データ前半に追加
            T1 = Time[Frame_n[0]-i]
            F1 = Frame[Frame_n[0]-i]
            Gz1 = GRFz[Frame_n[0]-i]
            Gy1 = GRFy[Frame_n[0]-i]
            Gx1 = GRFx[Frame_n[0]-i]
            Time_n.insert(0,T1)
            Frame_n.insert(0,F1)
            GRFz_n.insert(0, Gz1)
            GRFy_n.insert(0, Gy1)
            GRFx_n.insert(0, Gx1)
            # データ後半に追加
            T2 = Time[Frame_n[-1]+i]
            F2 = Frame[Frame_n[-1]+i]
            Gz2 = GRFz[Frame_n[-1]+i]
            Gy2 = GRFy[Frame_n[-1]+i]
            Gx2 = GRFy[Frame_n[-1]+i]
            Time_n.append(T2)
            Frame_n.append(F2)
            GRFz_n.append(Gz2)
            GRFy_n.append(Gy2)
            GRFx_n.append(Gy2)

        RESULTS = pd.DataFrame(list(zip(Frame_n,Time_n,GRFx_n,GRFy_n,GRFz_n)), columns = ['Frame','Time','GRFx','GRFy','GRFz'])
        indexNames = RESULTS[ (RESULTS['GRFz'] < thlethould1)].index
        RESULTS.drop(indexNames , inplace=True) #閾値以下を削除
        return RESULTS

    n = AnalysisPeriod-1

    ## 分析データ ##___________________________________________________________________________________________________________________________________________________________________________
    #　GRFzで区切られたデータ
    Step1 = GRFz_n_Func(0+n,1+n); Step2 = GRFz_n_Func(2+n,3+n); Step3 = GRFz_n_Func(4+n,5+n); Step4 = GRFz_n_Func(6+n,7+n); Step5 = GRFz_n_Func(8+n,9+n)
    Step6 = GRFz_n_Func(10+n,11+n); Step7 = GRFz_n_Func(12+n,13+n); Step8 = GRFz_n_Func(14+n,15+n); Step9 = GRFz_n_Func(16+n,17+n); Step10 = GRFz_n_Func(18+n,19+n)
    Step11 = GRFz_n_Func(20+n,21+n); Step12 = GRFz_n_Func(22+n,23+n); Step13 = GRFz_n_Func(24+n,25+n); Step14 = GRFz_n_Func(26+n,27+n); Step15 = GRFz_n_Func(28+n,29+n)
    Step16 = GRFz_n_Func(30+n,31+n); Step17 = GRFz_n_Func(32+n,33+n); Step18 = GRFz_n_Func(34+n,35+n); Step19 = GRFz_n_Func(36+n,37+n); Step20 = GRFz_n_Func(38+n,39+n)
    Step21 = GRFz_n_Func(40+n,41+n); Step22 = GRFz_n_Func(42+n,43+n); Step23 = GRFz_n_Func(44+n,45+n); Step24 = GRFz_n_Func(46+n,47+n); Step25 = GRFz_n_Func(48+n,49+n); Step26 = GRFz_n_Func(50+n,51+n);

    Time1 = Step1['Time']; Time2 = Step2['Time']; Time3 = Step3['Time']; Time4 = Step4['Time']; Time5 = Step5['Time']; Time6 = Step6['Time']; Time7 = Step7['Time']; Time8 = Step8['Time']; Time9 = Step9['Time']; Time10 = Step10['Time']
    Time11 = Step11['Time']; Time12 = Step12['Time']; Time13 = Step13['Time']; Time14 = Step14['Time']; Time15 = Step15['Time']; Time16 = Step16['Time']; Time17 = Step17['Time']; Time18 = Step18['Time']; Time19 = Step19['Time']; Time20 = Step20['Time']; Time21 = Step21['Time']

    GRFx1 = Step1['GRFx']; GRFx2 = Step2['GRFx']; GRFx3 = Step3['GRFx']; GRFx4 = Step4['GRFx']; GRFx5 = Step5['GRFx']; GRFx6 = Step6['GRFx']; GRFx7 = Step7['GRFx']; GRFx8 = Step8['GRFx']; GRFx9 = Step9['GRFx']; GRFx10 = Step10['GRFx']
    GRFx11 = Step11['GRFx']; GRFx12 = Step12['GRFx']; GRFx13 = Step13['GRFx']; GRFx14 = Step14['GRFx']; GRFx15 = Step15['GRFx']; GRFx16 = Step16['GRFx']; GRFx17 = Step17['GRFx']; GRFx18 = Step18['GRFx']; GRFx19 = Step19['GRFx']; GRFx20 = Step20['GRFx']

    GRFy1 = Step1['GRFy']; GRFy2 = Step2['GRFy']; GRFy3 = Step3['GRFy']; GRFy4 = Step4['GRFy']; GRFy5 = Step5['GRFy']; GRFy6 = Step6['GRFy']; GRFy7 = Step7['GRFy']; GRFy8 = Step8['GRFy']; GRFy9 = Step9['GRFy']; GRFy10 = Step10['GRFy']
    GRFy11 = Step11['GRFy']; GRFy12 = Step12['GRFy']; GRFy13 = Step13['GRFy']; GRFy14 = Step14['GRFy']; GRFy15 = Step15['GRFy']; GRFy16 = Step16['GRFy']; GRFy17 = Step17['GRFy']; GRFy18 = Step18['GRFy']; GRFy19 = Step19['GRFy']; GRFy20 = Step20['GRFy']

    GRFz1 = Step1['GRFz']; GRFz2 = Step2['GRFz']; GRFz3 = Step3['GRFz']; GRFz4 = Step4['GRFz']; GRFz5 = Step5['GRFz']; GRFz6 = Step6['GRFz']; GRFz7 = Step7['GRFz']; GRFz8 = Step8['GRFz']; GRFz9 = Step9['GRFz']; GRFz10 = Step10['GRFz']
    GRFz11 = Step11['GRFz']; GRFz12 = Step12['GRFz']; GRFz13 = Step13['GRFz']; GRFz14 = Step14['GRFz']; GRFz15 = Step15['GRFz']; GRFz16 = Step16['GRFz']; GRFz17 = Step17['GRFz']; GRFz18 = Step18['GRFz']; GRFz19 = Step19['GRFz']; GRFz20 = Step20['GRFz']

    ## 分析データ: Spline ##___________________________________________________________________________________________________________________________________________________________________________
    def Spline_Func(s_df):
        Num = s_df.count()
        x = np.arange(Num)
        y = s_df.dropna().values
        f = interp1d(x, y, kind='cubic')
        k = np.linspace(0,Num-1, num=101)
        spline = pd.DataFrame(f(k))
        return spline
    #GRFx
    GRFx_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
    GRFx_Spline['Step1']=Spline_Func(GRFx1); GRFx_Spline['Step2']=Spline_Func(GRFx2); GRFx_Spline['Step3']=Spline_Func(GRFx3); GRFx_Spline['Step4']=Spline_Func(GRFx4); GRFx_Spline['Step5']=Spline_Func(GRFx5);
    GRFx_Spline['Step6']=Spline_Func(GRFx6); GRFx_Spline['Step7']=Spline_Func(GRFx7); GRFx_Spline['Step8']=Spline_Func(GRFx8); GRFx_Spline['Step9']=Spline_Func(GRFx9); GRFx_Spline['Step10']=Spline_Func(GRFx10);
    GRFx_Spline['Step11']=Spline_Func(GRFx11); GRFx_Spline['Step12']=Spline_Func(GRFx12); GRFx_Spline['Step13']=Spline_Func(GRFx13); GRFx_Spline['Step14']=Spline_Func(GRFx14); GRFx_Spline['Step15']=Spline_Func(GRFx15);
    GRFx_Spline['Step16']=Spline_Func(GRFx16); GRFx_Spline['Step17']=Spline_Func(GRFx17); GRFx_Spline['Step18']=Spline_Func(GRFx18); GRFx_Spline['Step19']=Spline_Func(GRFx19); GRFx_Spline['Step20']=Spline_Func(GRFx20);

    #GRFy
    GRFy_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
    GRFy_Spline['Step1']=Spline_Func(GRFy1); GRFy_Spline['Step2']=Spline_Func(GRFy2); GRFy_Spline['Step3']=Spline_Func(GRFy3); GRFy_Spline['Step4']=Spline_Func(GRFy4); GRFy_Spline['Step5']=Spline_Func(GRFy5);
    GRFy_Spline['Step6']=Spline_Func(GRFy6); GRFy_Spline['Step7']=Spline_Func(GRFy7); GRFy_Spline['Step8']=Spline_Func(GRFy8); GRFy_Spline['Step9']=Spline_Func(GRFy9); GRFy_Spline['Step10']=Spline_Func(GRFy10);
    GRFy_Spline['Step11']=Spline_Func(GRFy11); GRFy_Spline['Step12']=Spline_Func(GRFy12); GRFy_Spline['Step13']=Spline_Func(GRFy13); GRFy_Spline['Step14']=Spline_Func(GRFy14); GRFy_Spline['Step15']=Spline_Func(GRFy15);
    GRFy_Spline['Step16']=Spline_Func(GRFy16); GRFy_Spline['Step17']=Spline_Func(GRFy17); GRFy_Spline['Step18']=Spline_Func(GRFy18); GRFy_Spline['Step19']=Spline_Func(GRFy19); GRFy_Spline['Step20']=Spline_Func(GRFy20);

    #GRFz
    GRFz_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
    GRFz_Spline['Step1']=Spline_Func(GRFz1); GRFz_Spline['Step2']=Spline_Func(GRFz2); GRFz_Spline['Step3']=Spline_Func(GRFz3); GRFz_Spline['Step4']=Spline_Func(GRFz4); GRFz_Spline['Step5']=Spline_Func(GRFz5);
    GRFz_Spline['Step6']=Spline_Func(GRFz6); GRFz_Spline['Step7']=Spline_Func(GRFz7); GRFz_Spline['Step8']=Spline_Func(GRFz8); GRFz_Spline['Step9']=Spline_Func(GRFz9); GRFz_Spline['Step10']=Spline_Func(GRFz10);
    GRFz_Spline['Step11']=Spline_Func(GRFz11); GRFz_Spline['Step12']=Spline_Func(GRFz12); GRFz_Spline['Step13']=Spline_Func(GRFz13); GRFz_Spline['Step14']=Spline_Func(GRFz14); GRFz_Spline['Step15']=Spline_Func(GRFz15);
    GRFz_Spline['Step16']=Spline_Func(GRFz16); GRFz_Spline['Step17']=Spline_Func(GRFz17); GRFz_Spline['Step18']=Spline_Func(GRFz18); GRFz_Spline['Step19']=Spline_Func(GRFz19); GRFz_Spline['Step20']=Spline_Func(GRFz20);


    ####__________________________________________________________________________________________________________________________________________________________________________________________
    ## Export: DataFrame, Figure ##___________________________________________________________________________________________________________________________________________________________________________
    st.title('全てのデータ')
    # Output
    # Table
    st.write('> データフレーム（全て）')
    st.dataframe(df, width=1000, height=150)
    # Figure 1: ALL data
    # Figure setting
    st.write('> インポート: Figure GRFz')
    GRFz_fig = figure(title='GRFz time series', x_axis_label='Time (s)', y_axis_label='GRFz (N)', frame_height=200)
    LC_ALL = [70, 86, 113]
    LC_th = 'red'
    LW = 1.3
    # GRFz ALL
    GRFz_fig.line(Time,GRFz, line_color=LC_ALL)
    # GRFz each steps
    GRFz_fig.line(Time1, GRFz1,line_color=LC_th, line_width = LW); GRFz_fig.line(Time2, GRFz2,line_color=LC_th, line_width = LW); GRFz_fig.line(Time3, GRFz3,line_color=LC_th, line_width = LW); GRFz_fig.line(Time4, GRFz4,line_color=LC_th, line_width = LW); GRFz_fig.line(Time5, GRFz5,line_color=LC_th, line_width = LW)
    GRFz_fig.line(Time6, GRFz6,line_color=LC_th, line_width = LW); GRFz_fig.line(Time7, GRFz7,line_color=LC_th, line_width = LW); GRFz_fig.line(Time8, GRFz8,line_color=LC_th, line_width = LW); GRFz_fig.line(Time9, GRFz9,line_color=LC_th, line_width = LW); GRFz_fig.line(Time10, GRFz10,line_color=LC_th, line_width = LW)
    GRFz_fig.line(Time11, GRFz11,line_color=LC_th, line_width = LW); GRFz_fig.line(Time12, GRFz12,line_color=LC_th, line_width = LW); GRFz_fig.line(Time13, GRFz13,line_color=LC_th, line_width = LW); GRFz_fig.line(Time14, GRFz14,line_color=LC_th, line_width = LW); GRFz_fig.line(Time15, GRFz15,line_color=LC_th, line_width = LW)
    GRFz_fig.line(Time16, GRFz16,line_color=LC_th, line_width = LW); GRFz_fig.line(Time17, GRFz17,line_color=LC_th, line_width = LW); GRFz_fig.line(Time18, GRFz18,line_color=LC_th, line_width = LW); GRFz_fig.line(Time19, GRFz19,line_color=LC_th, line_width = LW); GRFz_fig.line(Time20, GRFz20,line_color=LC_th, line_width = LW)

    st.write('> 分析区間のデータ: 分析データ（赤ライン）, すべてのデータ（黒ライン）')
    st.bokeh_chart(GRFz_fig, use_container_width=True)


    SideButton2 = st.button('分析区間のデータ')
    if SideButton2:
        # DataFrame: Each data
        df1 = pd.DataFrame(range(100),columns=['Frame']);
        df1['Time1']=Time1; df1['Time2']=Time2; df1['Time3']=Time3; df1['Time4']=Time4; df1['Time5']=Time5; df1['Time6']=Time6; df1['Time7']=Time7; df1['Time8']=Time8; df1['Time9']=Time9; df1['Time10']=Time10
        df1['Time11']=Time11; df1['Time12']=Time12; df1['Time13']=Time13; df1['Time14']=Time14; df1['Time15']=Time15; df1['Time16']=Time16; df1['Time17']=Time17; df1['Time18']=Time18; df1['Time19']=Time19; df1['Time20']=Time20

        df1['GRFz1']=GRFz1; df1['GRFz2']=GRFz2; df1['GRFz3']=GRFz3; df1['GRFz4']=GRFz4; df1['GRFz5']=GRFz5; df1['GRFz6']=GRFz6; df1['GRFz7']=GRFz7; df1['GRFz8']=GRFz8; df1['GRFz9']=GRFz9; df1['GRFz10']=GRFz10
        df1['GRFz11']=GRFz11; df1['GRFz12']=GRFz12; df1['GRFz13']=GRFz13; df1['GRFz14']=GRFz14; df1['GRFz15']=GRFz15; df1['GRFz16']=GRFz16; df1['GRFz17']=GRFz17; df1['GRFz18']=GRFz18; df1['GRFz19']=GRFz19; df1['GRFz20']=GRFz20

        df1['GRFy1']=GRFy1; df1['GRFy2']=GRFy2; df1['GRFy3']=GRFy3; df1['GRFy4']=GRFy4; df1['GRFy5']=GRFy5; df1['GRFy6']=GRFy6; df1['GRFy7']=GRFy7; df1['GRFy8']=GRFy8; df1['GRFy9']=GRFy9; df1['GRFy10']=GRFy10
        df1['GRFy11']=GRFy11; df1['GRFy12']=GRFy12; df1['GRFy13']=GRFy13; df1['GRFy14']=GRFy14; df1['GRFy15']=GRFy15; df1['GRFy16']=GRFy16; df1['GRFy17']=GRFy17; df1['GRFy18']=GRFy18; df1['GRFy19']=GRFy19; df1['GRFy20']=GRFy20


        # Table output
        st.write('> データフレーム(分析ステップ)')
        st.dataframe(df1, width=1000, height=150)

        # Copy?
        copy_button1 = Button(label="Copy: All data")
        copy_button1.js_on_event("button_click", CustomJS(args=dict(df=df1.to_csv(sep='\t')), code="""
            navigator.clipboard.writeText(df);
            """))
        no_event = streamlit_bokeh_events(
                copy_button1,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)

        # Figure 2: Each data
        # Figure setting
        GRF_fig = figure(title='GRFz time series', x_axis_label='Time (s)', y_axis_label='GRFz (N)', frame_height=200)
        LC_GRFz = 'red'
        LC_GRFy = [25, 40, 64]
        LW = 1.3
        # GRFz each steps
        GRF_fig.line(Time1, GRFz1,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time2, GRFz2,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time3, GRFz3,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time4, GRFz4,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time5, GRFz5,line_color=LC_GRFz, line_width = LW)
        GRF_fig.line(Time6, GRFz6,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time7, GRFz7,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time8, GRFz8,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time9, GRFz9,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time10, GRFz10,line_color=LC_GRFz, line_width = LW)
        GRF_fig.line(Time11, GRFz11,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time12, GRFz12,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time13, GRFz13,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time14, GRFz14,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time15, GRFz15,line_color=LC_GRFz, line_width = LW)
        GRF_fig.line(Time16, GRFz16,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time17, GRFz17,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time18, GRFz18,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time19, GRFz19,line_color=LC_GRFz, line_width = LW); GRF_fig.line(Time20, GRFz20,line_color=LC_GRFz, line_width = LW)

        # GRFy each steps
        GRF_fig.line(Time1, GRFy1,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time2, GRFy2,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time3, GRFy3,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time4, GRFy4,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time5, GRFy5,line_color=LC_GRFy, line_width = LW)
        GRF_fig.line(Time6, GRFy6,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time7, GRFy7,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time8, GRFy8,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time9, GRFy9,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time10, GRFy10,line_color=LC_GRFy, line_width = LW)
        GRF_fig.line(Time11, GRFy11,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time12, GRFy12,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time13, GRFy13,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time14, GRFy14,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time15, GRFy15,line_color=LC_GRFy, line_width = LW)
        GRF_fig.line(Time16, GRFy16,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time17, GRFy17,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time18, GRFy18,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time19, GRFy19,line_color=LC_GRFy, line_width = LW); GRF_fig.line(Time20, GRFy20,line_color=LC_GRFy, line_width = LW)

        st.write('> 分析区間のデータ: GRFz（赤ライン）, GRFy（黒ライン）')
        st.bokeh_chart(GRF_fig, use_container_width=True)

    st.title('')
    st.title('平均値')
    """
    #
    ## 1-2: 平均値
    """
    st.write('GRFx')
    if Var1_Check:  #GRFx
        SideButton_Fx_R = st.button('GRFx 1st-steps')
        SideButton_Fx_L = st.button('GRFx 2nd-steps')
        if SideButton_Fx_R:
            st.write('GRFx 1st-steps')
            # DataFrame: Each data
            GRFx_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFx_Spline['Step1']=Spline_Func(GRFx1);    GRFx_Spline['Step3']=Spline_Func(GRFx3);    GRFx_Spline['Step5']=Spline_Func(GRFx5);    GRFx_Spline['Step7']=Spline_Func(GRFx7);    GRFx_Spline['Step9']=Spline_Func(GRFx9);
            GRFx_Spline['Step11']=Spline_Func(GRFx11);  GRFx_Spline['Step13']=Spline_Func(GRFx13);  GRFx_Spline['Step15']=Spline_Func(GRFx15);  GRFx_Spline['Step17']=Spline_Func(GRFx17);  GRFx_Spline['Step19']=Spline_Func(GRFx19);

            # データフレーム
            st.dataframe(GRFx_Spline, width=1000, height=150)
            # Copy?
            copy_button_GRFx_R = Button(label="Copy: GRFx")
            copy_button_GRFx_R.js_on_event("button_click", CustomJS(args=dict(df=GRFx_Spline.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
            no_event = streamlit_bokeh_events(
                copy_button_GRFx_R,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)
            # # グラフ
            GRFx_Spline2 = GRFx_Spline.drop(columns='Frame')
            st.line_chart(GRFx_Spline2)

        if SideButton_Fx_L:
            st.write('GRFx 2nd-steps')
            # DataFrame: Each data
            GRFx_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFx_Spline['Step2']=Spline_Func(GRFx2);    GRFx_Spline['Step4']=Spline_Func(GRFx4);    GRFx_Spline['Step6']=Spline_Func(GRFx6);     GRFx_Spline['Step8']=Spline_Func(GRFx8);   GRFx_Spline['Step10']=Spline_Func(GRFx10);
            GRFx_Spline['Step12']=Spline_Func(GRFx12);  GRFx_Spline['Step14']=Spline_Func(GRFx14);  GRFx_Spline['Step16']=Spline_Func(GRFx16);   GRFx_Spline['Step18']=Spline_Func(GRFx18); GRFx_Spline['Step20']=Spline_Func(GRFx20);

            # データフレーム
            st.dataframe(GRFx_Spline, width=1000, height=150)
            # Copy?
            copy_button_GRFx_L = Button(label="Copy: GRFx")
            copy_button_GRFx_L.js_on_event("button_click", CustomJS(args=dict(df=GRFx_Spline.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
            no_event = streamlit_bokeh_events(
                copy_button_GRFx_L,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)
            # # グラフ
            GRFx_Spline2 = GRFx_Spline.drop(columns='Frame')
            st.line_chart(GRFx_Spline2)

    st.write('GRFy')
    if Var2_Check:  #GRFy
        SideButton_Fy_R = st.button('GRFy 1st-steps')
        SideButton_Fy_L = st.button('GRFy 2nd-steps')
        if SideButton_Fy_R:
            st.write('GRFy 1st-steps')
            # DataFrame: Each data
            GRFy_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFy_Spline['Step1']=Spline_Func(GRFy1);    GRFy_Spline['Step3']=Spline_Func(GRFy3);    GRFy_Spline['Step5']=Spline_Func(GRFy5);    GRFy_Spline['Step7']=Spline_Func(GRFy7);    GRFy_Spline['Step9']=Spline_Func(GRFy9);
            GRFy_Spline['Step11']=Spline_Func(GRFy11);  GRFy_Spline['Step13']=Spline_Func(GRFy13);  GRFy_Spline['Step15']=Spline_Func(GRFy15);  GRFy_Spline['Step17']=Spline_Func(GRFy17);  GRFy_Spline['Step19']=Spline_Func(GRFy19);

            # データフレーム
            st.dataframe(GRFy_Spline, width=1000, height=150)
            # Copy?
            copy_button1_1 = Button(label="Copy: GRFy")
            copy_button1_1.js_on_event("button_click", CustomJS(args=dict(df=GRFy_Spline.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
            no_event = streamlit_bokeh_events(
                copy_button1_1,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)
            # グラフ
            GRFy_Spline2 = GRFy_Spline.drop(columns='Frame')
            st.line_chart(GRFy_Spline2)

        if SideButton_Fy_L:
            st.write('GRFy 2nd-steps')
            # DataFrame: Each data
            GRFy_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFy_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFy_Spline['Step2']=Spline_Func(GRFy2);    GRFy_Spline['Step4']=Spline_Func(GRFy4);    GRFy_Spline['Step6']=Spline_Func(GRFy6);     GRFy_Spline['Step8']=Spline_Func(GRFy8);   GRFy_Spline['Step10']=Spline_Func(GRFy10);
            GRFy_Spline['Step12']=Spline_Func(GRFy12);  GRFy_Spline['Step14']=Spline_Func(GRFy14);  GRFy_Spline['Step16']=Spline_Func(GRFy16);   GRFy_Spline['Step18']=Spline_Func(GRFy18); GRFy_Spline['Step20']=Spline_Func(GRFy20);

            # データフレーム
            st.dataframe(GRFy_Spline, width=1000, height=150)
            # Copy?
            copy_button1_1 = Button(label="Copy: GRFy")
            copy_button1_1.js_on_event("button_click", CustomJS(args=dict(df=GRFy_Spline.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
            no_event = streamlit_bokeh_events(
                copy_button1_1,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)
            # グラフ
            GRFy_Spline2 = GRFy_Spline.drop(columns='Frame')
            st.line_chart(GRFy_Spline2)

    st.write('GRFz')
    if Var3_Check:  #GRFz
        SideButton_Fz_R = st.button('GRFz 1st-steps')
        SideButton_Fz_L = st.button('GRFz 2nd-steps')
        if SideButton_Fz_R:
            st.write('GRFz 1st-steps')
            # DataFrame: Each data
            GRFz_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFz_Spline['Step1']=Spline_Func(GRFz1);    GRFz_Spline['Step3']=Spline_Func(GRFz3);    GRFz_Spline['Step5']=Spline_Func(GRFz5);    GRFz_Spline['Step7']=Spline_Func(GRFz7);    GRFz_Spline['Step9']=Spline_Func(GRFz9);
            GRFz_Spline['Step11']=Spline_Func(GRFz11);  GRFz_Spline['Step13']=Spline_Func(GRFz13);  GRFz_Spline['Step15']=Spline_Func(GRFz15);  GRFz_Spline['Step17']=Spline_Func(GRFz17);  GRFz_Spline['Step19']=Spline_Func(GRFz19);

            # データフレーム
            st.dataframe(GRFz_Spline, width=1000, height=150)
            # Copy?
            copy_button1_2 = Button(label="Copy: GRFz")
            copy_button1_2.js_on_event("button_click", CustomJS(args=dict(df=GRFz_Spline.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
            no_event = streamlit_bokeh_events(
                copy_button1_2,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)
            # グラフ
            GRFz_Spline2 = GRFz_Spline.drop(columns='Frame')
            st.line_chart(GRFz_Spline2)

        if SideButton_Fz_L:
            st.write('GRFz 2nd-steps')
            # DataFrame: Each data
            GRFz_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
            GRFz_Spline['Step2']=Spline_Func(GRFz2);    GRFz_Spline['Step4']=Spline_Func(GRFz4);    GRFz_Spline['Step6']=Spline_Func(GRFz6);     GRFz_Spline['Step8']=Spline_Func(GRFz8);   GRFz_Spline['Step10']=Spline_Func(GRFz10);
            GRFz_Spline['Step12']=Spline_Func(GRFz12);  GRFz_Spline['Step14']=Spline_Func(GRFz14);  GRFz_Spline['Step16']=Spline_Func(GRFz16);   GRFz_Spline['Step18']=Spline_Func(GRFz18); GRFz_Spline['Step20']=Spline_Func(GRFz20);

            # データフレーム
            st.dataframe(GRFz_Spline, width=1000, height=150)
            # Copy?
            copy_button_GRFz_L = Button(label="Copy: GRFz")
            copy_button_GRFz_L.js_on_event("button_click", CustomJS(args=dict(df=GRFz_Spline.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
            no_event = streamlit_bokeh_events(
                copy_button_GRFz_L,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)
            # # グラフ
            GRFz_Spline2 = GRFz_Spline.drop(columns='Frame')
            st.line_chart(GRFz_Spline2)


#_____________________________________________________________________________________________________________________________________________________________________________________________
    """
    #
    ## 1-3: 接地時間・滞空時間
    """
    st.title('')
    st.title('1-3: 接地時間・滞空時間')
    SideButton_PhaseTime_R = st.button('接地・滞空時間 1st-steps')
    SideButton_PhaseTime_L = st.button('接地・滞空時間 2nd-steps')


    if SideButton_PhaseTime_R:
        def PhaseTime_Func(s_Time1, s_Time2):
            InitialContact = (s_Time1[:1].values)
            PushOff = (s_Time1[-1:].values)
            NextContact = (s_Time2[:1].values)

            StanceTime = PushOff-InitialContact
            FlightTime = NextContact-PushOff

            PhaseTime_df = pd.DataFrame([StanceTime,FlightTime], columns=['Step1'], index=['Contact time', 'Flight time'])
            return PhaseTime_df

        PhaseTime = PhaseTime_Func(Time1, Time2);
        PhaseTime['Step3']=PhaseTime_Func(Time3, Time4);
        PhaseTime['Step5']=PhaseTime_Func(Time5, Time6);
        PhaseTime['Step7']=PhaseTime_Func(Time7, Time8);
        PhaseTime['Step9']=PhaseTime_Func(Time9, Time10);
        PhaseTime['Step11']=PhaseTime_Func(Time11, Time12);
        PhaseTime['Step13']=PhaseTime_Func(Time13, Time14);
        PhaseTime['Step15']=PhaseTime_Func(Time15, Time16);
        PhaseTime['Step17']=PhaseTime_Func(Time17, Time18);
        PhaseTime['Step19']=PhaseTime_Func(Time19, Time20);


        st.dataframe(PhaseTime, width=1000, height=150)
        # Copy?
        copy_button_PhaseTime = Button(label="Copy: Contact&Flight time")
        copy_button_PhaseTime.js_on_event("button_click", CustomJS(args=dict(df=PhaseTime.to_csv(sep='\t')), code="""
            navigator.clipboard.writeText(df);
            """))
        no_event = streamlit_bokeh_events(
            copy_button_PhaseTime,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)
        #　グラフ
        st.bar_chart(PhaseTime.T)  #グラフ微妙

    if SideButton_PhaseTime_L:
        def PhaseTime_Func(s_Time1, s_Time2):
            InitialContact = (s_Time1[:1].values)
            PushOff = (s_Time1[-1:].values)
            NextContact = (s_Time2[:1].values)

            StanceTime = PushOff-InitialContact
            FlightTime = NextContact-PushOff

            PhaseTime_df = pd.DataFrame([StanceTime,FlightTime], columns=['Step1'], index=['Contact time', 'Flight time'])
            return PhaseTime_df

        PhaseTime = PhaseTime_Func(Time2, Time3);
        PhaseTime['Step4']=PhaseTime_Func(Time4, Time5);
        PhaseTime['Step6']=PhaseTime_Func(Time6, Time7);
        PhaseTime['Step8']=PhaseTime_Func(Time8, Time9);
        PhaseTime['Step10']=PhaseTime_Func(Time10, Time11);
        PhaseTime['Step12']=PhaseTime_Func(Time12, Time13);
        PhaseTime['Step14']=PhaseTime_Func(Time14, Time15);
        PhaseTime['Step16']=PhaseTime_Func(Time16, Time18);
        PhaseTime['Step18']=PhaseTime_Func(Time18, Time19);
        PhaseTime['Step20']=PhaseTime_Func(Time20, Time21);

        st.dataframe(PhaseTime, width=1000, height=150)
        # Copy?
        copy_button_PhaseTime = Button(label="Copy: Contact&Flight time")
        copy_button_PhaseTime.js_on_event("button_click", CustomJS(args=dict(df=PhaseTime.to_csv(sep='\t')), code="""
            navigator.clipboard.writeText(df);
            """))
        no_event = streamlit_bokeh_events(
            copy_button_PhaseTime,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)
        #　グラフ
        st.bar_chart(PhaseTime.T)  #グラフ微妙
        #dfから平均値を求める

#________________________________________________________________________________________________________________________
    """
    #
    ## ▶︎　2. ファイル2の結果
    ## 2-1: その他の分析データ参照
    """
    st.title('')
    st.title('▶︎　2. ファイル2の結果')
    st.write('2-1: その他の分析データ参照')
    ex_file = pd.ExcelFile(uploaded_file_02)
    ex_df = pd.read_excel(ex_file, sheet_name = 0)
    ex_Time = ex_df[ex_Time]
    ex_DATA1 = ex_df[ex_Var1]
    # if ex_Var2_Check2:
    #     ex_DATA2 = ex_df[ex_Var2]
    # if ex_Var3_Check2:
    #     ex_DATA3 = ex_df[ex_Var3]

    def ExtDataAnalysis_df_Func(exDATA):
        def ExtDataAnalysis_Func(sTime, sData, Tn, Dn):
            InitialContact_Time = sTime[:1].values
            ToeOff_Time = sTime[-1:].values
            InitialContact_Frame = ex_df.query('Time == '+str(InitialContact_Time))['Frame'].values
            ToeOff_Frame = ex_df.query('Time == '+str(ToeOff_Time))['Frame'].values

            X1 = range(int(InitialContact_Frame),int(ToeOff_Frame+1))
            Y1 = sData[range(int(InitialContact_Frame),int(ToeOff_Frame+1))]
            T1 = ex_Time[range(int(InitialContact_Frame),int(ToeOff_Frame+1))]
            ex_df_n = pd.DataFrame(T1,columns=[Tn])
            ex_df_n[Dn]=Y1
            ex_df_n[Tn]=T1
            return ex_df_n

        ex_df1 = ExtDataAnalysis_Func(Time1, exDATA, 'Time1', 'DATA1'); ex_df1.reset_index(inplace=True, drop=True)
        ex_df2 = ExtDataAnalysis_Func(Time2, exDATA, 'Time2', 'DATA2'); ex_df2.reset_index(inplace=True, drop=True)
        ex_df3 = ExtDataAnalysis_Func(Time3, exDATA, 'Time3', 'DATA3'); ex_df3.reset_index(inplace=True, drop=True)
        ex_df4 = ExtDataAnalysis_Func(Time4, exDATA, 'Time4', 'DATA4'); ex_df4.reset_index(inplace=True, drop=True)
        ex_df5 = ExtDataAnalysis_Func(Time5, exDATA, 'Time5', 'DATA5'); ex_df5.reset_index(inplace=True, drop=True)
        ex_df6 = ExtDataAnalysis_Func(Time6, exDATA, 'Time6', 'DATA6'); ex_df6.reset_index(inplace=True, drop=True)
        ex_df7 = ExtDataAnalysis_Func(Time7, exDATA, 'Time7', 'DATA7'); ex_df7.reset_index(inplace=True, drop=True)
        ex_df8 = ExtDataAnalysis_Func(Time8, exDATA, 'Time8', 'DATA8'); ex_df8.reset_index(inplace=True, drop=True)
        ex_df9 = ExtDataAnalysis_Func(Time9, exDATA, 'Time9', 'DATA9'); ex_df9.reset_index(inplace=True, drop=True)
        ex_df10 = ExtDataAnalysis_Func(Time10, exDATA, 'Time10', 'DATA10'); ex_df10.reset_index(inplace=True, drop=True)
        ex_df11 = ExtDataAnalysis_Func(Time11, exDATA, 'Time11', 'DATA11'); ex_df11.reset_index(inplace=True, drop=True)
        ex_df12 = ExtDataAnalysis_Func(Time12, exDATA, 'Time12', 'DATA12'); ex_df12.reset_index(inplace=True, drop=True)
        ex_df13 = ExtDataAnalysis_Func(Time13, exDATA, 'Time13', 'DATA13'); ex_df13.reset_index(inplace=True, drop=True)
        ex_df14 = ExtDataAnalysis_Func(Time14, exDATA, 'Time14', 'DATA14'); ex_df14.reset_index(inplace=True, drop=True)
        ex_df15 = ExtDataAnalysis_Func(Time15, exDATA, 'Time15', 'DATA15'); ex_df15.reset_index(inplace=True, drop=True)
        ex_df16 = ExtDataAnalysis_Func(Time16, exDATA, 'Time16', 'DATA16'); ex_df16.reset_index(inplace=True, drop=True)
        ex_df17 = ExtDataAnalysis_Func(Time17, exDATA, 'Time17', 'DATA17'); ex_df17.reset_index(inplace=True, drop=True)
        ex_df18 = ExtDataAnalysis_Func(Time18, exDATA, 'Time18', 'DATA18'); ex_df18.reset_index(inplace=True, drop=True)
        ex_df19 = ExtDataAnalysis_Func(Time19, exDATA, 'Time19', 'DATA19'); ex_df19.reset_index(inplace=True, drop=True)
        ex_df20 = ExtDataAnalysis_Func(Time20, exDATA, 'Time20', 'DATA20'); ex_df20.reset_index(inplace=True, drop=True)

        Extra_df = pd.concat([ex_df1,ex_df2,ex_df3,ex_df4,ex_df5,ex_df6,ex_df7,ex_df8,ex_df9,ex_df10,
                              ex_df11,ex_df12,ex_df13,ex_df14,ex_df15,ex_df16,ex_df17,ex_df18,ex_df19,ex_df20],axis=1)
        return Extra_df
    ex_Table = ExtDataAnalysis_df_Func(ex_DATA1)

    ## 出力項目
    # データフレーム
    st.dataframe(ex_Table)
    # Copy?
    copy_button_ex = Button(label="Copy: Extra data 1")
    copy_button_ex.js_on_event("button_click", CustomJS(args=dict(df=ex_Table.to_csv(sep='\t')), code="""
        navigator.clipboard.writeText(df);
        """))
    no_event_ex = streamlit_bokeh_events(
        copy_button_ex,
        events="GET_TEXT",
        key="get_text",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    # FIGURE
    # Figure: Each data
    # Figure setting
    ex_fig = figure(title=str(ex_Var1), x_axis_label='Time (s)', y_axis_label=str(ex_Var1), frame_height=200)
    # ラインカラー・幅
    LC_ALL = 'black'
    LC_DATA = 'red'
    LW = 1.3
    # GRFz ALL
    ex_fig.line(ex_Time,ex_DATA1, line_color=LC_ALL)
    # GRFz each steps
    ex_fig.line(ex_Table['Time1'], ex_Table['DATA1'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time2'], ex_Table['DATA2'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time3'], ex_Table['DATA3'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time4'], ex_Table['DATA4'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time5'], ex_Table['DATA5'],line_color=LC_DATA, line_width = LW);
    ex_fig.line(ex_Table['Time6'], ex_Table['DATA6'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time7'], ex_Table['DATA7'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time8'], ex_Table['DATA8'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time9'], ex_Table['DATA9'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time10'], ex_Table['DATA10'],line_color=LC_DATA, line_width = LW);
    ex_fig.line(ex_Table['Time11'], ex_Table['DATA11'],line_color=LC_DATA, line_width = LW);   ex_fig.line(ex_Table['Time12'], ex_Table['DATA12'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time13'], ex_Table['DATA13'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time14'], ex_Table['DATA14'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time15'], ex_Table['DATA15'],line_color=LC_DATA, line_width = LW);
    ex_fig.line(ex_Table['Time16'], ex_Table['DATA16'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time17'], ex_Table['DATA17'],line_color=LC_DATA, line_width = LW);   ex_fig.line(ex_Table['Time18'], ex_Table['DATA18'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time19'], ex_Table['DATA19'],line_color=LC_DATA, line_width = LW);    ex_fig.line(ex_Table['Time20'], ex_Table['DATA20'],line_color=LC_DATA, line_width = LW);


    st.write('> 分析区間のデータ: 分析データ（赤ライン）, すべてのデータ（黒ライン）')
    st.bokeh_chart(ex_fig, use_container_width=True)


    st.title('File2: 平均値')
    SideButton_Ex_Spline_R = st.button('その他のデータ:  1st-Steps 平均値')
    SideButton_Ex_Spline_L = st.button('その他のデータ:  2nd-Steps 平均値')

    if SideButton_Ex_Spline_R:
        st.write('1st steps')
        def Spline_Func(s_df):
            Num = s_df.count()
            x = np.arange(Num)
            y = s_df.dropna().values
            f = interp1d(x, y, kind='cubic')
            k = np.linspace(0,Num-1, num=101)
            spline = pd.DataFrame(f(k))
            return spline

        ex_Table_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
        ex_Table_Spline['Step1']=Spline_Func(ex_Table['DATA1']);    ex_Table_Spline['Step3']=Spline_Func(ex_Table['DATA3']);    ex_Table_Spline['Step5']=Spline_Func(ex_Table['DATA5']);    ex_Table_Spline['Step7']=Spline_Func(ex_Table['DATA7']);    ex_Table_Spline['Step9']=Spline_Func(ex_Table['DATA9']);
        ex_Table_Spline['Step11']=Spline_Func(ex_Table['DATA11']);  ex_Table_Spline['Step13']=Spline_Func(ex_Table['DATA13']);  ex_Table_Spline['Step15']=Spline_Func(ex_Table['DATA15']);  ex_Table_Spline['Step17']=Spline_Func(ex_Table['DATA17']);  ex_Table_Spline['Step19']=Spline_Func(ex_Table['DATA19']);


        st.dataframe(ex_Table_Spline)
        # データフレーム

        # Copy?
        copy_button_ex2_R = Button(label="Copy: Extra data mean")
        copy_button_ex2_R.js_on_event("button_click", CustomJS(args=dict(df=ex_Table_Spline.to_csv(sep='\t')), code="""
            navigator.clipboard.writeText(df);
            """))
        ex_no_event_R = streamlit_bokeh_events(
            copy_button_ex2_R,
            events="ex_R_GET_TEXT",
            key="ex_R_get_text",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

        ex_Table_Spline_R2 = ex_Table_Spline.drop(columns='Frame')
        st.line_chart(ex_Table_Spline_R2)

    if SideButton_Ex_Spline_L:
        st.write('2nd steps')
        def Spline_Func(s_df):
            Num = s_df.count()
            x = np.arange(Num)
            y = s_df.dropna().values
            f = interp1d(x, y, kind='cubic')
            k = np.linspace(0,Num-1, num=101)
            spline = pd.DataFrame(f(k))
            return spline

        ex_Table_Spline = pd.DataFrame(range(0,101),columns=['Frame']);
        ex_Table_Spline['Step2']=Spline_Func(ex_Table['DATA2']);    ex_Table_Spline['Step4']=Spline_Func(ex_Table['DATA4']);    ex_Table_Spline['Step6']=Spline_Func(ex_Table['DATA6']);    ex_Table_Spline['Step8']=Spline_Func(ex_Table['DATA8']);    ex_Table_Spline['Step10']=Spline_Func(ex_Table['DATA10']);
        ex_Table_Spline['Step12']=Spline_Func(ex_Table['DATA12']);  ex_Table_Spline['Step14']=Spline_Func(ex_Table['DATA14']);  ex_Table_Spline['Step16']=Spline_Func(ex_Table['DATA16']);  ex_Table_Spline['Step18']=Spline_Func(ex_Table['DATA18']);  ex_Table_Spline['Step20']=Spline_Func(ex_Table['DATA20']);


        st.dataframe(ex_Table_Spline)
        # データフレーム

        # Copy?
        copy_button_ex2_L = Button(label="Copy: Extra data mean")
        copy_button_ex2_L.js_on_event("button_click", CustomJS(args=dict(df=ex_Table_Spline.to_csv(sep='\t')), code="""
            navigator.clipboard.writeText(df);
            """))
        ex_no_event_L = streamlit_bokeh_events(
            copy_button_ex2_L,
            events="ex_L_GET_TEXT",
            key="ex_L_get_text",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

        ex_Table_Spline_L2 = ex_Table_Spline.drop(columns='Frame')
        st.line_chart(ex_Table_Spline_L2)

if __name__ == '__STEP10__':
    Sub10()
