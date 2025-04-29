import streamlit as st
import pandas as pd
import json
from io import BytesIO

st.set_page_config(page_title="Excel to Localized JSON", layout="centered")

st.title("📄 Excel to Localized JSON Converter")

uploaded_file = st.file_uploader("Upload Excel file with columns: id, english, german", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Check required columns
        required_cols = ['id', 'english', 'german']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Missing required columns. Found columns: {df.columns.tolist()}")
        else:
            # Convert to desired JSON structure
            result = {
                row['id']: {
                    "en": row['english'],
                    "de": row['german']
                }
                for _, row in df.iterrows()
                if pd.notnull(row['id']) and pd.notnull(row['english']) and pd.notnull(row['german'])
            }

            json_str = json.dumps(result, ensure_ascii=False, indent=4)
            json_bytes = BytesIO(json_str.encode('utf-8'))

            st.success("✅ JSON created successfully!")

            st.download_button(
                label="📥 Download localized_strings.json",
                data=json_bytes,
                file_name="localized_strings.json",
                mime="application/json"
            )

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
