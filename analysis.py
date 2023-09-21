import pandas as pd
import numpy as np


# reading data sets
git_path = "https://raw.githubusercontent.com/Subhashrpg/streamlit/master/ipl_datasets"
path1 = "/ipl1.csv"
path2 = "/ipl2.csv"
df1 = pd.read_csv("https://raw.githubusercontent.com/Subhashrpg/streamlit/master/ipl_datasets/ipl1.csv")
df2 = pd.read_csv("https://raw.githubusercontent.com/Subhashrpg/streamlit/master/ipl_datasets/ipl2.csv")

#data structure 
df1["ID"] = df1["ID"].astype(np.int32)
df1["innings"] = df1["innings"].astype(np.int8)
df1["overs"] = df1["overs"].astype(np.int8)
df1["ballnumber"] = df1["ballnumber"].astype(np.int8)
df1["batsman_run"] = df1["batsman_run"].astype(np.int8)
df1["extras_run"] = df1["extras_run"].astype(np.int8)
df1["total_run"] = df1["total_run"].astype(np.int8)
df1["non_boundary"] = df1["non_boundary"].astype(np.int8)
df1["isWicketDelivery"] = df1["isWicketDelivery"].astype(np.int8)
df1["isWicketDelivery"] = df1["isWicketDelivery"].astype(np.int8)

# getting info part
batter = df1["batter"].unique().tolist()
bowler = df1["bowler"].unique().tolist()
unique_season = sorted(df2["Season"].unique(), reverse = False)

# renameing teams with change
rename = {
    "Kings XI Punjab" : "Punjab Kings",
    "Delhi Daredevils" : "Delhi Capitals",
    "Rising Pune Supergiants" : "Rising Pune Supergiant",
}

df2.replace(rename.keys(),rename.values(),inplace = True)
df1.replace(rename.keys(),rename.values(),inplace = True)


# batter's performance analysis
def batsman_analysis(batter):
    try:
        temp_df = df1[df1["batter"] == batter]

        matches = df2[(df2["Team1Players"].str.contains(batter)) | (df2["Team2Players"].str.contains(batter))].shape[0]
        innings = len(temp_df.groupby("ID")["batter"].count().index.tolist())
        batsman_runs = temp_df["batsman_run"].sum()
        highest_score = temp_df.groupby("ID")["batsman_run"].sum().max()

        four_df = temp_df[(temp_df["batsman_run"] == 4) | (temp_df["batsman_run"] == 6)]
        try:
            fours = four_df.groupby(["batter","batsman_run"])["batsman_run"].count().unstack()[4].values[0]
        except KeyError:
            fours = 0
        try:
            sixes = four_df.groupby(["batter","batsman_run"])["batsman_run"].count().unstack()[6].values[0]
        except KeyError:
                sixes = 0
                
        total_balls = temp_df.groupby(["batter"])["batsman_run"].count().values[0]
        out = temp_df[~temp_df["kind"].isin(["retired hurt","retired out"])]["isWicketDelivery"].sum()

        try:
            strike_rate = round((batsman_runs/total_balls)*100,2)
        except ZeroDivisionError:
            print("something wrong with total_balls variable,please check")
            
        try:
            avg_score = round(batsman_runs/out,2)
        except ZeroDivisionError:
            print("something wrong with avg_score variable,please check")
            
        new_df = temp_df.groupby("ID")["batsman_run"].sum().reset_index()
        fifties = new_df.query("batsman_run >= 50 and batsman_run < 100")["batsman_run"].count()
        hundreds = new_df.query("batsman_run >= 100")["batsman_run"].count()

        data = {"Match": matches,"Inn":innings, "Runs":batsman_runs,"HS": highest_score,"Avg": avg_score,"Strike_rate":strike_rate,"100": hundreds,"50": fifties,"4s": fours,"6s":sixes}
        batsman_df = pd.DataFrame(data, index = [batter])
    except Exception as e:
        print(e)
    else:
        return batsman_df

def batsman_overall(batter):

    final_df = df1.merge(df2, on = "ID")[["ID","batter","batsman_run","Team1","Team2","BattingTeam"]]
    new_df = final_df[final_df["batter"] == batter]

    yb = new_df[new_df.Team1 == new_df.BattingTeam][["Team1","Team2"]]
    tm1 = yb.shift(-1,axis = 1).Team1.values
    new_df.loc[yb.index,["Team1"]] = tm1

    overall = new_df.groupby(["Team1"])["batsman_run"].sum().sort_values(ascending = False).reset_index()
    balls = new_df.groupby(["Team1"])["batsman_run"].count().reset_index().rename(columns = {"batsman_run":"balls"})

    four_df = new_df[(new_df["batsman_run"] == 4)]
    fours = four_df.groupby(["Team1"])["batsman_run"].count().reset_index().rename(columns = {"batsman_run":"4s"})
    six_df = new_df[(new_df["batsman_run"] == 6)]
    sixes = six_df.groupby(["Team1"])["batsman_run"].count().reset_index().rename(columns = {"batsman_run":"6s"})
    six_fours = sixes.merge(fours, on = "Team1", how = "outer")

    hundred_df = new_df.groupby(["ID","Team1"])["batsman_run"].sum().reset_index()
    hundreds = hundred_df[hundred_df["batsman_run"] >= 100].groupby(["Team1"])["batsman_run"].count().reset_index()
    fifties = hundred_df[(hundred_df["batsman_run"] >= 50) & (hundred_df["batsman_run"] < 100)].groupby(["Team1"])["batsman_run"].count().reset_index()
    fifties.rename(columns = {"batsman_run": "50"}, inplace = True)
    hundreds.rename(columns = {"batsman_run": "100"},inplace = True)
    hundred_fifties = fifties.merge(hundreds, on = "Team1", how = "outer").fillna("-")

    matches = new_df.groupby(["ID","Team1"])["batter"].count().reset_index()["Team1"].value_counts().reset_index().rename(columns = {"index":"Team1","Team1":"Match"})
    max_score = new_df.groupby(["ID","Team1"])["batsman_run"].sum().reset_index().groupby("Team1")["batsman_run"].max().reset_index()
    max_score.rename(columns= {"batsman_run":"HS"}, inplace = True)

    overall = overall.merge(matches, on = "Team1", how = "outer").merge(max_score, on = "Team1", how = "outer").merge(
        balls, on = ["Team1"], how = "outer")
    overall = overall.merge(hundred_fifties, on = "Team1", how = "left").merge(six_fours, on = "Team1", how = "left")

    overall["strike_rate"] =  round((overall["batsman_run"]/overall["balls"])*100,2)
    overall["average"] =  round(overall["batsman_run"]/overall["Match"],2)
        
    overall.fillna("-",inplace = True)
    overall.set_index("Team1",inplace = True)
    overall = overall.iloc[:,[1,0,2,9,8,4,5,7,6]]
    overall.rename(columns = {"batsman_run": "Runs","average": "Avg","strike_rate": "Strike_rate"},inplace = True)
    return overall

def bowler_analysis(bowler):
    try:
        temp_df = df1[df1["bowler"] == bowler]
        matches = df2[(df2["Team1Players"].str.contains(bowler)) | (df2["Team2Players"].str.contains(bowler))].shape[0]
        innings = len(temp_df.groupby("ID")["bowler"].count().index.tolist())

        total_balls = temp_df[temp_df["ballnumber"].isin([1,2,3,4,5,6])]["ballnumber"].count()
        total_runs = temp_df[~temp_df["extra_type"].isin(["legbyes","byes","penalty"])]["total_run"].sum()
        total_wicket = temp_df[~temp_df["kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]["kind"].count()

        if total_balls != 0 or total_wicket != 0:
            ecomomy = round((total_runs/total_balls)*6,2)
            average = round(total_runs/total_wicket,2)
        else:
            ecomomy = 0
            average = 0

        inning_runs = temp_df[~temp_df["extra_type"].isin(["legbyes","byes","penalty"])].groupby("ID")["total_run"].sum().reset_index()
        inning_wicket_df = temp_df[~temp_df["kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
        inning_wicket = inning_wicket_df.groupby("ID")["isWicketDelivery"].sum().reset_index()

        bbi_df = inning_runs.merge(inning_wicket, on = "ID").rename(columns= {"isWicketDelivery": "wicket"})
        best_inning = bbi_df.sort_values(by = ["wicket","total_run"], ascending = [False,True])

        try:
            bbi_run = best_inning["total_run"].head(1).values[0]
            bbi_wicket = best_inning["wicket"].head(1).values[0]
        except IndexError:
            bbi_run = 0
            bbi_wicket = 0

        best_match = f"{bbi_run}/{bbi_wicket}"

        wicket_df = inning_wicket.groupby("ID")["isWicketDelivery"].sum().reset_index()
        three_wicket = wicket_df[wicket_df["isWicketDelivery"] <= 4]["isWicketDelivery"].count()
        five_wicket = wicket_df[wicket_df["isWicketDelivery"] >= 5]["isWicketDelivery"].count()


        data = {"Mathces":matches,"Inn": innings,"Balls":total_balls,"Runs":total_runs,"Wicket":total_wicket,"BBM":best_match,"Economy": ecomomy, "Average": average, "3W":three_wicket,"5W": five_wicket}

        bowler_df = pd.DataFrame(data, index = [bowler])
    except Exception as e:
        print(e)
    else:
        return bowler_df

# bowler overall analysis
def bowler_overall(bowler):
    final_df = df1.merge(df2, on = "ID")[["ID","ballnumber","bowler","extra_type","total_run","isWicketDelivery","kind","Season"
                                      ,"Team1","Team2","BattingTeam","Team1Players","Team2Players"]]
    new_df = final_df[final_df.bowler == bowler]

    match_df = new_df.groupby(["ID","BattingTeam"]).bowler.count().reset_index().BattingTeam.value_counts().reset_index().rename(
    columns = {"index" : "BattingTeam", "BattingTeam": "Match"})
    ball_df = new_df[new_df.ballnumber.isin([1,2,3,4,5,6])].groupby("BattingTeam").ballnumber.count().reset_index()

    run_df = new_df[~new_df["extra_type"].isin(["legbyes","byes","penalty"])]
    run_df1 = run_df.groupby("BattingTeam").total_run.sum().reset_index()

    wicket_df = new_df[~new_df["kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
    wicket_df1 = wicket_df.groupby("BattingTeam").isWicketDelivery.sum().reset_index()
    run_wicket_df = run_df1.merge(wicket_df1, on = "BattingTeam", how = "inner")

    best_run = run_df.groupby(["ID","BattingTeam"]).total_run.sum().reset_index()
    best_wicket = wicket_df.groupby(["ID","BattingTeam"]).isWicketDelivery.sum().reset_index()
    best_inning = best_run.merge(best_wicket, on = ["ID","BattingTeam"], how = "inner").sort_values(
        by = ["isWicketDelivery","total_run"], ascending = [False,True]).drop(columns = "ID")
    bbi_df = best_inning.loc[best_inning.groupby("BattingTeam").isWicketDelivery.idxmax()]
    bbi_df["BBM"] = bbi_df.total_run.astype("str") +"/" + bbi_df.isWicketDelivery.astype("str")
    bbi_df = bbi_df.drop(columns = ["total_run","isWicketDelivery"])

    three_wicket = best_inning[best_inning.isWicketDelivery <= 4].groupby("BattingTeam").isWicketDelivery.count().reset_index()
    five_wicket = best_inning[best_inning.isWicketDelivery >= 5].groupby("BattingTeam").isWicketDelivery.count().reset_index()
    three_five_df = three_wicket.merge(five_wicket, on = "BattingTeam", how = "outer")

    final_df = match_df.merge(ball_df, on = "BattingTeam").merge(run_wicket_df, on = "BattingTeam").merge(
    bbi_df, on = "BattingTeam").merge(three_five_df, on = "BattingTeam", how = "outer").rename(
    columns = {"ballnumber": "Balls","total_run": "Runs", "isWicketDelivery": "Wickets","isWicketDelivery_x":"3W","isWicketDelivery_y": "5w","BattingTeam": "Teams"})

    economy = (final_df.apply(lambda row : round(row["Runs"] / row["Balls"],2) if row["Balls"] != 0 else "0", axis = 1)*6).values
    avg = final_df.apply(lambda row : round(row["Runs"] / row["Wickets"],2) if row["Wickets"] != 0 else row["Runs"], axis = 1).values

    final_df.insert(6, "Economy",economy)
    final_df.insert(7, "Average",avg)
    final_df = final_df.set_index("Teams").fillna("0")
    final_df["Average"] = final_df["Average"].astype("float")
    final_df["Economy"] = final_df["Economy"].astype("float")
    
    return final_df

# team overall analysis
def team_overall(df2):
    t1 = df2["Team1"].unique()
    t2 = df2["Team2"].unique()
    df = df2[~df2["WinningTeam"].isna()]
    teams = set(t1)&set(t2)
    new_df = pd.DataFrame()
    data = []

    for team in teams:
        match_played = df[(df["Team1"] == team) | (df["Team2"] == team)].shape[0]
        win = df[df["WinningTeam"] == team].shape[0]
        win_percent = round((win/match_played) *100,2)
        home_win = round((df[(df["WinningTeam"] == team) & (df["Team1"] == team)].shape[0]/ df[df["Team1"] == team].shape[0]) * 100,2)
        away_win = round((df[(df["WinningTeam"] == team) & (df["Team2"] == team)].shape[0]/ df[df["Team2"] == team].shape[0]) * 100,2)
        
        data.append([team,match_played,win,win_percent,home_win,away_win])

    new_df[["Team","Match","Win","Win_percent","Home_win_percent","Away_win_percent"]] = data

    new_df.sort_values(by = "Win_percent", ascending = False, inplace= True)
    new_df.set_index("Team", inplace= True)
    return new_df


# point table
def point_table(df):
    
    t1 = df["Team1"].unique()
    t2 = df["Team2"].unique()
    teams = set(t1)&set(t2)
    new_df = pd.DataFrame()
    data = []
    
    for team in teams:
        match_played = df[(df["Team1"] == team) | (df["Team2"] == team)].shape[0]
        win = df[df["WinningTeam"] == team].shape[0]
        no_result = df[((df["Team1"] == team) | (df["Team2"] == team)) & (df["WinningTeam"].isnull())].shape[0]

        data.append([team,match_played,win,no_result])
        
    new_df[["Team","Match","Win","No Result"]] = data
    new_df["Points"] = new_df["Win"] * 2 + new_df["No Result"]
    
    new_df.sort_values(by = "Points", ascending = False, inplace= True)
    new_df.set_index("Team", inplace = True)
    
    return new_df

# important record
def important_analysis(df1,df2):
    final_df1 = df2[df2.MatchNumber == "Final"].groupby(["Team1"])["MatchNumber"].count().reset_index()
    final_df2 = df2[df2.MatchNumber == "Final"].groupby(["Team2"])["MatchNumber"].count().reset_index()
    final_df = final_df1.merge(final_df2, how = "outer", left_on= "Team1", right_on= "Team2")
    final_df.fillna(0, inplace = True)

    final_df["final_played"] =  final_df["MatchNumber_x"] + final_df["MatchNumber_y"]
    temp_df = final_df.iloc[:,[0,2]][final_df.iloc[:,[0,2]]["Team2"] == 0]
    final_df.loc[temp_df.index,temp_df.columns] = temp_df.shift(1, axis = 1)
    final_df.drop(columns= ["Team1","MatchNumber_x","MatchNumber_y"], inplace = True)
    most_final_played = final_df.sort_values(by = "final_played", ascending= False).head(1)
    most_final_played.rename(columns = {"Team2": "Team"}, inplace = True)
    most_final_played.set_index("Team", inplace = True)

    most_player_of_match = df2.Player_of_Match.value_counts(ascending = False).head(1)
    most_player_of_match = pd.DataFrame(most_player_of_match)
    most_player_of_match.rename(columns = {"Player_of_Match": "Total_MOM"}, inplace = True)

    most_run = df1.groupby("batter")["batsman_run"].sum().sort_values(ascending = False).head(1)
    most_run = pd.DataFrame(most_run)
    most_run.rename(columns = {"batsman_run": "total_runs"}, inplace = True)

    wicket_df = df1[~df1["kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
    most_wicket = wicket_df.groupby("bowler")["isWicketDelivery"].sum().sort_values(ascending = False).head(1)
    most_wicket = pd.DataFrame(most_wicket)
    most_wicket.rename(columns = {"isWicketDelivery": "total_wickets"}, inplace = True)

    most_final_win = df2[df2.MatchNumber == "Final"]["WinningTeam"].value_counts().reset_index().head(1)
    most_final_win.rename(columns = {"index":"Team", "WinningTeam" : "total_win"}, inplace = True)
    most_final_win.set_index("Team", inplace = True)

    return most_final_played,most_final_win,most_player_of_match,most_run,most_wicket

# season important analysis
def season_analysis(season,df1,df2):
    
    temp_df = df2[df2["Season"] == season]
    final_df = temp_df[temp_df["MatchNumber"] == "Final"]
    
    final_team = final_df[["Team1","Team2"]]
    final_won = pd.DataFrame(final_df[["WinningTeam"]]).rename(columns = {"WinningTeam" : "final_win"})
    
    season_id = temp_df["ID"].values.tolist()
    season_run_df = df1[df1.ID.isin(season_id)]
    season_run = pd.DataFrame(season_run_df.groupby("batter")["batsman_run"].sum().sort_values(ascending = False)
             .head(1)).rename(columns= {"batsman_run" : "Total_runs"})
    
    wicket_df = season_run_df[~season_run_df["kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
    season_wicket = pd.DataFrame(wicket_df.groupby("bowler")["isWicketDelivery"].sum().sort_values(ascending = False)
                .head(1)).rename(columns = {"isWicketDelivery": "total wickets"})
    
    season_mom = pd.DataFrame(temp_df.Player_of_Match.value_counts(ascending = False).head(1)
            ).rename(columns = {"Player_of_Match": "Total_MOM"})
    
    return final_team,final_won,season_run,season_wicket,season_mom

# season team overall 
def season_overall(season,df2):
    
    temp_df = df2[df2.Season == season]
    result = team_overall(temp_df)
    return result  

# season point table 
def season_point_table(season, df):
    temp_df = df2[df2.Season == season]
    result = point_table(temp_df)
    return result

# Season important analysis 
def season_important_analysis(season,df1,df2):
    
    temp_df = df2[df2.Season == season]
    season_id = temp_df["ID"].values.tolist()
    
    season_run_df = df1[df1.ID.isin(season_id)]
    top5_batsman = season_run_df.groupby("batter")["batsman_run"].sum().sort_values(ascending = False).head().reset_index(
                    ).rename(columns= {"batsman_run" : "Total_runs"})
    
    wicket_df = season_run_df[~season_run_df["kind"].isin(["run out","retired hurt","obstructing the field","retired out"])]
    top5_bowler = wicket_df.groupby("bowler")["isWicketDelivery"].sum().sort_values(ascending = False).head().reset_index().rename(
    columns = {"isWicketDelivery": "total_wickets"})
    
    top5_sixes = season_run_df[season_run_df.batsman_run == 6].groupby("batter").batsman_run.count().sort_values(
    ascending = False).head().reset_index().rename(columns = {"batsman_run": "total_sixes"})
    
    centuary_df = season_run_df.groupby(["ID","batter"]).batsman_run.sum().sort_values(ascending = False).reset_index().rename(
    columns= {"batsman_run" : "Runs"})[["batter","Runs"]]
    centuary_df = centuary_df[centuary_df.Runs >= 100]
    
    return top5_batsman,top5_bowler,top5_sixes,centuary_df
