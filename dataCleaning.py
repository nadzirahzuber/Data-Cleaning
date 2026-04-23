import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Cleaning App", layout="wide")

st.title("🧹 Data Cleaning Application")

# File Upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Original Data")
    st.dataframe(df)

    # Missing Values
    st.subheader("🔍 Missing Values")
    missing = df.isnull().sum()
    st.write(missing)

    # Duplicate Records
    st.subheader("📋 Duplicate Records")
    duplicates = df.duplicated().sum()
    st.write(f"Total duplicate rows: {duplicates}")

    # -------------------------------
    # REMOVE MISSING VALUES
    # -------------------------------
    if st.button("🗑 Remove Missing Values"):
        df = df.dropna()
        st.success("Missing values removed!")

    # -------------------------------
    # HANDLE MISSING VALUES
    # -------------------------------
    st.subheader("⚙️ Handle Missing Values")

    column = st.selectbox("Select column", df.columns)

    method = st.selectbox(
        "Select method",
        ["Mean", "Median", "Mode", "Fill with Value"]
    )

    if st.button("Apply Handling"):
        if method == "Mean":
            df[column].fillna(df[column].mean(), inplace=True)
        elif method == "Median":
            df[column].fillna(df[column].median(), inplace=True)
        elif method == "Mode":
            df[column].fillna(df[column].mode()[0], inplace=True)
        elif method == "Fill with Value":
            value = st.text_input("Enter value")
            if value:
                df[column].fillna(value, inplace=True)

        st.success("Missing values handled!")

    # -------------------------------
    # REMOVE DUPLICATES
    # -------------------------------
    if st.button("🧹 Remove Duplicate Rows"):
        df = df.drop_duplicates()
        st.success("Duplicates removed!")

    # -------------------------------
    # SHOW CLEANED DATA
    # -------------------------------
    st.subheader("✅ Cleaned Data")
    st.dataframe(df)

    # -------------------------------
    # DOWNLOAD CLEANED FILE
    # -------------------------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )