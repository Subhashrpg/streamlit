import streamlit as st
import pandas as pd
import numpy as np
import analysis as alt
import matplotlib.pyplot as plt


# plotting functions
def season_plot(
    axes,
    data=None,
    x=None,
    y=None,
    color="blue",
    title=None,
    x_label=None,
    y_label=None,
    rotation=10,
    font_title=None,
    font_x_y=None,
):
    axes.bar(data=data, x=x, height=y, color=color)
    # axes.set_xticks(x)
    axes.set_xticklabels(x, rotation=rotation)

    axes.set_title(title, fontdict=font_title)
    axes.set_xlabel(x_label, fontdict=font_x_y)
    axes.set_ylabel(y_label, fontdict=font_x_y)
    plt.show()


st.set_page_config(layout="wide", page_title="ipl analysis", page_icon="🟢🟢")
st.sidebar.title(":orange[Ipl Analysis]")
check_box = st.sidebar.selectbox(":blue[Select One]", ["batter", "bowler", "team"])

unique_batter = alt.batter
unique_bowler = alt.bowler
unique_season = alt.unique_season

if check_box == "batter":
    st.sidebar.subheader(":blue[Batsman name]")
    selected_batsman = st.sidebar.selectbox(":blue[Select Batsman]", unique_batter)
    btn1 = st.sidebar.button(":red[Batsman's Record]")

    if btn1:
        st.header(f":orange[{selected_batsman} In IPL(2008-2022)]")

        st.subheader(f":blue[{selected_batsman}'s overall record]")
        batsman_record = alt.batsman_analysis(selected_batsman)
        st.dataframe(batsman_record, use_container_width=True)

        st.subheader(f":blue[{selected_batsman}'s record against team]")
        batsman_overall = alt.batsman_overall(selected_batsman)
        st.dataframe(batsman_overall, use_container_width=True)

        st.subheader(":blue[Graphical Representation]")
        fig, axs = plt.subplots(
            4, 1, layout="constrained", figsize=(8, 16), sharex=True
        )

        season_plot(
            axs[0],
            data=batsman_overall,
            x=batsman_overall.index,
            y="Runs",
            title=f"{selected_batsman}'s runs",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Total Runs",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[0].tick_params(axis="both", which="both", labelsize=8)

        season_plot(
            axs[1],
            data=batsman_overall,
            x=batsman_overall.index,
            y="Avg",
            title=f"{selected_batsman}'s average",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Average",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[1].tick_params(axis="both", which="both", labelsize=8)

        season_plot(
            axs[2],
            data=batsman_overall,
            x=batsman_overall.index,
            y="Strike_rate",
            title=f"{selected_batsman}'s strike rate",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Strike Rate",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[2].tick_params(axis="both", which="both", labelsize=8)

        season_plot(
            axs[3],
            data=batsman_overall,
            x=batsman_overall.index,
            y="HS",
            title=f"{selected_batsman}'s highest score",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Highest Score",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[3].tick_params(axis="both", which="both", labelsize=8)
        st.pyplot(fig)

elif check_box == "bowler":
    st.sidebar.subheader(":blue[Bowler name]")
    select_bowler = st.sidebar.selectbox(":blue[Select Bowler]", unique_bowler)
    btn2 = st.sidebar.button(":red[Bowler's Record]")

    if btn2:
        st.header(f":orange[{select_bowler} In IPL(2008-2022)]")
        st.subheader(f":blue[{select_bowler}'s overall record]")
        bowler_record = alt.bowler_analysis(select_bowler)
        st.dataframe(bowler_record, width=900)

        st.subheader(f":blue[{select_bowler}'s record against teams]")
        bowler_overall = alt.bowler_overall(select_bowler)
        st.dataframe(bowler_overall,width = 900)

        st.subheader(f":blue[Graphical Representation]")
        fig, axs = plt.subplots(
            3, 1, layout="constrained", figsize=(10, 12), sharex=True
        )

        season_plot(
            axs[0],
            data=bowler_overall,
            x=bowler_overall.index,
            y="Wickets",
            title=f"{select_bowler}'s Wickets",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Total Wickets",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[0].tick_params(axis="both", which="both", labelsize=8)

        season_plot(
            axs[1],
            data=bowler_overall,
            x=bowler_overall.index,
            y="Average",
            title=f"{select_bowler}'s average",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Average",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[1].tick_params(axis="both", which="both", labelsize=8)

        season_plot(
            axs[2],
            data=bowler_overall,
            x=bowler_overall.index,
            y="Economy",
            title=f"{select_bowler}'s Economy",
            font_title={"fontsize": 18, "color": "red"},
            rotation=20,
            y_label="Economy",
            font_x_y={"fontsize": 14, "color": "red"},
        )
        axs[2].tick_params(axis="both", which="both", labelsize=8)
        st.pyplot(fig)

else:
    box1 = st.sidebar.selectbox(
        ":blue[Teams analysis]", ["Overall", "Seasonwise analysis"]
    )

    if box1 == "Overall":
        btn4 = st.sidebar.button(":red[Analyse team performance]")

        if btn4:
            st.header(":orange[IPL Team Analysis(2008-2022)]")
            (
                most_final,
                most_win,
                most_mom,
                most_run,
                most_wicket,
            ) = alt.important_analysis(alt.df1, alt.df2)

            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)

            with col1:
                st.subheader(":blue[Most Final Played]")
                st.dataframe(most_final, width=250)
            with col2:
                st.subheader(":blue[Most Final Win]")
                st.dataframe(most_win, 250)
            with col3:
                st.subheader(":blue[Most Wicket]")
                st.dataframe(most_wicket, 250)
            with col4:
                st.subheader(":blue[Most Runs]")
                st.dataframe(most_run, width=300)
            with col5:
                st.subheader(":blue[Most Man Of The Match]")
                st.dataframe(most_mom, width=300)

            st.subheader(":blue[Overall Analysis]")
            team_analysis = alt.team_overall(alt.df2)
            st.dataframe(team_analysis, width=900)

            st.subheader(":blue[Overall Point Table]")
            team_point_table = alt.point_table(alt.df2)
            st.dataframe(team_point_table, width=900)

            # visual representation
            st.subheader(":blue[Graphical Representation]")
            top5_match_played = team_analysis.sort_values(
                by="Match", ascending=False
            ).head()
            top5_win_percent = team_analysis.sort_values(
                by="Win_percent", ascending=False
            ).head()
            top5_win = team_point_table.sort_values(by="Win", ascending=False).head()

            fig, axs = plt.subplots(3, 1, layout="constrained", figsize=(8, 16))

            season_plot(
                axs[0],
                data=top5_match_played,
                x=top5_match_played.index,
                y="Match",
                color="green",
                title="Top 5 teams by match played",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=20,
                y_label="Total Match",
                font_x_y={"fontsize": 14, "color": "orange"},
            )

            season_plot(
                axs[1],
                data=top5_win_percent,
                x=top5_win_percent.index,
                y="Win_percent",
                color="green",
                title="Top 5 teams by win percent",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=20,
                y_label="Win Percent",
                font_x_y={"fontsize": 14, "color": "orange"},
            )

            season_plot(
                axs[2],
                data=top5_win,
                x=top5_win.index,
                y="Win",
                color="green",
                title="Top 5 teams by match win",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=20,
                y_label="Total Wom",
                font_x_y={"fontsize": 14, "color": "orange"},
            )
            st.pyplot(fig)

    else:
        st.sidebar.subheader(":blue[Ipl Season]")
        season = st.sidebar.selectbox(":blue[Select Season]", unique_season)
        season_btn = st.sidebar.button(":red[Season Analysis]")

        if season_btn:
            st.header(f":orange[IPL SEASON({season})]")
            (
                season__team,
                season_won,
                season_run,
                season_wicket,
                season_mom,
            ) = alt.season_analysis(season, alt.df1, alt.df2)

            col1, col2, col3 = st.columns(3)
            col4, col5 = st.columns(2)

            with col1:
                st.subheader(":blue[Most Runs]")
                st.dataframe(season_run, width=200)
            with col2:
                st.subheader(":blue[Most Wicket]")
                st.dataframe(season_wicket, 200)
            with col3:
                st.subheader(":blue[Final Winning Team]")
                st.dataframe(season_won, width=200)
            with col4:
                st.subheader(":blue[Final Played]")
                st.dataframe(season__team, width=600)
            with col5:
                st.subheader(":blue[Most Man Of The Match]")
                st.dataframe(season_mom, width=300)

            st.subheader(":blue[Overall Analysis]")
            season_analysis = alt.season_overall(season, alt.df2)
            st.dataframe(season_analysis, width=900)

            st.subheader(":blue[Point Table]")
            season_point_table = alt.season_point_table(season, alt.df2)
            st.dataframe(season_point_table, width=900)

            # visual_representation
            st.subheader(":blue[Visual Representation]")
            (
                top5_batsman,
                top5_bowler,
                top5_sixes,
                centuary_batsman,
            ) = alt.season_important_analysis(season, alt.df1, alt.df2)

            fig, axs = plt.subplots(2, 2, layout="constrained", figsize=(10, 7))

            season_plot(
                axs[0][0],
                data=top5_batsman,
                x=top5_batsman.batter,
                y="Total_runs",
                color="green",
                title="Top 5 batsman",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=10,
                y_label="Total Runs",
                font_x_y={"fontsize": 14, "color": "orange"},
            )

            season_plot(
                axs[0][1],
                data=top5_bowler,
                x=top5_bowler.bowler,
                y="total_wickets",
                color="green",
                title="Top 5 bowler",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=15,
                y_label="Total Wickets",
                font_x_y={"fontsize": 14, "color": "orange"},
            )

            season_plot(
                axs[1][0],
                data=top5_sixes,
                x=top5_sixes.batter,
                y="total_sixes",
                color="green",
                title="Top 5 batter by sixes",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=15,
                y_label="Total Sixes",
                font_x_y={"fontsize": 14, "color": "orange"},
            )

            season_plot(
                axs[1][1],
                data=centuary_batsman,
                x=centuary_batsman.batter,
                y="Runs",
                color="green",
                title="Batsman(who made centuary)",
                font_title={"fontsize": 18, "color": "orange"},
                rotation=15,
                y_label="Batsman Runs",
                font_x_y={"fontsize": 14, "color": "orange"},
            )
            st.pyplot(fig)