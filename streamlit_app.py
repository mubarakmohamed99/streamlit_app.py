# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reinsurance Claims Processing Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "📥 Document Ingestion",
    "🧮 Validation & Reconciliation",
    "🚨 Exception Management",
    "📊 Reporting & SICS Integration"
])

# ---- Page 1: Document Ingestion ----
if page == "📥 Document Ingestion":
    st.title("📥 Document Ingestion Agent")
    st.write("Upload and classify documents (Bordereaux, Account Statements, Cash Calls, Treaty Slips).")

    uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Received: {file.name}")
        st.info("⚡ Document classification and extraction in progress... (placeholder)")

    # Example preview table
    st.subheader("Extracted Data Preview")
    sample_data = {
        "Claim_No": ["C001", "C002"],
        "Insured": ["ABC Ltd", "XYZ Ltd"],
        "DOL": ["2024-01-15", "2024-02-10"],
        "Gross": [100000, 75000]
    }
    st.dataframe(pd.DataFrame(sample_data))

# ---- Page 2: Validation & Reconciliation ----
elif page == "🧮 Validation & Reconciliation":
    st.title("🧮 Core Validation Agent")
    st.write("Results of 7 validation rules.")

    rules = [
        "Claims vs Surplus Reconciliation",
        "Premium Reconciliation",
        "Financial Formula Validation",
        "Date Range Validation",
        "Duplicate Detection",
        "Territory Validation",
        "Cross-System Validation"
    ]
    for r in rules:
        st.subheader(r)
        st.progress(0.7)  # placeholder
        st.success("Status: Ready for Booking")  # placeholder

# ---- Page 3: Exception Management ----
elif page == "🚨 Exception Management":
    st.title("🚨 Exception Management Agent")
    st.write("Handle critical, warning, and auto-resolve exceptions.")

    st.warning("2 critical exceptions detected: Premium variance, Duplicate recovery")
    st.info("1 warning exception: Territory mismatch")
    st.success("3 auto-resolved: Minor calculation differences")

    st.subheader("Exception Queue")
    st.table(pd.DataFrame({
        "Type": ["Premium Variance", "Duplicate Recovery", "Territory Mismatch"],
        "Severity": ["Critical", "Critical", "Warning"],
        "Status": ["Pending", "Pending", "In Review"]
    }))

# ---- Page 4: Reporting & SICS Integration ----
elif page == "📊 Reporting & SICS Integration":
    st.title("📊 Reporting & SICS Integration Agent")
    st.write("Generate exception reports, booking-ready summaries, and cross-validation results.")

    st.download_button("⬇️ Download Exception Report (PDF)", "Report content here", file_name="exception_report.pdf")
    st.download_button("⬇️ Download Booking Ready Report (Excel)", "Excel content here", file_name="booking_report.xlsx")

    st.subheader("Cross Validation Summary")
    st.metric("Matches", 45)
    st.metric("Mismatches", 2)
