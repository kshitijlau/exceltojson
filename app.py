import streamlit as st
import pandas as pd
import json
from io import BytesIO, ZipFile

st.set_page_config(page_title="Multi-Language JSON Generator", layout="centered")
st.title("📄 Excel to Multi-Language JSON Generator")

uploaded_file = st.file_uploader("Upload Excel file with columns: id, english, german, ...", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Ensure 'id' column exists
        if 'id' not in df.columns:
            st.error("Missing required column: 'id'")
        else:
            lang_columns = [col for col in df.columns if col != 'id']
            if not lang_columns:
                st.error("No language columns found. Please include at least one language like 'english', 'german'.")
            else:
                zip_buffer = BytesIO()
                with ZipFile(zip_buffer, 'w') as zip_file:
                    for lang in lang_columns:
                        lang_dict = {
                            row['id']: row[lang]
                            for _, row in df.iterrows()
                            if pd.notnull(row['id']) and pd.notnull(row[lang])
                        }
                        json_bytes = json.dumps(lang_dict, ensure_ascii=False, indent=4).encode('utf-8')
                        zip_file.writestr(f"{lang[:2].lower()}.json", json_bytes)

                st.success("✅ JSON files created successfully!")

                st.download_button(
                    label="📥 Download ZIP with JSON files",
                    data=zip_buffer.getvalue(),
                    file_name="localized_jsons.zip",
                    mime="application/zip"
                )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
