import streamlit as st
import pandas as pd
import plotly.express as px
import os
from math import floor
import pickle
import numpy as np
import time


st.set_page_config(page_title="Smartphone Addiction EDA", layout="wide")

current_dir = os.getcwd()


def apply_custom_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: white;
        }
        
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }

        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 20, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

       /*header {visibility: hidden;}*/
        
        h1, h2, h3, p, span, label {
            color: #e0e0e0 !important;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        .stRadio div[role="radiogroup"] {
            background: rgba(255, 255, 255, 0.03);
            padding: 10px;
            border-radius: 10px;
        }

        [data-testid="stSidebar"] {
            min-width: 250px !important;
            max-width: 400px !important;
            width: 250px !important;
        }

        /* Opcjonalnie: dostosowanie głównego kontentu, aby nie nachodził na szeroki sidebar */
        .stAppViewBlockContainer {
            margin-left: auto;
            margin-right: auto;
        }
        
        </style>
    """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_model():
    path = os.path.join(current_dir, "model", "model.pkl")
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error(f"Model file not found at {path}. Check your file structure.")
    except (pickle.UnpicklingError, EOFError):
        st.error("Model file is corrupted or not a valid pickle file.")
    except ModuleNotFoundError as e:
        st.error(f"Missing library required to load model: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while loading the model: {e}")


def convert_to_readable_time(t):

    hours = floor(t)
    minutes = int((t - floor(t)) * 60)
    return f"{hours} hours and {minutes} minutes"


@st.cache_data
def load_grouped_data():
    data = pd.DataFrame()
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "data", "age_grouped_screentime.csv")
    if not os.path.exists(path):

        return pd.DataFrame(
            {
                "age": range(15, 25),
                "daily_screen_time_hours": [5, 6, 7, 8, 7, 6, 5, 4, 5, 6],
            }
        )

    data = pd.read_csv(path)
    data["daily_avg_text"] = data["daily_screen_time_hours"].apply(
        convert_to_readable_time
    )
    data["social_avg_text"] = data["social_media_hours"].apply(convert_to_readable_time)
    data["gaming_avg_text"] = data["gaming_hours"].apply(convert_to_readable_time)
    data["ws_avg_text"] = data["work_study_hours"].apply(convert_to_readable_time)

    return data


@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "data", "clean_data.csv")
    data = pd.DataFrame()
    try:
        data = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
    except Exception as e:
        st.error(f"Error: {e}")
    return data


def render_gender_dashboard():
    st.title("👫 Gender-Based Usage Analysis")

    st.markdown(
        """
        <style>
        .gender-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    try:
        data = load_data()
        color_map = {"Female": "#E260D1", "Male": "#00d2ff", "Other": "#3aff6d"}

        def create_gender_donut(df, column, title):
            avg_df = df.groupby("gender")[[column]].mean().reset_index()

            fig = px.pie(
                avg_df,
                values=column,
                names="gender",
                hole=0.3,
                template="plotly_dark",
                color="gender",
                color_discrete_map=color_map,
            )

            fig.update_layout(
                title={
                    "text": f"<b>{title}</b>",
                    "y": 0.9,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top",
                },
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5
                ),
                margin=dict(l=20, r=20, t=50, b=20),
                height=350,
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                marker=dict(line=dict(color="rgba(0,0,0,0)", width=0)),
                hovertemplate="<b>%{label}</b><br>Avg: %{value:.2f}h<extra></extra>",
            )
            return fig

        row1_left, row1_right = st.columns(2)
        row2_left, row2_right = st.columns(2)

        with row1_left:
            st.plotly_chart(
                create_gender_donut(
                    data, "daily_screen_time_hours", "Daily Usage Total"
                ),
                use_container_width=True,
            )

        with row1_right:
            st.plotly_chart(
                create_gender_donut(data, "social_media_hours", "Social Media Impact"),
                use_container_width=True,
            )

        with row2_left:
            st.plotly_chart(
                create_gender_donut(data, "gaming_hours", "Gaming Habits"),
                use_container_width=True,
            )

        with row2_right:
            st.plotly_chart(
                create_gender_donut(data, "work_study_hours", "Productive Usage"),
                use_container_width=True,
            )

    except Exception as e:
        st.error(f"Error: {e}")


def render_main():

    st.markdown(
        """
        <div style="text-align: center; padding: 40px 0px;">
            <h1 style="font-size: 3.5rem; margin-bottom: 10px;">📱 Smartphone addiction analysis </h1>
            <p style="font-size: 1.2rem; color: #b0b0b0;">Decoding the impact of smartphone habits on our daily lives.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🔍 Project Overview")
        st.write(
            """
        Welcome to the **Smartphone Addiction Analysis Dashboard**. This project explores 
        how different demographic factors—like age and gender influence our digital 
        consumption. 
        """
        )

        st.markdown("---")

        st.markdown("### 🛠️ What can you do here?")

        f1, f2, f3 = st.columns(3)
        with f1:
            st.info(
                "**Exploratory Data Analysis**\n\nDive into interactive charts to see how screen time varies across age groupos."
            )
        with f2:
            st.success(
                "**Gender Insights**\n\nCompare usage patterns between Male, Female, and Other categories."
            )

        with f3:
            st.warning(
                "**Addiction Checker**\n\nInput your own data and let our Random Forest model predict your addiction risk."
            )

    with col2:
        st.markdown("### 📊 Dataset Info")
        st.markdown(
            """
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);">
            <p><strong>Source:</strong> 
                <a href="https://www.kaggle.com/datasets/algozee/smartphone-usage-and-addiction-analysis-dataset" 
                target="_blank" 
                style="color: #00d2ff; text-decoration: none; font-weight: bold;">
                Kaggle Dataset 🔗
                </a>
            </p>
            <p><strong>Entries:</strong> 7500 unique records</p>
            <p><strong>Target:</strong> addicted_label (Binary)</p>
            <p><strong>Model:</strong> Random Forest Classifier</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.caption("👈 Use the sidebar to navigate between the different analysis modules.")


def render_model_site():
    st.title("💉 Addiction checker")

    model = load_model()

    daily = st.number_input(
        label="How many hours daily do you spend on your phone?",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.5,
    )

    weekend = st.number_input(
        label="What is your weekend screentime?",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.5,
    )

    social = st.number_input(
        label="How many hours daily do you spend on social media?",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.5,
    )

    data = np.array([[social, daily, weekend]])

    addiction_percentage = model.predict_proba(data)[0, 1]
    addiction_percentage = float(addiction_percentage * 100)
    placeholder = st.empty()

    with placeholder.container():
        st.write("🔍 Analyzing your habits...")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

    if addiction_percentage < 10:
        msg = "✅ **Ultra Low Risk:** Your habits are looking incredibly healthy."
    elif addiction_percentage < 20:
        msg = "🟢 **Low Risk:** You've got a great balance going."
    elif addiction_percentage < 30:
        msg = "🟡 **Mild:** Slightly elevated, but nothing to worry about."
    elif addiction_percentage < 40:
        msg = "🟠 **Moderate:** You're approaching the average usage levels."
    elif addiction_percentage < 50:
        msg = "⚠️ **Borderline:** You are right on the edge of a high-impact lifestyle."
    elif addiction_percentage < 60:
        msg = "⚖️ **Tipping Point:** The model leans slightly toward High Impact."
    elif addiction_percentage < 70:
        msg = "🚩 **Noticeable:** Your screen time is starting to dominate your day."
    elif addiction_percentage < 80:
        msg = (
            "🔥 **High Impact:** The data shows a strong correlation with high stress."
        )
    elif addiction_percentage < 90:
        msg = "🚨 **Significant:** Very high probability of academic/work impact."
    else:
        msg = "🛑 **Critical:** Your digital habits are in the top tier of impact."

    with placeholder.container():
        st.divider()
        st.subheader(f"Result: {addiction_percentage}% probability of addiction")
        st.markdown(f"### {msg}")
        st.info(
            "Note: this is just a simple machine learning model trained on a small Kaggle dataset and should not be treated as professional or medical advice"
        )


def render_avg_dashboard():
    with st.sidebar:
        st.subheader("Settings")
        chosen_variable = st.radio(
            "Select Metric:",
            options=[
                "Overall daily screen time",
                "Social media screen time",
                "Gaming screen time",
                "Work/study screen time",
            ],
        )
        st.info("Tip: Use the charts to explore trends across different age groups.")

    st.title("👴👶 Statistics with respect to age")

    var_map = {
        "Overall daily screen time": (
            "daily_screen_time_hours",
            "#E260D1",
            "Total Usage time",
            "daily_avg_text",
        ),
        "Social media screen time": (
            "social_media_hours",
            "#00d2ff",
            "Social Media usage time",
            "social_avg_text",
        ),
        "Gaming screen time": (
            "gaming_hours",
            "#3aff6d",
            "Gaming time",
            "gaming_avg_text",
        ),
        "Work/study screen time": (
            "work_study_hours",
            "#ffbd3f",
            "Work/Study",
            "ws_avg_text",
        ),
    }
    col_name, color, display_title, custom_col = var_map[chosen_variable]

    row1_left, row1_right = st.columns(2)
    row2_left, row2_right = st.columns(2)

    try:
        df_grouped = load_grouped_data()
        df = load_data()

        with row1_left:
            st.subheader(f"Average {display_title}")
            fig = px.bar(
                df_grouped,
                x="age",
                y=col_name,
                template="plotly_dark",
                custom_data=custom_col,
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0),
                height=350,
                yaxis_range=[0, 10],
            )
            fig.update_traces(
                marker_color=color,
                marker_line_width=0,
                hovertemplate="%{customdata[0]}<br>%{x} years old",
            )
            st.plotly_chart(fig, use_container_width=True)

        with row1_right:
            st.subheader("Key Insights")
            max_val = df_grouped[col_name].max()
            avg_val = df_grouped[col_name].mean()

            c1, c2 = st.columns(2)
            c1.metric("Peak Usage", f"{max_val:.1f}h")
            c2.metric("Average", f"{avg_val:.1f}h")

            st.markdown(
                f"""
            💡 **Observation:** The highest addiction levels for **{display_title.lower()}** are seen in the age group of **{df_grouped.loc[df_grouped[col_name].idxmax(), 'age']}** years old.
            """
            )

        with row2_left:
            st.subheader("Raw Data Preview")
            st.dataframe(
                df_grouped[["age", col_name]].sort_values(by=col_name, ascending=False),
                hide_index=True,
                use_container_width=True,
                height=250,
            )

        with row2_right:
            st.subheader("Distribution")
            fig_hist = px.histogram(
                df, x="daily_screen_time_hours", nbins=24, template="plotly_dark"
            )
            fig_hist.update_traces(
                xbins=dict(start=0.0, end=24.0, size=0.5),
                marker_line_width=1,
                marker_color="orange",
                marker_line_color="rgba(255, 255, 255, 0.1)",
            )

            fig_hist.update_layout(
                xaxis=dict(
                    tickmode="linear",
                    tick0=0,
                    dtick=1,
                    range=[0, 24],
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=30, b=10),
                height=350,
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_hist, use_container_width=True, config={"displayModeBar": False}
            )

    except Exception as e:
        st.error(f"Error loading data: {e}")


def main():
    apply_custom_style()

    if "page" not in st.session_state:
        st.session_state.page = "main_dashboard"
        render_main()

    with st.sidebar:
        st.title("📊 Dashboard")
        st.markdown("---")

        with st.expander("App content"):
            st.write("Go to:")
            if st.button("Main site"):
                st.session_state.page = "main"
                st.rerun()
            if st.button("Average stats"):
                st.session_state.page = "avg"
                st.rerun()
            if st.button("Gender comparison"):
                st.session_state.page = "gender"
                st.rerun()
            if st.button("Addiction checker"):
                st.session_state.page = "rf"
                st.rerun()

    if st.session_state.page == "main":
        render_main()
    elif st.session_state.page == "avg":
        render_avg_dashboard()
    elif st.session_state.page == "gender":
        render_gender_dashboard()
    elif st.session_state.page == "rf":
        render_model_site()


if __name__ == "__main__":
    main()
