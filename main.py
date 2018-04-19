# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 17:14:45 2017

@author: lenovo
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as mlt
import seaborn as sns

import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls


from subprocess import check_output

matches=pd.read_csv('matches.csv')   
delivery=pd.read_csv('deliveries.csv')

matches.head(2)

delivery.head(2)
matches.drop(['umpire3'],axis=1,inplace=True)  #since all the values are NaN
delivery.fillna(0,inplace=True)     #filling all the NaN values with 0


matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW'],inplace=True)

delivery.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW'],inplace=True)


print('Total Matches Played:',matches.shape[0])

print('  Venues Played At:',matches['city'].unique()) 
    
print('  Teams :',matches['team1'].unique())

print('Total venues played at:',matches['city'].nunique())

print('Total umpires ',matches['umpire1'].nunique())

print((matches['player_of_match'].value_counts()).idxmax(),' : has most man of the match awards')

print(((matches['winner']).value_counts()).idxmax(),': has the highest number of match wins')

df=matches.iloc[[matches['win_by_runs'].idxmax()]]

df[['season','team1','team2','winner','win_by_runs']]

df=matches.iloc[[matches['win_by_wickets'].idxmax()]]

df[['season','team1','team2','winner','win_by_wickets']]

print('Toss Decisions in %',((matches['toss_decision']).value_counts())/577*100)

def tossdecision():
    print("\n\t\t\t\t\tTOSS DECISION ACROSS SEASONS")
    mlt.subplots(figsize=(10,6))
    sns.countplot(x='season',hue='toss_decision',data=matches)
    mlt.show()
    
def maxtosswin():
    print("\n\t\t\t\t\t\tMAXIMUM TOSS WINNER")
    mlt.subplots(figsize=(10,6))
    ax=matches['toss_winner'].value_counts().plot.bar(width=0.8)
    for p in ax.patches:
        ax.annotate(format(p.get_height()), (p.get_x()+0.15, p.get_height()+1))
        mlt.show()
        
def tosswinneralsomatchwinner():        
        print("\n\t\t\t\t\tIS TOSS WINNER ALSO MATCH WINNER??")
        df=matches[matches['toss_winner']==matches['winner']]
        slices=[len(df),(577-len(df))]
        labels=['yes','no']
        mlt.pie(slices,labels=labels,startangle=90,shadow=True,explode=(0,0),autopct='%1.1f%%',colors=['r','g'])
        fig = mlt.gcf()
        fig.set_size_inches(6,6)
        mlt.show()
        
def runsacrosseachseason():        
        print("\n\t\t\t\t\tRUNS ACROSS EACH SEASON")
        mlt.subplots(figsize=(10,6))
        batsmen = matches[['id','season']].merge(delivery, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
        #merging the matches and delivery dataframe by referencing the id and match_id columns respectively
        season=batsmen.groupby(['season'])['total_runs'].sum().reset_index()
        season['total_runs'].plot(marker='o')
        mlt.show()
        
def averagerunspermatch():        
        print("\n\t\t\t\t\tAVERAGE RUNS PER MATCH")
        batsmen = matches[['id','season']].merge(delivery, left_on = 'id', right_on = 'match_id', how = 'left').drop('id', axis = 1)
        season=batsmen.groupby(['season'])['total_runs'].sum().reset_index()
        #season['total_runs'].plot(marker='o')
        mlt.subplots(figsize=(10,6))
        avgruns_each_season=matches.groupby(['season']).count().id.reset_index()
        avgruns_each_season.rename(columns={'id':'matches'},inplace=1)
        avgruns_each_season['total_runs']=season['total_runs']
        avgruns_each_season['average_runs_per_match']=avgruns_each_season['total_runs']/avgruns_each_season['matches']
        avgruns_each_season['average_runs_per_match'].plot(marker='o')
        mlt.show()
        
def favouritegrounds():        
        print("\n\t\t\t\t\tFAVOURITE GROUNDS")
        mlt.subplots(figsize=(10,6))
        ax = matches['venue'].value_counts().plot.bar(width=.8, color=["#999966", "#8585ad", "#c4ff4d", "#ffad33"])
        ax.set_xlabel('Grounds')
        ax.set_ylabel('count')
        mlt.show()
        
def maximummanofthematches():        
        print("\n\t\t\t\tMAXIMUM MAN OF THE MATCHES")
        mlt.subplots(figsize=(10,6))
        
        ax = matches['player_of_match'].value_counts().head(10).plot.bar(width=.8, color='R')  #counts the values corresponding 
        # to each batsman and then filters out the top 10 batsman and then plots a bargraph 
        ax.set_xlabel('player_of_match') 
        ax.set_ylabel('count')
        for p in ax.patches:
            ax.annotate(format(p.get_height()), (p.get_x()+0.15, p.get_height()+0.25))
            mlt.show()
            
def batsman_comparator(stat1,stat2,batsman1,batsman2):
    balls=delivery.groupby(['batsman'])['ball'].count().reset_index()
    runs=delivery.groupby(['batsman'])['batsman_runs'].sum().reset_index()
    balls=balls.merge(runs,left_on='batsman',right_on='batsman',how='outer')
    balls.columns=[['batsman','ball_x','ball_y']]
    sixes=delivery.groupby('batsman')['batsman_runs'].agg(lambda x: (x==4).sum()).reset_index()
    fours=delivery.groupby(['batsman'])['batsman_runs'].agg(lambda x: (x==6).sum()).reset_index()
    balls['strike_rate']=balls['ball_y']/balls['ball_x']*100
    balls=balls.merge(sixes,left_on='batsman',right_on='batsman',how='outer')
    balls=balls.merge(fours,left_on='batsman',right_on='batsman',how='outer')
    compare=delivery.groupby(["match_id", "batsman","batting_team"])["batsman_runs"].sum().reset_index()
    compare=compare.groupby(['batsman','batting_team'])['batsman_runs'].max().reset_index()
    balls=balls.merge(compare,left_on='batsman',right_on='batsman',how='outer')
    balls.columns=[['batsman','balls','runs','strike_rate',"6's","4's",'Team','Highest_score']]
    balls.head()
    sns.FacetGrid(balls,hue='Team',size=8).map(mlt.scatter, stat1,stat2, alpha=0.5).add_legend()
    bats1=balls[balls['batsman'].str.contains(batsman1)].sort_values(by=stat1,ascending=False)
    bats2=balls[balls['batsman'].str.contains(batsman2)].sort_values(by=stat1,ascending=False)
    mlt.scatter(bats1[stat1],bats1[stat2]-1,s=75,c='#55ff33')
    mlt.text(x=bats1[stat1].values[0],y=bats1[stat2].values[0],s=batsman1,
            fontsize=10, weight='bold', color='#f46d43')
    mlt.scatter(bats2[stat1],bats2[stat2],s=75,c='#f73545')
    mlt.text(x=bats2[stat1].values[0],y=bats2[stat2].values[0]+1,s=batsman2, 
            fontsize=10, weight='bold', color='#ff58fd')
    fig=mlt.gcf()
    fig.set_size_inches(10,6)
    mlt.title('Batsman Comparator',size=25)
    mlt.show()


print("most no.of runs");
max_runs=delivery.groupby(['batsman'])['batsman_runs'].sum()
ax=max_runs.sort_values(ascending=False)[:6]
#print(ax);

print("bowlers with most no.of wickets");

dismissal_kinds= ["bowled","caught","lbw","stumped","caught and bowled","hit wicket"]
ct=delivery[delivery["dismissal_kind"].isin(dismissal_kinds)]
ax1=ct['bowler'].value_counts()[:5]


#print(ax1);   
#print("allrounder");
#print("Ravindra jadeja");
#print("wicketkeeper");
#print("MS Dhoni");
def dreamteam():    
    print("BEST IPL TEAM ");
    print(ax+ax1)
    #print(ax1)
    #print("\n 1.CH GAYLE \n 2.G GAMBHIR \n 3.SK RAINA \n 4.V KOHLI(c) \n 5.RG SHARMA \n 6.R JADEJA \n 7.MS DHONI(wk) \n 8.SL MALINGA \n 9.A MISHRA \n 10.DJ BRAVO \n 11.PP CHAWLA");
    
       
def menu():
    ch=1;
    while ch!=10:
        print("\n------------------------------------------------------------------------------------------");
        print("\n\n\t\t\t\t\tMENU\n\t\t\t\t1.TOSS DECISION ACROSS SEASONS\n\t\t\t\t2.MAXIMUM TOSS WINNER\n\t\t\t\t3.IS TOSS WINNER ALSO A MATCH WINNER\n\t\t\t\t4.RUNS ACROSS EACH SEASONS\n\t\t\t\t5.AVERAGE RUNS PER MATCH\n\t\t\t\t6.FOVOURITE GROUNDS\n\t\t\t\t7.MAXIMUM MAN OF THE MATCHES\n\t\t\t\t8.PLAYERS COMPARISONS\n\t\t\t\t9.DREAM TEAM\n\t\t\t\t10.EXIT")
        ch=int(input("\t\t\t\t\tenter choice: "))
        if(ch==1):
            tossdecision()
            
        if(ch==2):
            maxtosswin()
            
        if(ch==3):
            tosswinneralsomatchwinner()
            
        if(ch==4):
            runsacrosseachseason()
            
        if(ch==5):
            averagerunspermatch()
            
        if(ch==6):
            favouritegrounds()
            
        if(ch==7):
            maximummanofthematches()
            
        if(ch==8):
            print("Enter stats on basis you want to compare\n" )
            a1=input()
            
            a2=input()
            
            player1=input("enter player 1\n")
            player2=input("enter player 2\n")
            batsman_comparator(a1,a2,player1,player2)
            
        if(ch==9):
            dreamteam()

        
 
    
menu()      
            
