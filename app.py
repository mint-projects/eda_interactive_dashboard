import streamlit as st
import pandas as pd
import plotly.express as px
import os
from math import floor


st.set_page_config(page_title="Smartphone Addiction EDA", layout="wide")


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

        header {visibility: hidden;}
        
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


def convert_to_readable_time(t):

    hours = floor(t)
    minutes = int((t - floor(t)) * 60)
    return f"{hours} hours and {minutes} minutes"


@st.cache_data
def load_grouped_data():

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

    st.title("📱 Smartphone Addiction Analysis")

    var_map = {
        "Overall daily screen time": (
            "daily_screen_time_hours",
            "#E260D1",
            "Total Usage",
            "daily_avg_text",
        ),
        "Social media screen time": (
            "social_media_hours",
            "#00d2ff",
            "Social Media",
            "social_avg_text",
        ),
        "Gaming screen time": ("gaming_hours", "#3aff6d", "Gaming", "gaming_avg_text"),
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
            fig_pie = px.pie(df_grouped, values=col_name, names="age", hole=0.4)
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=20, b=0),
                height=250,
                showlegend=False,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {e}")


def main():
    apply_custom_style()

    if "page" not in st.session_state:
        st.session_state.page = "main_dashboard"

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
            if st.button("Sex comparison"):
                st.session_state.page = "sex"
                st.rerun()
            if st.button("Addiction checker"):
                st.session_state.page = "xgb"
                st.rerun()

    if st.session_state.page == "main":
        st.write("Rendering main page")
    elif st.session_state.page == "avg":
        render_avg_dashboard()
    elif st.session_state.page == "sex":
        st.write("Rendering sex comparison dashboard")
    elif st.session_state.page == "xgb":
        st.write("Rendering model")


if __name__ == "__main__":
    main()
