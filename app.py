import streamlit as st
import pandas as pd
import plotly.express as px
import os
from math import floor

st.set_page_config("Smartphone Addiction Exploratory Data Analysis", layout="wide")


def convert_to_readable_time(t):
    hours = floor(t)
    minutes = int((t - floor(t)) * 60)
    return f"{hours} hours and {minutes} minutes"


@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "data", "clean_data.csv")
    data = pd.read_csv(path)
    return data


@st.cache_data
def load_grouped_data():
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "data", "age_grouped_screentime.csv")
    data = pd.read_csv(path)
    data["daily_avg_text"] = data["daily_screen_time_hours"].apply(
        convert_to_readable_time
    )
    data["social_avg_text"] = data["social_media_hours"].apply(convert_to_readable_time)
    data["gaming_avg_text"] = data["gaming_hours"].apply(convert_to_readable_time)
    data["ws_avg_text"] = data["work_study_hours"].apply(convert_to_readable_time)

    return data


def main():

    with st.sidebar:
        st.title("Menu")

        page = st.radio("Select the page", ["Main page", "Plot 1"])
        st.divider()
        st.info("author: somebody")

    if page == "Plot 1":
        try:
            st.title("Average daily usage time")
            df_grouped = load_grouped_data()

            plot_placeholder = st.empty()

            chosen_variable = st.radio(
                "Choose a screen time type:",
                options=(
                    "Overall daily screen time",
                    "Social media screen time",
                    "Gaming screen time",
                    "Work/study screen time",
                ),
                horizontal=True,
            )

            if chosen_variable == "Overall daily screen time":
                fig = px.bar(
                    df_grouped,
                    x="age",
                    y="daily_screen_time_hours",
                    title="Average daily screen time depending on the user's age",
                    custom_data=["daily_avg_text"],
                )
            elif chosen_variable == "Social media screen time":
                fig = px.bar(
                    df_grouped,
                    x="age",
                    y="social_media_hours",
                    title="Average social media usage time depending on the user's age",
                    custom_data=["social_avg_text"],
                )

            elif chosen_variable == "Gaming screen time":
                fig = px.bar(
                    df_grouped,
                    x="age",
                    y="gaming_hours",
                    title="Average gaming time depending on the user's age",
                    custom_data=["gaming_avg_text"],
                )

            elif chosen_variable == "Work/study screen time":
                fig = px.bar(
                    df_grouped,
                    x="age",
                    y="work_study_hours",
                    title="Average work/study time depending on the user's age",
                    custom_data=["ws_avg_text"],
                )

            fig.update_layout(
                xaxis=dict(tickmode="linear", tick0=0, dtick=1),
                yaxis=dict(range=[0, 10]),
            )
            fig.update_traces(
                hovertemplate="%{customdata[0]}<br>%{x} years old",
                marker_color="#E260D1",
                marker_line_color="#000000",
                marker_line_width=1.5,
            )
            plot_placeholder.plotly_chart(fig, use_container_width=True)

            with st.expander("See the dataframe"):
                st.write(df_grouped)

        except FileNotFoundError:
            st.error(f"File not found")
        except Exception as e:
            st.error(f"Unexpected error occured: {e}")
    elif page == "Main page":
        st.title("Smartphone addiction level - interactive dashboard")
        st.text("Main page (to be developed soon)")


if __name__ == "__main__":
    main()
