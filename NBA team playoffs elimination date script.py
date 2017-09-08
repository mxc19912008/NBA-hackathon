import pandas as pd
from pandas import DataFrame
import numpy as np
import itertools

# Read in data
division = pd.read_csv("Division_Info.csv")
result = pd.read_csv("2016_17_NBA_Scores.csv")

#Slicing data for convenience
team = division["Team_Name"]
conference = division ["Conference_id"]
division =division["Division_id"]
con_dict = dict(zip(team,conference))
div_dict=dict(zip(team,division))
date = result["Date"]
date=date.unique()

temp1=np.repeat(date,30)
length=date.size
temp2=team
temp3=division

for i in range(1,length):
    temp3=temp3.append(division)
temp4=conference
for i in range(1,length):
    temp4=temp4.append(conference)
for i in range(1,length):
    temp2=temp2.append(team)
    
result=result.set_index(["Date","Home Team"])

# Dta manipulation process:
# df2 is the daily dataframe for team vs team wins.
df2= pd.DataFrame(index=[temp1,temp2],columns=team)


# X is the list of df2, adding a time dimension.
Date = date[0]
for j in range(0,result.loc[date[0]].shape[0]):
    Home = result.loc[Date].index[j]
    Away= result.loc[Date,Home]["Away Team"]
    if result.loc[Date,Home]["Winner"]=="Home":
        df2.loc[Date,Home][Away]=1
    else:
        df2.loc[Date,Away][Home]=1
X=[]
for i in range(0,date.size):
    X.append(df2.loc[date[i]])
for i in range(1,date.size):
    X[i]=X[i].combine_first(X[i-1])
    Date = date[i]
    for j in range(0,result.loc[Date].shape[0]):
        Home = result.loc[Date].index[j]
        Away= result.loc[Date,Home]["Away Team"]
        if result.loc[Date,Home]["Winner"]=="Home":
            last = X[i-1].loc[Home][Away]
            X[i].loc[Home][Away]=1 if pd.isnull(last) else last+1
        else:
            last = X[i-1].loc[Away][Home]
            X[i].loc[Away][Home]=1 if pd.isnull(last) else last+1

for i in range(0,date.size):
    X[i]=X[i].fillna(0)
    

#----------------------------------------------------------------------
    
#df1 is the daily dataframe for team performance.
    
raw_data = {"Date":temp1,"Team":temp2,"Division":temp3,"Conference":temp4}
df1=pd.DataFrame(raw_data,columns=["Date","Team","Division","Conference","Wins",
								"Games Played","Games Remaining","Wining Rate","Net Scores"])
df1=df1.set_index(["Date","Team"])

# Y is the list of df1, adding a time dimension.
Date = date[0]
for j in range(0,result.loc[date[0]].shape[0]):
    Home = result.loc[Date].index[j]
    Away= result.loc[Date,Home]["Away Team"]
    df1.loc[Date,Home]["Games Played"]=1
    df1.loc[Date,Home]["Net Scores"]=result.loc[Date,Home]["Home Score"]-result.loc[Date,Home]["Away Score"]
    df1.loc[Date,Away]["Games Played"]=1
    df1.loc[Date,Away]["Net Scores"]=result.loc[Date,Home]["Away Score"]-result.loc[Date,Home]["Home Score"]
    
    if result.loc[Date,Home]["Winner"]=="Home":
        df1.loc[Date,Home]["Wins"]=1
    else:
        df1.loc[Date,Away]["Wins"]=1

Y=[]
for i in range(0,date.size):
    Y.append(df1.loc[date[i]])
for i in range(1,date.size):
    Y[i]=Y[i].combine_first(Y[i-1])
    Date = date[i]
    for j in range(0,result.loc[Date].shape[0]):
        Home = result.loc[Date].index[j]
        Away= result.loc[Date,Home]["Away Team"]
        #set games played
        last_played = Y[i-1].loc[Home,"Games Played"]
        Y[i].loc[Home,"Games Played"]=1 if pd.isnull(last_played) else last_played + 1
        last_played = Y[i-1].loc[Away,"Games Played"]
        Y[i].loc[Away,"Games Played"]=1 if pd.isnull(last_played) else last_played + 1
        
        #set net scores
        last_net = Y[i-1].loc[Home,"Net Scores"]
        if pd.isnull(last_net):
            Y[i].loc[Home,"Net Scores"]= result.loc[Date,Home]["Home Score"]-result.loc[Date,Home]["Away Score"] 
        else:
            Y[i].loc[Home,"Net Scores"]= last_net+result.loc[Date,Home]["Home Score"]-result.loc[Date,Home]["Away Score"]
        
        last_net = Y[i-1].loc[Away,"Net Scores"]
        if pd.isnull(last_net):
            Y[i].loc[Away,"Net Scores"]= result.loc[Date,Home]["Away Score"]-result.loc[Date,Home]["Home Score"] 
        else:
            Y[i].loc[Away,"Net Scores"]= last_net+result.loc[Date,Home]["Away Score"]-result.loc[Date,Home]["Home Score"]
            
            
        if result.loc[Date,Home]["Winner"]=="Home":
            last = Y[i-1].loc[Home]["Wins"]
            temp = Y[i].loc[Home]
            Y[i].loc[Home,"Wins"]=1 if pd.isnull(last) else last+1
        else:
            last = Y[i-1].loc[Away]["Wins"]
            Y[i].loc[Away,"Wins"]=1 if pd.isnull(last) else last+1
    

for i in range(0,date.size):
    Y[i]=Y[i].fillna(0)


for i in range(0,date.size):
    for j in range(0,30):
        Y[i].iloc[j,4]= 82 - Y[i].iloc[j,3]
        Y[i].iloc[j,5] = Y[i].iloc[j,2]/Y[i].iloc[j,3]


for i in range(0,date.size):
    k=DataFrame(Y[i].to_records())
    k=k.set_index(["Conference","Division"])
    k1=k.loc["East"].sort_values("Wining Rate",ascending=False)
    k1["Conference"]="East"
    k2=k.loc["West"].sort_values("Wining Rate",ascending=False)
    k2["Conference"]="West"
    k1=DataFrame(k1.to_records())
    k2=DataFrame(k2.to_records())
    Y[i]=pd.concat([k1,k2])

# adding max possible winning rate and min winning rate to Y
for i in range(0,date.size):
    Y[i]['Max possible wining rate'] = (Y[i]['Wins']+Y[i]['Games Remaining'])/82
    Y[i]['Min possible wining rate'] = Y[i]['Wins']/82
# Z is a dictionary for updating elimination date.
Z = {}    
for j in range(date.size-1,-1,-1):
    for i in range(8,15):
        if Y[j].loc[i].iloc[0]['Max possible wining rate'] < Y[j].loc[7].iloc[0]['Min possible wining rate']:
            Z[Y[j].loc[i].iloc[0]['Team']] = date[j]
        if abs(Y[j].loc[i].iloc[0]['Max possible wining rate'] - Y[j].loc[7].iloc[0]['Min possible wining rate'])< 1e-6:
            if X[j][Y[j].loc[i].iloc[0]['Team']][Y[j].loc[7].iloc[0]['Team']] > X[j][Y[j].loc[7].iloc[0]['Team']][Y[j].loc[i].iloc[0]['Team']]:
                Z[Y[j].loc[i].iloc[0]['Team']] = date[j]
            elif X[j][Y[j].loc[i].iloc[0]['Team']][Y[j].loc[7].iloc[0]['Team']] == X[j][Y[j].loc[7].iloc[0]['Team']][Y[j].loc[i].iloc[0]['Team']] and Y[j].loc[i].iloc[0]['Net Scores'] < Y[j].loc[7].iloc[0]['Net Scores']:
                Z[Y[j].loc[i].iloc[0]['Team']] = date[j]
        if Y[j].loc[i].iloc[1]['Max possible wining rate'] < Y[j].loc[7].iloc[1]['Min possible wining rate']:
            Z[Y[j].loc[i].iloc[1]['Team']] = date[j]
        if abs(Y[j].loc[i].iloc[1]['Max possible wining rate'] - Y[j].loc[7].iloc[1]['Min possible wining rate'])< 1e-6:
            if X[j][Y[j].loc[i].iloc[1]['Team']][Y[j].loc[7].iloc[1]['Team']] > X[j][Y[j].loc[7].iloc[1]['Team']][Y[j].loc[i].iloc[1]['Team']]:
                Z[Y[j].loc[i].iloc[1]['Team']] = date[j]
            elif X[j][Y[j].loc[i].iloc[1]['Team']][Y[j].loc[7].iloc[1]['Team']] == X[j][Y[j].loc[7].iloc[1]['Team']][Y[j].loc[i].iloc[1]['Team']] and Y[j].loc[i].iloc[1]['Net Scores'] < Y[j].loc[7].iloc[1]['Net Scores']:
                Z[Y[j].loc[i].iloc[1]['Team']] = date[j]
# result_list is the final result list for which we can look up when a team is eliminated.

result_list = []
for t in team:
    if t not in Z.keys():
        result_list.append({t:"Playoffs"})
    else:
        result_list.append({t:Z[t]})
# then we can see the list
result_list
