import streamlit as st
st.set_page_config(page_title="Lab Manager")

Lab_01 = st.Page("Lab_01.py", title="Lab_01")
Lab_02 = st.Page("Lab_02.py", title="Lab_02")
Lab_03 = st.Page("Lab_03.py", title="Lab_03")
Lab_04 = st.Page("Lab_04.py", title="Lab_04")
Lab_05 = st.Page("Lab_05.py", title="Lab_05")
LabLangChain = st.Page("LabLangChain.py", title="LabLangChain")
LabMultimodal = st.Page("LabMultimodal.py", title="LabMultimodal")
Lab9 = st.Page("Lab9.py", title="Lab9", default=True)


pg = st.navigation([Lab_01, Lab_02, Lab_03, Lab_04, Lab_05, LabLangChain, LabMultimodal, Lab9])

pg.run()

