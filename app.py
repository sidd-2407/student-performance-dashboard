import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

st.title("📊 Student Performance Dashboard")
st.markdown("Power BI–style interactive dashboard using Streamlit")

# -------------------------
# Sample Student Data
# -------------------------
data = {
    "Student": ["Amit", "Riya", "Suresh", "Neha", "Rahul", "Pooja", "Karan", "Sneha"],
    "Class": ["10A", "10A", "10B", "10B", "10A", "10C", "10C", "10B"],
    "Maths": [78, 85, 67, 90, 88, 72, 81, 95],
    "Science": [82, 88, 70, 92, 85, 75, 79, 93],
    "English": [75, 80, 72, 85, 90, 78, 83, 88],
    "Grade": ["B", "A", "C", "A", "A", "B", "B", "A"],
    "Month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar", "Apr", "Apr"],
    "Profile": [
        "https://i.pravatar.cc/100?img=1",
        "https://i.pravatar.cc/100?img=2",
        "https://i.pravatar.cc/100?img=3",
        "https://i.pravatar.cc/100?img=4",
        "https://i.pravatar.cc/100?img=5",
        "https://i.pravatar.cc/100?img=6",
        "https://i.pravatar.cc/100?img=7",
        "https://i.pravatar.cc/100?img=8",
    ]
}

df = pd.DataFrame(data)

# -------------------------
# Sidebar Filter
# -------------------------
st.sidebar.header("🔍 Filters")
selected_class = st.sidebar.selectbox(
    "Select Class",
    options=["All"] + sorted(df["Class"].unique().tolist())
)

if selected_class != "All":
    df = df[df["Class"] == selected_class]

# -------------------------
# KPI Section
# -------------------------
df["Average"] = df[["Maths", "Science", "English"]].mean(axis=1)

col1, col2, col3, col4 = st.columns(4)

col1.metric("👩‍🎓 Total Students", len(df))
col2.metric("📈 Avg Score", round(df["Average"].mean(), 2))
col3.metric("🏆 Top Score", df["Average"].max())
col4.metric("🥇 Top Student", df.loc[df["Average"].idxmax(), "Student"])

# -------------------------
# Charts Section
# -------------------------
st.markdown("## 📊 Performance Overview")

# Bar Chart – Average Score by Subject
subject_avg = df[["Maths", "Science", "English"]].mean().reset_index()
subject_avg.columns = ["Subject", "Average Score"]

bar_fig = px.bar(
    subject_avg,
    x="Subject",
    y="Average Score",
    text="Average Score",
    title="Average Score by Subject",
    color="Subject"
)
st.plotly_chart(bar_fig, use_container_width=True)

# Pie Chart – Grade Distribution
pie_fig = px.pie(
    df,
    names="Grade",
    title="Grade Distribution",
    hole=0.4
)
st.plotly_chart(pie_fig, use_container_width=True)

# Line Chart – Monthly Average Trend
month_avg = df.groupby("Month")["Average"].mean().reset_index()

line_fig = px.line(
    month_avg,
    x="Month",
    y="Average",
    markers=True,
    title="Monthly Performance Trend"
)
st.plotly_chart(line_fig, use_container_width=True)

# -------------------------
# Student Profiles
# -------------------------
st.markdown("## 🧑‍🎓 Student Profiles")

cols = st.columns(4)
for i, row in df.iterrows():
    with cols[i % 4]:
        st.image(row["Profile"], width=100)
        st.write(f"**{row['Student']}**")
        st.write(f"Class: {row['Class']}")
        st.write(f"Avg Score: {round(row['Average'], 2)}")

st.success("✅ Dashboard Loaded Successfully!")
