import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Performance Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better styling ---
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Full Student Dataset (10 Students)
data = [
    {"Name": "Rasheed Ahamed", "English": 69, "Informatics Practices": 81, "Accountancy": 65, "Business Studies": 66, "Economics": 67, "Physical Education": 78, "Islamic Education": 83},
    {"Name": "Aisha Khan", "English": 48, "Informatics Practices": 52, "Accountancy": 89, "Business Studies": 37, "Economics": 51, "Physical Education": 63, "Islamic Education": 92},
    {"Name": "Liam O'Connor", "English": 61, "Informatics Practices": 92, "Accountancy": 73, "Business Studies": 95, "Economics": 90, "Physical Education": 50, "Islamic Education": 0},
    {"Name": "Sofia Martinez", "English": 75, "Informatics Practices": 81, "Accountancy": 37, "Business Studies": 76, "Economics": 92, "Physical Education": 91, "Islamic Education": 0},
    {"Name": "Chen Wei", "English": 71, "Informatics Practices": 83, "Accountancy": 68, "Business Studies": 89, "Economics": 82, "Physical Education": 60, "Islamic Education": 0},
    {"Name": "Amara Okafor", "English": 95, "Informatics Practices": 45, "Accountancy": 48, "Business Studies": 56, "Economics": 87, "Physical Education": 47, "Islamic Education": 0},
    {"Name": "Yuki Tanaka", "English": 38, "Informatics Practices": 23, "Accountancy": 18, "Business Studies": 25, "Economics": 41, "Physical Education": 8, "Islamic Education": 0},
    {"Name": "Lucas Silva", "English": 82, "Informatics Practices": 49, "Accountancy": 87, "Business Studies": 81, "Economics": 89, "Physical Education": 67, "Islamic Education": 0},
    {"Name": "Elena Petrova", "English": 38, "Informatics Practices": 70, "Accountancy": 56, "Business Studies": 54, "Economics": 38, "Physical Education": 77, "Islamic Education": 0},
    {"Name": "Omar Al-Fayed", "English": 78, "Informatics Practices": 91, "Accountancy": 62, "Business Studies": 83, "Economics": 78, "Physical Education": 86, "Islamic Education": 53}
]

# Subject list for calculations
subjects = ["English", "Informatics Practices", "Accountancy", "Business Studies", "Economics", "Physical Education", "Islamic Education"]

# --- Create DataFrame ---
df = pd.DataFrame(data)

# Calculate Average Score
df["Average Score"] = df[subjects].mean(axis=1).round(2)

# Logic for Passing: All scores >= 40
def check_passing(row):
    for subject in subjects:
        if row[subject] < 40:
            return "Needs Improvement"
    return "Passing"

df["Status"] = df.apply(check_passing, axis=1)

# --- Sidebar Navigation ---
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Select a page:", ["Dashboard", "Student Details", "Analytics", "Download Data"])

# --- Page 1: Dashboard ---
if page == "Dashboard":
    st.title("📊 Student Performance Tracker Dashboard")
    st.markdown("---")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df), delta=None)
    
    with col2:
        passing_count = len(df[df["Status"] == "Passing"])
        st.metric("Passing Students", passing_count, delta=f"{(passing_count/len(df)*100):.1f}%")
    
    with col3:
        failing_count = len(df[df["Status"] == "Needs Improvement"])
        st.metric("Needs Improvement", failing_count, delta=f"{(failing_count/len(df)*100):.1f}%")
    
    with col4:
        class_avg = df["Average Score"].mean()
        st.metric("Class Average", f"{class_avg:.2f}", delta=None)
    
    st.markdown("---")
    
    # Display DataFrame
    st.subheader("📋 All Students Performance")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart for average scores
        fig_avg = px.bar(
            df.sort_values("Average Score", ascending=False),
            x="Name",
            y="Average Score",
            color="Status",
            color_discrete_map={"Passing": "#2ecc71", "Needs Improvement": "#e74c3c"},
            title="Average Scores by Student",
            labels={"Average Score": "Average Score", "Name": "Student Name"}
        )
        fig_avg.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_avg, use_container_width=True)
    
    with col2:
        # Pie chart for passing status
        status_counts = df["Status"].value_counts()
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Student Status Distribution",
            color_discrete_map={"Passing": "#2ecc71", "Needs Improvement": "#e74c3c"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- Page 2: Student Details ---
elif page == "Student Details":
    st.title("👤 Individual Student Details")
    st.markdown("---")
    
    # Select a student
    selected_student = st.selectbox("Select a student:", df["Name"].tolist())
    
    student_data = df[df["Name"] == selected_student].iloc[0]
    
    # Display student info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Student Name", selected_student)
    
    with col2:
        st.metric("Average Score", f"{student_data['Average Score']:.2f}")
    
    with col3:
        st.metric("Status", student_data["Status"])
    
    st.markdown("---")
    
    # Subject scores table
    st.subheader("📚 Subject-wise Scores")
    subject_scores = {subject: student_data[subject] for subject in subjects}
    subject_df = pd.DataFrame(list(subject_scores.items()), columns=["Subject", "Score"])
    st.dataframe(subject_df, use_container_width=True, hide_index=True)
    
    # Subject scores bar chart
    fig_subject = px.bar(
        subject_df,
        x="Subject",
        y="Score",
        color="Score",
        color_continuous_scale="RdYlGn",
        title=f"Subject Scores for {selected_student}",
        labels={"Score": "Score", "Subject": "Subject"}
    )
    fig_subject.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Pass Threshold (40)")
    fig_subject.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_subject, use_container_width=True)

# --- Page 3: Analytics ---
elif page == "Analytics":
    st.title("📈 Class Analytics")
    st.markdown("---")
    
    # Subject-wise average
    st.subheader("📊 Subject-wise Class Average")
    subject_averages = {subject: df[subject].mean() for subject in subjects}
    subject_avg_df = pd.DataFrame(list(subject_averages.items()), columns=["Subject", "Average Score"])
    subject_avg_df = subject_avg_df.sort_values("Average Score", ascending=False)
    
    fig_subject_avg = px.bar(
        subject_avg_df,
        x="Subject",
        y="Average Score",
        color="Average Score",
        color_continuous_scale="Viridis",
        title="Class Average by Subject",
        labels={"Average Score": "Average Score", "Subject": "Subject"}
    )
    fig_subject_avg.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Target (50)")
    fig_subject_avg.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_subject_avg, use_container_width=True)
    
    st.markdown("---")
    
    # Performance distribution
    st.subheader("📊 Score Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig_hist = px.histogram(
            df,
            x="Average Score",
            nbins=10,
            title="Distribution of Average Scores",
            labels={"Average Score": "Average Score", "count": "Number of Students"}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Box plot
        fig_box = go.Figure()
        for subject in subjects:
            fig_box.add_trace(go.Box(y=df[subject], name=subject))
        fig_box.update_layout(
            title="Score Distribution by Subject",
            yaxis_title="Score",
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_box, use_container_width=True)

# --- Page 4: Download Data ---
elif page == "Download Data":
    st.title("📥 Download Data")
    st.markdown("---")
    
    # Convert dataframe to CSV
    csv = df.to_csv(index=False)
    
    # Download button
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="student_performance.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Display data summary
    st.subheader("Data Summary")
    st.write(f"**Total Records:** {len(df)}")
    st.write(f"**Total Subjects:** {len(subjects)}")
    st.write(f"**Passing Students:** {len(df[df['Status'] == 'Passing'])}")
    st.write(f"**Students Needing Improvement:** {len(df[df['Status'] == 'Needs Improvement'])}")
    
    st.markdown("---")
    
    # Show the full dataframe
    st.subheader("Full Dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Student Performance Tracker | School Project 2024</p>", unsafe_allow_html=True)
