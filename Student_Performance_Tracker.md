# Student Performance Tracker

## Project Overview

This project provides an interactive web application built with Streamlit to track and analyze student academic performance. It allows for easy visualization of individual student scores, class-wide analytics, and overall performance metrics. The application is designed to be user-friendly and presentable, making it ideal for educational settings or personal tracking.

## Features

- **Interactive Dashboard**: Displays key performance indicators such as total students, passing students, students needing improvement, and class average. It also includes visual summaries of average scores and passing status distribution.

- **Individual Student Details**: Allows users to select a specific student and view their subject-wise scores, average score, and passing status. A dedicated bar chart visualizes their performance across subjects.

- **Class Analytics**: Provides insights into overall class performance, including subject-wise average scores and score distribution histograms, and box plots.

- **Data Download**: Enables users to download the complete student performance data as a CSV file directly from the application.

- **Dynamic Data Handling**: Processes raw student score data to calculate average scores and determine passing status based on predefined criteria.

## Technologies Used

- **Python**: The core programming language.

- **Pandas**: Used for data manipulation and analysis, creating DataFrames.

- **Streamlit**: For building the interactive web application and user interface.

- **Plotly Express**: For generating interactive and visually appealing charts and graphs.

## Setup and Installation

To run this project locally, follow these steps:

1. **Prerequisites**:Ensure you have Python 3.7 or higher installed on your system.

1. **Clone the Repository (or save the file)**:If you have the `student_performance.py` file, save it to your desired project directory.

1. **Install Dependencies**:Open your terminal or command prompt, navigate to your project directory, and install the required Python libraries using pip:

   ```bash
   pip install streamlit pandas plotly
   ```

## How to Run the Application

Once the dependencies are installed, you can run the Streamlit application:

1. **Navigate to the Project Directory**:Open your terminal or command prompt and change to the directory where you saved `student_performance.py`.

1. **Execute the Streamlit Command**:Run the application using the Streamlit CLI:

   ```bash
   streamlit run student_performance.py
   ```

1. **Access the Application**:Streamlit will automatically open a new tab in your default web browser, displaying the application. If it doesn't, you can manually navigate to `http://localhost:8501` (or the address provided in your terminal ).

## Data Structure and Logic

The application uses an embedded dataset of 10 students, each with scores across seven subjects: English, Informatics Practices, Accountancy, Business Studies, Economics, Physical Education, and Islamic Education.

- **Average Score**: Calculated as the mean of all subject scores for each student.

- **Passing Status**: A student is considered "Passing" if they score 40 or above in *all* subjects. If any subject score is below 40, their status is "Needs Improvement."

## Author
Rasheed & Ammar

