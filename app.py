import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title("📊 WhatsApp Report Card Generator")

# Upload mapping file
mapping_file = st.file_uploader("Upload Mapping File (Excel)", type=["xlsx"])
raw_data = st.text_area("Paste WhatsApp Messages Here")

def get_symbols(count):
    if count == 3:
        return "✔️✔️✔️"
    elif count == 2:
        return "✔️✔️"
    elif count == 1:
        return "✔️"
    else:
        return "✖️✖️✖️"

if mapping_file and raw_data:
    mapping_df = pd.read_excel(mapping_file)
    mapping_dict = dict(zip(mapping_df["Phone Number"], mapping_df["Name"]))
    tehsil_dict = dict(zip(mapping_df["Phone Number"], mapping_df["Tehsil"]))

    rows = []
    for line in raw_data.split("\n"):
        date_match = re.search(r"\[(\d{2}/\d{2})", line)
        phone_match = re.search(r"(\+91 \d+)", line)

        if date_match and phone_match:
            date = date_match.group(1)
            phone = phone_match.group(1)
            name = mapping_dict.get(phone, "Unknown")
            tehsil = tehsil_dict.get(phone, "Unknown")
            thumbs = line.count("👍")
            checks = line.count("✅")

            rows.append([date, tehsil, name, get_symbols(thumbs), get_symbols(checks)])

    df = pd.DataFrame(rows, columns=["Date", "Tehsil", "Name", "👍", "✅"])

    # Group by Tehsil
    for tehsil in df["Tehsil"].unique():
        st.subheader(f"📍 {tehsil}")
        st.dataframe(df[df["Tehsil"] == tehsil])

    # Download Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
    st.download_button("📥 Download Report", data=output.getvalue(), file_name="report.xlsx")
