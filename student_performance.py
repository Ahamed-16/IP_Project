import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF

# --- Page Configuration ---
st.set_page_config(
    page_title="Student Performance Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
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
    .fail-row {
        background-color: #ffcccc !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Student Dataset ---
data = [
    {"Name": "Rasheed Ahamed", "English": 69, "Informatics Practices": 81, "Accountancy": 65, "Business Studies": 66, "Economics": 67, "Physical Education": 78, "Islamic Education": 83},
    {"Name": "Aisha Khan", "English": 48, "Informatics Practices": 52, "Accountancy": 89, "Business Studies": 37, "Economics": 51, "Physical Education": 63, "Islamic Education": 92},
    {"Name": "Liam O'Connor", "English": 61, "Informatics Practices": 92, "Accountancy": 73, "Business Studies": 95, "Economics": 90, "Physical Education": 50, "Islamic Education": 71},
    {"Name": "Sofia Martinez", "English": 75, "Informatics Practices": 81, "Accountancy": 37, "Business Studies": 76, "Economics": 92, "Physical Education": 91, "Islamic Education": 38},
    {"Name": "Chen Wei", "English": 71, "Informatics Practices": 83, "Accountancy": 68, "Business Studies": 89, "Economics": 82, "Physical Education": 60, "Islamic Education": 70},
    {"Name": "Amara Okafor", "English": 95, "Informatics Practices": 45, "Accountancy": 48, "Business Studies": 56, "Economics": 87, "Physical Education": 47, "Islamic Education": 80},
    {"Name": "Yuki Tanaka", "English": 38, "Informatics Practices": 23, "Accountancy": 18, "Business Studies": 25, "Economics": 41, "Physical Education": 8, "Islamic Education": 0},
    {"Name": "Lucas Silva", "English": 82, "Informatics Practices": 49, "Accountancy": 87, "Business Studies": 81, "Economics": 89, "Physical Education": 67, "Islamic Education": 54},
    {"Name": "Elena Petrova", "English": 38, "Informatics Practices": 70, "Accountancy": 56, "Business Studies": 54, "Economics": 38, "Physical Education": 77, "Islamic Education": 82},
    {"Name": "Omar Al-Fayed", "English": 78, "Informatics Practices": 91, "Accountancy": 62, "Business Studies": 83, "Economics": 78, "Physical Education": 86, "Islamic Education": 53}
]

subjects = ["English", "Informatics Practices", "Accountancy", "Business Studies", "Economics", "Physical Education", "Islamic Education"]

# --- DataFrame ---
df = pd.DataFrame(data)
df["Average Score"] = df[subjects].mean(axis=1).round(2)

# --- Grade System ---
def get_grade(avg):
    if avg < 40:
        return "Fail"
    elif 40 <= avg <= 70:
        return "Needs Improvement"
    else:
        return "Pass"

df["Grade"] = df["Average Score"].apply(get_grade)

# --- Passing Logic ---
def check_status(row):
    for subject in subjects:
        if row[subject] < 40:
            return "Failing"
    return "Passing"

df["Status"] = df.apply(check_status, axis=1)

# --- PDF Generator ---
def generate_pdf(student):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="Student Performance Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {student['Name']}", ln=True)
    pdf.cell(200, 10, txt=f"Average Score: {student['Average Score']}", ln=True)
    pdf.cell(200, 10, txt=f"Grade: {student['Grade']}", ln=True)
    pdf.cell(200, 10, txt=f"Status: {student['Status']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Subject Scores:", ln=True)

    for subject in subjects:
        pdf.cell(200, 8, txt=f"{subject}: {student[subject]}", ln=True)

    return pdf.output(dest="S").encode("latin-1")

# --- Sidebar Navigation ---
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Select a page:", ["Dashboard", "Student Details", "Analytics", "Download Data"])

# --- Dashboard Page ---
if page == "Dashboard":
    st.title("📊 Student Performance Dashboard")
    st.markdown("---")

    # Warning Banner
    failing_count = len(df[df["Status"] == "Failing"])
    if failing_count > 0:
        st.error(f"⚠️ **{failing_count} student(s) are failing!** Immediate attention required.")
    else:
        st.success("✅ All students are performing well!")

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(df))
    col2.metric("Passing", len(df[df["Status"] == "Passing"]))
    col3.metric("Failing", failing_count)
    col4.metric("Class Average", f"{df['Average Score'].mean():.2f}")

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Bar chart: Average scores by student
        fig_avg = px.bar(
            df.sort_values("Average Score", ascending=False),
            x="Name",
            y="Average Score",
            color="Grade",
            color_discrete_map={"Fail": "#e74c3c", "Needs Improvement": "#f39c12", "Pass": "#2ecc71"},
            title="Average Scores by Student",
            labels={"Average Score": "Score", "Name": "Student"}
        )
        fig_avg.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Fail Threshold")
        fig_avg.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Pass Threshold")
        fig_avg.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_avg, use_container_width=True)

    with col2:
        # Pie chart: Grade distribution
        grade_counts = df["Grade"].value_counts()
        fig_pie = px.pie(
            values=grade_counts.values,
            names=grade_counts.index,
            title="Grade Distribution",
            color_discrete_map={"Fail": "#e74c3c", "Needs Improvement": "#f39c12", "Pass": "#2ecc71"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # Student Performance Table
    def highlight_fail(row):
        return ['background-color: #ffcccc' if row["Status"] == "Failing" else '' for _ in row]

    st.subheader("📋 Student Performance Table")
    st.dataframe(df.style.apply(highlight_fail, axis=1), use_container_width=True)

# --- Student Details Page ---
elif page == "Student Details":
    st.title("👤 Individual Student Details")
    st.markdown("---")

    selected = st.selectbox("Select a student:", df["Name"].tolist())
    student = df[df["Name"] == selected].iloc[0]

    # Student Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Name", student["Name"])
    col2.metric("Average Score", f"{student['Average Score']:.2f}")
    col3.metric("Grade", student["Grade"])
    col4.metric("Status", student["Status"])

    st.markdown("---")

    # PDF Download
    pdf_data = generate_pdf(student)
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_data,
        file_name=f"{student['Name']}_Report.pdf",
        mime="application/pdf"
    )

    st.markdown("---")

    # Subject Scores Table
    subject_df = pd.DataFrame(
        [{"Subject": s, "Score": student[s]} for s in subjects]
    )
    st.subheader("📚 Subject-wise Scores")
    st.dataframe(subject_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Subject Scores Bar Chart with Thresholds
    fig_subject = px.bar(
        subject_df,
        x="Subject",
        y="Score",
        color="Score",
        color_continuous_scale="RdYlGn",
        title=f"Subject Performance for {selected}",
        labels={"Score": "Score", "Subject": "Subject"}
    )
    fig_subject.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Fail (40)")
    fig_subject.add_hline(y=70, line_dash="dash", line_color="green", annotation_text="Pass (70)")
    fig_subject.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_subject, use_container_width=True)

# --- Analytics Page ---
elif page == "Analytics":
    st.title("📈 Class Analytics")
    st.markdown("---")

    # Subject-wise Average
    st.subheader("📊 Subject-wise Class Average")
    subject_avg_df = pd.DataFrame(
        [{"Subject": s, "Average Score": df[s].mean()} for s in subjects]
    ).sort_values("Average Score", ascending=False)

    fig_subject = px.bar(
        subject_avg_df,
        x="Subject",
        y="Average Score",
        color="Average Score",
        color_continuous_scale="Viridis",
        title="Class Average by Subject"
    )
    fig_subject.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Target (50)")
    fig_subject.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_subject, use_container_width=True)

    st.markdown("---")

    # Score Distribution
    st.subheader("📊 Score Distribution Analysis")
    col1, col2 = st.columns(2)

    with col1:
        # Histogram
        fig_hist = px.histogram(
            df,
            x="Average Score",
            nbins=10,
            title="Distribution of Average Scores",
            labels={"Average Score": "Score", "count": "Number of Students"},
            color_discrete_sequence=["#3498db"]
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Box plot for all subjects
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

    st.markdown("---")

    # Performance Summary
    st.subheader("📊 Performance Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Highest Average", f"{df['Average Score'].max():.2f}")
    with col2:
        st.metric("Lowest Average", f"{df['Average Score'].min():.2f}")
    with col3:
        st.metric("Median Average", f"{df['Average Score'].median():.2f}")

    st.markdown("---")

    # Grade Distribution Table
    st.subheader("📋 Grade Distribution")
    grade_dist = df["Grade"].value_counts().reset_index()
    grade_dist.columns = ["Grade", "Count"]
    st.dataframe(grade_dist, use_container_width=True, hide_index=True)

# --- Download Data Page ---
elif page == "Download Data":
    st.title("📥 Download Data")
    st.markdown("---")

    # CSV Download
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="student_performance.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # Data Summary
    st.subheader("📊 Data Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(df))
    col2.metric("Total Subjects", len(subjects))
    col3.metric("Passing Students", len(df[df["Status"] == "Passing"]))
    col4.metric("Failing Students", len(df[df["Status"] == "Failing"]))

    st.markdown("---")

    # Full Dataset
    st.subheader("📋 Full Dataset")
    st.dataframe(df, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Student Performance Tracker | School Project 2026 | Developed by Rasheed & Ammar</p>", unsafe_allow_html=True)
