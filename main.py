import streamlit as st

import streamlit as st
import pandas as pd
import re
from data_extractor import extract

st.set_page_config(
    page_title="Skills & Experience Extractor",
    layout="centered"
)

st.title("Skills & Experience Extractor")
st.caption("Extract structured skills and experience from Job Descriptions or CVs")

# Text input
input_text = st.text_area(
    "Paste Job Posting or CV text below:",
    height=300,
    placeholder="Enter or paste text here..."
)

# Button
if st.button("Extract"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Extracting information..."):
            try:
                result = extract((input_text))

                st.subheader("Document Type")
                st.write(result.get("document_type", "Not available"))

                st.subheader("Experience Summary")
                st.write(result.get("experience_summary", "Not available"))

                # Experience Years
                st.subheader("Years of Experience")
                st.write(result.get("experience_years"))

                # Skills Table
                skills = result.get("skills", [])
                if skills:
                    st.subheader("Skills")
                    skills_df = pd.DataFrame({"Skill": skills})
                    st.dataframe(skills_df, use_container_width=True)

                # Tools & Technologies Table
                tools = result.get("tools_technologies", [])
                if tools:
                    st.subheader("Tools & Technologies")
                    tools_df = pd.DataFrame({"Tool / Technology": tools})
                    st.dataframe(tools_df, use_container_width=True)

            except Exception as e:
                st.error(str(e))



