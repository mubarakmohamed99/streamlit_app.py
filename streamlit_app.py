# app.py
import streamlit as st
import os, json
from process_claim import load_config, llm_extract, evaluate_rules, retrieve_support
from decide_and_report import make_decision, save_report
from ingest import ingest_folder, load_text

cfg = load_config()

st.title("🛡️ Reinsurance Claim Decision Assistant")

# Upload insurer docs
with st.expander("📑 Upload Insurer Documents (Policies, Laws, Rules)"):
    files = st.file_uploader("Upload PDF/DOCX/TXT", accept_multiple_files=True)
    if st.button("Ingest Docs"):
        for f in files:
            path = os.path.join("uploads/policies", f.name)
            os.makedirs("uploads/policies", exist_ok=True)
            with open(path, "wb") as out: out.write(f.getbuffer())
        ingest_folder(cfg, "uploads/policies")
        st.success("Documents ingested into vector DB!")

# Upload claim file
claim_file = st.file_uploader("📂 Upload Claim Document", type=["txt","pdf","docx"])
if claim_file and st.button("Process Claim"):
    path = os.path.join("uploads/claims", claim_file.name)
    os.makedirs("uploads/claims", exist_ok=True)
    with open(path, "wb") as out: out.write(claim_file.getbuffer())
    claim_text = load_text(path)

    # Process
    claim_fields = llm_extract(cfg, claim_text)
    triggered = evaluate_rules(claim_fields, cfg.get("rules_file"))
    retrieved = retrieve_support(cfg, claim_fields)

    # Decision
    record = {"claim_fields": claim_fields, "triggered_rules": triggered, "retrieved": retrieved}
    decision = make_decision(cfg, record)
    save_report(cfg, record, decision)

    # Show results
    st.subheader("Claim Details")
    st.json(claim_fields)

    st.subheader("Triggered Rules")
    st.json(triggered)

    st.subheader("Relevant Policy/Law Passages")
    for r in retrieved:
        st.markdown(f"**{r['citation']}**: {r['text'][:300]}...")

    st.subheader("Decision")
    st.json(decision)
