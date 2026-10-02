# Automated Data Analysis & File Processing Platform

## 📌 Project Overview
This project is an automated, user-friendly data analysis web utility built with Python. Handling raw data files manually can be time-consuming and prone to errors. This application solves that problem by allowing users to upload datasets (such as CSV or Excel files) and automatically auditing them for quality issues. The system scans the data instantly to detect data hygiene anomalies, specifically tracking down missing values and duplicate rows.

## ⚙️ Core Functionalities
The application automates the essential first steps of any data science pipeline:

1. **File Upload Interface:** A clean web front-end that accepts user-uploaded data sheets.
2. **Automated Missing Value Detection:** Scans every column in the dataset to calculate and pinpoint empty or `null` entries.
3. **Duplicate Row Audit:** Identifies identical duplicate entries across rows that could skew analytical results.
4. **Data Cleanliness Report:** Generates an immediate visual summary of the dataset's overall health and quality status.

---

## 🛠️ Tech Stack & Architecture
- **Backend & Logic:** Python 3.x
- **Data Manipulation:** Pandas (For structure auditing and vectorization)
- **Deployment & Hosting:** GitHub

---

## 🚀 Future Roadmap & Enhancements
While the current version focuses on automated data cleaning and structural auditing, future updates will include:
- Integrated statistical profiling (mean, median, mode, and standard deviation summaries).
- Automatic handling options (e.g., dropping or imputing missing rows at the click of a button).
- Interactive data visualization charts using Python plotting libraries.
