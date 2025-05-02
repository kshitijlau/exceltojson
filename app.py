import streamlit as st
import pandas as pd
import json
from io import BytesIO

st.set_page_config(page_title="JSON to Excel Converter", layout="wide")
st.title("🔄 JSON to Excel Converter for Translator Review")

uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

if uploaded_file:
    try:
        json_data = json.load(uploaded_file)

        if isinstance(json_data, dict):
            df = pd.DataFrame(list(json_data.items()), columns=["Key", "Original String"])
            df["Translator Feedback"] = ""  # empty column for translators to fill

            st.subheader("📋 Preview of Converted Data")
            st.dataframe(df.head(10))

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Strings")
            output.seek(0)

            st.download_button(
                label="📥 Download Excel for Translation Review",
                data=output,
                file_name="translated_strings_review.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Uploaded JSON is not a flat key-value dictionary.")

    except Exception as e:
        st.error(f"Error parsing JSON file: {e}")
