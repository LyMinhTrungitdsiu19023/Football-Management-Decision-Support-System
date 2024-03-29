import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import spatial
from ratelimit import limits
import requests
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import time 

url = "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"
url_transfer = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
@st.cache_data(experimental_allow_widgets=True)
def load_data(url):
    html = pd.read_html(url, header = 1)
    playerstats = html[0]
    shoot = html[4]
    passing = html[5]
    df = html[8]
    playerstats.drop(playerstats.tail(2).index, inplace = True)
#     playerstats["Nation"] = playerstats["Nation"].str.replace('[a-z]', '')
#     playerstats["Age"] = playerstats["Age"].str.replace(r'(-\d\d\d)', '')

    return playerstats, shoot, passing, df, html

def Analysis(url):
    #Forward
    data = load_data(url)[4]

    #Shoot
    shoot =  data[4]
    shoot.drop(shoot.tail(2).index, inplace = True)
    shoot["Nation"] = shoot["Nation"].str.replace('[a-z]', '')
    shoot = shoot.drop(['SoT%', 'Sh/90', 'SoT/90', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches'], axis=1)
    shoot.rename(columns = {'Gls':'Goals', 'Sh':'Shots total', 'SoT':'Shots on Target', 'G/Sh':'Goal per Shot', 'FK':'Freekick','PK':'Penalty Kick','PKatt':'Pentallty Attemp'}, inplace = True)
    shoot = shoot.reset_index(drop = True) 

    #Pass
    passing =  data[5]
    passing.drop(passing.tail(2).index, inplace = True)
    passing["Nation"] = passing["Nation"].str.replace('[a-z]', '')
#     passing = passing.drop(['xAG','xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'Prog','Matches'], axis=1)
    passing.rename(columns = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    passing = passing.reset_index(drop = True)



    #Defend
    df =  data[8]
    df.drop(df.tail(2).index, inplace = True)
    df["Nation"] = df["Nation"].str.replace('[a-z]', '')
    df = df.drop(['Def 3rd', 'Att 3rd','Att','Lost','Sh','Pass','Tkl+Int','Clr','Matches'], axis=1)
    df.rename(columns = {'Tkl':'Number of Players Tackles', 'Tkl.1':'Number of Tackled by Competitors','Int':'Intercept', 'Err':'Mistakes lead to goals'}, inplace = True)

    df = df.reset_index(drop = True)

    #Possesion
    possesion = data[9]
    possesion.drop(possesion.tail(2).index, inplace = True)
    possesion["Nation"] = possesion["Nation"].str.replace('[a-z]', '')
    possesion_1 = pd.DataFrame()
    possesion_1 = possesion[['Player','Nation','Pos','Age','90s','Touches','Def Pen','Att Pen','Live', 'Rec', 'Mid 3rd']]
    possesion_1.rename(columns = {'Def Pen':'Touches in defensive area of team', 'Att Pen':'Touches in attacking area of team', 'Live':'Live-ball touches', 'Rec':'Number of successfully recieved the pass'}, inplace = True)
    possesion_1 = possesion_1.reset_index(drop = True)

    return shoot, passing, df, possesion_1

def Analysis_Forward(url):
    st.header('Statistics of Forward')

    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("FW")]
    shoot = shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("FW")]
    passing = passing.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("FW")]
    df = df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(df)

    possesion = Analysis(url)[3]
    possesion = possesion.loc[possesion["Pos"].str.contains("FW")]
    possesion = possesion.reset_index(drop = True)
    st.write('Stats of Possesion')
    st.dataframe(possesion)
def Analysis_Mid(url):
    st.header('Statistics of Midfield')


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("MF")]
    shoot = shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("MF")]
    passing = passing.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("MF")]
    df = df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(df)

    possesion = Analysis(url)[3]
    possesion = possesion.loc[possesion["Pos"].str.contains("FW")]
    possesion = possesion.reset_index(drop = True)
    st.write('Stats of Possesion')
    st.dataframe(possesion)
def Analysis_defend(url):
    st.header('Statistics of Defensive')


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("DF")]
    shoot = shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("DF")]
    passing = passing.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("DF")]
    df = df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(df) 

    possesion = Analysis(url)[3]
    possesion = possesion.loc[possesion["Pos"].str.contains("FW")]
    possesion = possesion.reset_index(drop = True)
    st.write('Stats of Possesion')
    st.dataframe(possesion)

def plot_chart(attr, url):
    playerstats = load_data(url)
    html = pd.read_html(url, header = 1)
    defend = html[8]
#     defend = load_data(url)[3]
    defend.drop(defend.tail(2).index, inplace = True)
#     defend = Analysis(url)[2]
    rc = {'figure.figsize':(8,4),
      'axes.facecolor':'#0e1117',
      'axes.edgecolor': '#0e1117',
      'axes.labelcolor': 'white',
      'figure.facecolor': '#0e1117',
      'patch.edgecolor': '#0e1117',
      'text.color': 'white',
      'xtick.color': 'white',
      'ytick.color': 'white',
      'grid.color': 'grey',
      'font.size' : 8,
      'axes.labelsize': 12,
      'xtick.labelsize': 8,
      'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()

    if attr == "Goal":

        goal_df =  load_data(url)[0].sort_values(by='Gls', ascending=False)
        goal_df = goal_df.head(10)
        goal_df_1 = pd.DataFrame()
        goal_df_1 = goal_df[["Player", "Gls"]]
        ax = sns.barplot(x = goal_df_1["Player"], y = goal_df_1["Gls"], data=goal_df_1.reset_index(), color = "#00BFFF")
        ax.set(xlabel = "Player", ylabel = "Goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Assist":

        ast_df =  load_data(url)[0].sort_values(by='Ast', ascending=False)
        ast_df = ast_df.head(10)
        ast_df_1 = pd.DataFrame()
        ast_df_1 = ast_df[["Player", "Ast"]]
        ax = sns.barplot(x = ast_df_1["Player"], y = ast_df_1["Ast"], data=ast_df_1.reset_index(), color = "#FCE6C9")
        ax.set(xlabel = "Player", ylabel = "Assists")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Goal per 90Mins":

        Gls_df =  load_data(url)[0].sort_values(by='Gls.1', ascending=False)
        Gls_df = Gls_df.head(10)
        Gls_df_1 = pd.DataFrame()
        Gls_df_1 = Gls_df[["Player", "Gls.1"]]
        ax = sns.barplot(x = Gls_df_1["Player"], y = Gls_df_1["Gls.1"], data=Gls_df_1.reset_index(), color = "#FFD700")
        ax.set(xlabel = "Player", ylabel = "Goal per Shots")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Passed per 90Mins":

        astcom_df =  load_data(url)[0].sort_values(by='Ast.1', ascending=False)
        astcom_df = astcom_df.head(10)
        astcom_df_1 = pd.DataFrame()
        astcom_df_1 = astcom_df[["Player", "Ast.1"]]
        ax = sns.barplot(x = astcom_df_1["Player"], y = astcom_df_1["Ast.1"], data=astcom_df_1.reset_index(), color = "#7FFF00")
        ax.set(xlabel = "Player", ylabel = "Passed Completed")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Total Yellow Cards":

        CrdY_df =  load_data(url)[0].sort_values(by='CrdY', ascending=False)
        CrdY_df = CrdY_df.head(10)
        CrdY_df_1 = pd.DataFrame()
        CrdY_df_1 = CrdY_df[["Player", "CrdY"]]
        ax = sns.barplot(x = CrdY_df_1["Player"], y = CrdY_df_1["CrdY"], data=CrdY_df_1.reset_index(), color = "#CD5B45")
        ax.set(xlabel = "Player", ylabel = "Yellow Cards")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Total Red Cards":

        CrdR_df =  load_data(url)[0].sort_values(by='CrdR', ascending=False)
        CrdR_df = CrdR_df.head(10)
        CrdR_df_1 = pd.DataFrame()
        CrdR_df_1 = CrdR_df[["Player", "CrdR"]]
        ax = sns.barplot(x = CrdR_df_1["Player"], y = CrdR_df_1["CrdR"], data=CrdR_df_1.reset_index(), color = "#CD5B45")
        ax.set(xlabel = "Player", ylabel = "Red Cards")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)


    if attr == "Total Penalty Goals":

        PKatt_df =  load_data(url)[0].sort_values(by='PKatt', ascending=False)
        PKatt_df = PKatt_df.head(10)
        PKatt_df_1 = pd.DataFrame()
        PKatt_df_1 = PKatt_df[["Player", "PKatt"]]
        ax = sns.barplot(x = PKatt_df_1["Player"], y = PKatt_df_1["PKatt"], data=PKatt_df_1.reset_index(), color = "#53868B")
        ax.set(xlabel = "Player", ylabel = "Total Penalty Goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Tackle Completed":

        tkl_df = defend.sort_values(by='Tkl.1', ascending=False)
        tkl_df = tkl_df.head(10)
        tkl_df_1 = pd.DataFrame()
        tkl_df_1 = tkl_df[["Player", "Tkl.1"]]
        ax = sns.barplot(x = tkl_df_1["Player"], y = tkl_df_1["Tkl.1"], data=tkl_df_1.reset_index(), color = "#79CDCD")
        ax.set(xlabel = "Player", ylabel = "Successful Tackles ")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)


    if attr == "Number of Tackled":

        tkled_df = defend.sort_values(by='Tkl', ascending=False)
        tkled_df = tkled_df.head(10)
        tkled_df_1 = pd.DataFrame()
        tkled_df_1 = tkled_df[["Player", "Tkl"]]
        ax = sns.barplot(x = tkled_df_1["Player"], y = tkled_df_1["Tkl"], data=tkled_df_1.reset_index(), color = "#79CDCD")
        ax.set(xlabel = "Player", ylabel = "Tackled by Competitors")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Mistakes lead to goals":

        err_df = defend.sort_values(by='Err', ascending=False)
        err_df = err_df.head(10)
        err_df_1 = pd.DataFrame()
        err_df_1 = err_df[["Player", "Err"]]
        ax = sns.barplot(x = err_df_1["Player"], y = err_df_1["Err"], data=err_df_1.reset_index(), color = "#79CDCD")
        ax.set(xlabel = "Player", ylabel = "Mistakes lead to goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Done Intercept":

        int_df = defend.sort_values(by='Int', ascending=False)
        int_df = int_df.head(10)
        int_df_1 = pd.DataFrame()
        int_df_1 = int_df[["Player", "Int"]]
        ax = sns.barplot(x = int_df_1["Player"], y = int_df_1["Int"], data=int_df_1.reset_index(), color = "#EE3A8C")
        ax.set(xlabel = "Player", ylabel = "Done Intercept")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Number of Touches":
        possesion = Analysis(url)[3]
        possesion_df = possesion.sort_values(by='Touches', ascending=False)
        possesion_df = possesion_df.head(10)
        possesion_df_1 = pd.DataFrame()
        possesion_df_1 = possesion_df[["Player", "Touches"]]
        ax = sns.barplot(x = possesion_df_1["Player"], y = possesion_df_1["Touches"], data=possesion_df_1.reset_index(), color = "#FFFFFF")
        ax.set(xlabel = "Player", ylabel = "Number of Touches")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Number of Touches in attacking area":
        attTouches = Analysis(url)[3]
        attTouches_df = attTouches.sort_values(by='Touches in attacking area of team', ascending=False)
        attTouches_df = attTouches_df.head(10)
        attTouches_df_1 = pd.DataFrame()
        attTouches_df_1 = attTouches_df[["Player", "Touches in attacking area of team"]]
        ax = sns.barplot(x = attTouches_df_1["Player"], y = attTouches_df_1["Touches in attacking area of team"], data=attTouches_df_1.reset_index(), color = "#FFFFFF")
        ax.set(xlabel = "Player", ylabel = "Touches in attacking area of team")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Playing time":

        time_df =  load_data(url)[0].sort_values(by='90s', ascending=False)
        time_df = time_df.head(10)
        time_df_1 = pd.DataFrame()
        time_df_1 = time_df[["Player", "90s"]]
        ax = sns.barplot(x = time_df_1["Player"], y = time_df_1["90s"], data=time_df_1.reset_index(), color = "#7FFF00")
        ax.set(xlabel = "Player", ylabel = "Playing time divide by 90 second")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)
def prediction(url):
    data = pd.read_html(url, header = 1)
#     data = load_data(url)
    shoot = data[4]
    shoot.drop(shoot.tail(2).index, inplace = True)
    shoot["Nation"] = shoot["Nation"].str.replace('[a-z]', '')
    exshoot = pd.DataFrame()
    exshoot = shoot[['Player','Nation','Age', 'Pos','xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']]
    exshoot = exshoot.reset_index(drop = True) 

    passing = data[5]
    passing.drop(passing.tail(2).index, inplace = True)
    passing["Nation"] = passing["Nation"].str.replace('[a-z]', '')
    expassing = pd.DataFrame()
    expassing = passing[['Player','xAG', 'xA']]


    predic_df = pd.merge(exshoot, expassing, on='Player', how='inner')
    predic_df.rename(columns = {'xG':'Expected Goals', 'npxG':'NonPenalty Expected Goals', 'npxG/Sh':'NonPenalty Expected Goals/shots', 'G-xG':'Goals compare ExGoals', 'np:G-xG':'NonPen Goal compare with expected', 'xAG':'Expected Assist Goals', 'xA':'Expected Assists'}, inplace = True)

    return predic_df 

def prediction_chart(attr):

    rc = {'figure.figsize':(8,4),
      'axes.facecolor':'#0e1117',
      'axes.edgecolor': '#0e1117',
      'axes.labelcolor': 'white',
      'figure.facecolor': '#0e1117',
      'patch.edgecolor': '#0e1117',
      'text.color': 'white',
      'xtick.color': 'white',
      'ytick.color': 'white',
      'grid.color': 'grey',
      'font.size' : 8,
      'axes.labelsize': 12,
      'xtick.labelsize': 8,
      'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()

    predic_df = prediction(url)
    if attr == "Expected Goals":
        xG = predic_df.sort_values(by='Expected Goals', ascending=False)
        xG = xG.head(10)
        xG_1 = pd.DataFrame()
        xG_1 = xG[["Player", "Expected Goals"]]
        ax = sns.barplot(x = xG_1["Player"], y = xG_1["Expected Goals"], data=xG_1.reset_index(), color = "#CD5C5C")
        ax.set(xlabel = "Players with Expected Goal", ylabel = "Expected Goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Expected Assists":
        xA = predic_df.sort_values(by='Expected Assists', ascending=False)
        xA = xA.head(10)
        xA_1 = pd.DataFrame()
        xA_1 = xA[["Player", "Expected Assists"]]
        ax = sns.barplot(x = xA_1["Player"], y = xA_1["Expected Assists"], data=xA_1.reset_index(), color = "#CD5C5C")
        ax.set(xlabel = "Players with Expected Assists", ylabel = "Expected Assists")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)
        
        
def defend_approach(url):
    expected = load_data(url)[0]
    
    fw_df = expected.loc[expected["Pos"].str.contains("FW")]
    fw_df = fw_df[fw_df["Player"].str.contains("Bernardo Silva")==False]
    fw = pd.DataFrame()
    fw = fw_df[['Player','Nation','Pos', 'xG']]
    fw = fw.sort_values(by='xG', ascending=False)

    possesion = Analysis(url)[3]
    mid = pd.DataFrame()
    mid = possesion[['Player','Nation','Pos', 'Mid 3rd']]
    mid = possesion.loc[possesion["Pos"].str.contains("MF")]
    mid = mid.sort_values(by='Mid 3rd', ascending=False)

    df = Analysis(url)[2]
    df.drop(df.tail(2).index, inplace = True)
    df["Nation"] = df["Nation"].str.replace('[a-z]', '')
    de = pd.DataFrame()
    de = df[['Player','Nation','Pos','TklW']]
    de = de.loc[de["Pos"].str.contains("DF")]
    de = de[de["Player"].str.contains("Phil Foden")==False]
    de = de.sort_values(by='TklW', ascending=False)
    
    return fw, mid, de

def possesion_approach(url):

    possesion = Analysis(url)[3]
    fw_df = possesion.loc[possesion["Pos"].str.contains("FW")]
    fw_df = fw_df[fw_df["Player"].str.contains("Bernardo Silva")==False]
    fw = pd.DataFrame()
    fw = fw_df[['Player','Nation','Pos', 'Touches']]
    fw = fw.sort_values(by='Touches', ascending=False)

    mid_df = possesion.loc[possesion["Pos"].str.contains("MF")]
    mid = pd.DataFrame()
    mid = mid_df[['Player','Nation','Pos', 'Touches']]
    mid = mid.sort_values(by='Touches', ascending=False)
    
    de_df = possesion.loc[possesion["Pos"].str.contains("DF")]
    de_df = de_df[de_df["Player"].str.contains("Phil Foden")==False]
    de = pd.DataFrame()
    de = de_df[['Player','Nation','Pos', 'Touches']]
    de = de.sort_values(by='Touches', ascending=False)
    return fw, mid, de

def attack_approach(url):
    expected = load_data(url)[0]
    
    fw_df = expected.loc[expected["Pos"].str.contains("FW")]
    fw_df = fw_df[fw_df["Player"].str.contains("Bernardo Silva")==False]
    fw = pd.DataFrame()
    fw = fw_df[['Player','Nation','Pos', 'xG']]
    fw = fw.sort_values(by='xG', ascending=False)

    mid_df = expected.loc[expected["Pos"].str.contains("MF")]
    mid = pd.DataFrame()
    mid = mid_df[['Player','Nation','Pos', 'xAG']]
    mid = mid.sort_values(by='xAG', ascending=False)
    
    de_df = expected.loc[expected["Pos"].str.contains("DF")]
    de_df = de_df[de_df["Player"].str.contains("Phil Foden")==False]
    de = pd.DataFrame()
    de = de_df[['Player','Nation','Pos', 'xAG']]
    de = de.sort_values(by='xAG', ascending=False)  
    
    return fw, mid, de
