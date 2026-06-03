import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

plt.switch_backend('Agg')

st.set_page_config(page_title="Enterprise Data Analyst", page_icon="📊", layout="wide")

st.title("📊 Production-Grade Data Analytics Web App")
st.markdown("### Upload any CSV file for instant data profiling, automatic cleaning, and interactive charts.")
st.write("---")

uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    # 🧠 MEMORY MANAGEMENT: Data ko session state mein rakhna taaki cleaning save rahe
    if "df" not in st.session_state or st.session_state.get("current_file") != uploaded_file.name:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.current_file = uploaded_file.name

    df = st.session_state.df

    if uploaded_file.size > 50 * 1024 * 1024:
        st.error("File size too large! Please upload a file smaller than 50MB.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👀 Data Preview (Top 5 Rows)")
            st.dataframe(df.head())
            
            st.subheader("🔢 Data Shape & Structure")
            st.write(f"**Total Records (Rows):** {df.shape[0]}")
            st.write(f"**Total Attributes (Columns):** {df.shape[1]}")
            
        with col2:
            st.subheader("⚠️ Missing Values Summary")
            missing_data = df.isnull().sum()
            total_missing = missing_data.sum()
            missing_df = pd.DataFrame({'Column Name': missing_data.index, 'Missing Values': missing_data.values})
            st.dataframe(missing_df[missing_df['Missing Values'] > 0])

        st.write("---")
        
        # SMART DATA CLEANING SECTION (WORKING WITH MEMORY)
        st.subheader("🛠️ Smart Data Cleaning & Export")
        
        total_duplicates = df.duplicated().sum()
        col_clean1, col_clean2 = st.columns(2)
        
        with col_clean1:
            st.markdown("#### 🔍 Duplicates Analysis")
            if total_duplicates > 0:
                st.warning(f"Total **{total_duplicates}** duplicate rows are present in the dataset.")
                if st.button("🗑️ Remove Duplicate Rows"):
                    # Memory ke andar se duplicates drop karna
                    st.session_state.df = df.drop_duplicates()
                    st.success("Duplicates successfully removed!")
                    st.rerun()
            else:
                st.success("Congratulations! this dataset has no duplicate rows.")
                
        with col_clean2:
            st.markdown("#### 🧼 Missing Values Analysis")
            if total_missing > 0:
                st.warning(f"Total **{total_missing}** missing values are present in the dataset.")
                if st.button("🧼 Auto-Clean Missing Values"):
                    # Memory ke andar missing values fill karna
                    for col in df.select_dtypes(include=['float64', 'int64']).columns:
                        df[col] = df[col].fillna(df[col].mean())
                    for col in df.select_dtypes(include=['object', 'category']).columns:
                        df[col] = df[col].fillna(df[col].mode()[0])
                    st.session_state.df = df
                    st.success("Missing values successfully filled!")
                    st.rerun()
            else:
                st.success("Congratulations! this dataset has no missing values.")
        
        st.write("")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        
        st.download_button(
            label="📥 Download Cleaned Dataset (CSV)",
            data=csv_bytes,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

        st.write("---")
        
        st.subheader("💡 Statistical Analysis")
        st.dataframe(df.describe())
        
        st.write("---")
        
        # ADVANCED MULTI-GRAPH ENGINE
        st.subheader("📈 Smart Analytics Chart Engine")
        
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        available_charts = []
        if len(numerical_cols) > 0:
            available_charts.append("Histogram (Distribution)")
            available_charts.append("Box Plot (Outliers Check)")
        if len(numerical_cols) >= 2:
            available_charts.append("Scatter Plot (Relationship)")
        if len(categorical_cols) > 0 and len(numerical_cols) > 0:
            available_charts.append("Bar Plot (Category vs Value)")
            
        if available_charts:
            chart_type = st.selectbox("Select Chart Type You Want to Visualize:", available_charts)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            
            if chart_type == "Histogram (Distribution)":
                selected_col = st.selectbox("Select column for Histogram:", numerical_cols, key="histo")
                sns.histplot(df[selected_col], kde=True, ax=ax, color="skyblue")
                plt.title(f"Distribution of {selected_col}")
                
            elif chart_type == "Box Plot (Outliers Check)":
                selected_col = st.selectbox("Select column for Box Plot:", numerical_cols, key="box")
                sns.boxplot(x=df[selected_col], ax=ax, color="lightgreen")
                plt.title(f"Outlier Analysis of {selected_col}")
                
            elif chart_type == "Scatter Plot (Relationship)":
                col_x = st.selectbox("Select X-Axis Variable:", numerical_cols, key="x_axis")
                col_y = st.selectbox("Select Y-Axis Variable:", numerical_cols, key="y_axis")
                sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax, color="salmon")
                plt.title(f"Correlation between {col_x} and {col_y}")
                
            elif chart_type == "Bar Plot (Category vs Value)":
                col_x = st.selectbox("Select Categorical Column (X-Axis):", categorical_cols, key="bar_x")
                col_y = st.selectbox("Select Numerical Column (Y-Axis):", numerical_cols, key="bar_y")
                sns.barplot(data=df, x=col_x, y=col_y, ax=ax, palette="viridis", errorbar=None)
                plt.title(f"Analysis of {col_y} across different {col_x}")
            
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.warning("This dataset doesn't have suitable columns for automatic visualization.")

st.sidebar.markdown("### 🛠️ System Architecture")
st.sidebar.markdown("""
**Deploy Readiness:** `Production-Grade`  
**Core Framework:** `Python 3.11 + Streamlit`  
**Execution Pipeline:** `Memory-Optimized (Agg)`  
""")
st.sidebar.write("---")
st.sidebar.caption("Designed for automated exploratory data analysis and real-time business intelligence processing.")