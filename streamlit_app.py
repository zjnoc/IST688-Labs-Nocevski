import streamlit as st

Lab_01 = st.Page("Lab_01.py", title="Lab_01")
Lab_02 = st.Page("Lab_02.py", title="Lab_02")
Lab_03 = st.Page("Lab_03.py", title="Lab_03")
Lab_04 = st.Page("Lab_04.py", title="Lab_04", default=True)

pg = st.navigation([Lab_01, Lab_02, Lab_03, Lab_04])

st.set_page_config(page_title="Lab Manager")


pg.run()