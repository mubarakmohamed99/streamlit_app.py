# app.py
import streamlit as st
import pandas as pd
import base64
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# ---------------- Gmail Helpers ----------------

def gmail_authenticate():
    """Authenticate with Gmail API and return service object."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def get_unread_attachments(service, user_id="me"):
    """Fetch attachments from unread Gmail messages only."""
    results = service.users().messages().list(
        userId=user_id,
        q="has:attachment is:unread",
        maxResults=10
    ).execute()
    messages = results.get("messages", [])
    attachments = []

    for msg in messages:
        msg_data = service.users().messages().get(userId=user_id, id=msg["id"]).execute()
        for part in msg_data["payload"].get("parts", []):
            if part.get("filename"):
                att_id = part["body"].get("attachmentId")
                if att_id:
                    att = service.users().messages().attachments().get(
                        userId=user_id, messageId=msg["id"], id=att_id
                    ).execute()
                    data = base64.urlsafe_b64decode(att["data"].encode("UTF-8"))
                    attachments.append({"filename": part["filename"], "data": data})

        # ✅ Mark the email as read after processing
        service.users().messages().modify(
            userId=user_id,
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    return attachments

# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="Reinsurance Claims Processing Dashboard", layout="wide")

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
    st.write("Upload or fetch documents (Bordereaux, Account Statements, Cash Calls, Treaty Slips).")

    uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Uploaded: {file.name}")
        st.info("⚡ Document classification and extraction in progress... (placeholder)")

    st.subheader("📧 Retrieve New Gmail Attachments")
    if st.button("Fetch Gmail Attachments"):
        try:
            service = gmail_authenticate()
            attachments = get_unread_attachments(service)
            if attachments:
                for att in attachments:
                    st.success(f"Downloaded: {att['filename']}")
                    st.download_button(f"⬇️ Download {att['filename']}", att["data"], file_name=att["filename"])
            else:
                st.warning("No new unread attachments found in Gmail.")
        except Exception as e:
            st.error(f"Error: {e}")

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
        st.progress(0.7)
        st.success("Status: Ready for Booking")

# ---- Page 3: Exception Management ----
elif page == "🚨 Exception Management":
    st.title("🚨 Exception Management Agent")
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
    st.download_button("⬇️ Download Exception Report (PDF)", "Report content here", file_name="exception_report.pdf")
    st.download_button("⬇️ Download Booking Ready Report (Excel)", "Excel content here", file_name="booking_report.xlsx")
    st.subheader("Cross Validation Summary")
    st.metric("Matches", 45)
    st.metric("Mismatches", 2)
