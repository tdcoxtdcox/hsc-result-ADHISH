import streamlit as st
import pandas as pd

# --- PAGE SETTINGS ---
st.set_page_config(page_title="HSC RESULT 2025, CHITTAGONG", layout="wide", page_icon="🎓")

# --- LOAD DATA ---
info_df = pd.read_csv('info_cleaned.csv')
marks_df = pd.read_csv('all_colleges_marks_with_total.csv')

# --- HEADER ---
st.markdown("""
<div style='text-align:center'>
  <h1>HSC RESULT 2025, CHITTAGONG</h1>
  <h4>Created by Adhish Bhattacharjee</h4>
</div>
""", unsafe_allow_html=True)

st.write("---")

# --- SIDEBAR SEARCH ---
st.sidebar.header("Search Options")
search_by = st.sidebar.selectbox(
    "Search By",
    ["Name", "Father's Name", "Mother's Name", "ROLL", "Registration"]
)
search_input = st.sidebar.text_input(f"Enter {search_by}:")

# --- SEARCH FUNCTION ---
def search_data(df, column, value, exact=False):
    if exact:
        return df[df[column].astype(str) == str(value)]
    else:
        return df[df[column].astype(str).str.contains(value, case=False, na=False)]

# --- SEARCH LOGIC ---
if search_input:
    if search_by in ["ROLL", "Registration"]:
        result_df = search_data(info_df, search_by, search_input, exact=True)
    else:
        result_df = search_data(info_df, search_by, search_input, exact=False)

    if not result_df.empty:
        st.subheader("Search Results")
        st.dataframe(result_df, use_container_width=True)

        selected_roll = st.selectbox("Select a student by ROLL:", result_df['ROLL'])
        student_marks = marks_df[marks_df['ROLL'] == selected_roll]
        student_info = info_df[info_df['ROLL'] == selected_roll]

        st.markdown("### Student Details")
        st.table(student_info)

        st.markdown("### Marks")
        st.table(student_marks[['subject', 'Mark', 'Total_Mark']])
    else:
        st.warning("No results found.")

st.write("---")

# --- RANKINGS ---
st.subheader("Rankings by Total Marks")
tab1, tab2, tab3 = st.tabs(["Science", "Business", "Humanity"])

def show_ranking(group_name, tab):
    group_df = info_df[info_df['Group'].str.lower() == group_name.lower()]
    total_marks = marks_df.groupby('ROLL')['Total_Mark'].max().reset_index()
    group_df = group_df.merge(total_marks, on='ROLL', how='left')
    group_df = group_df.sort_values(by='Total_Mark', ascending=False)
    with tab:
        st.table(group_df)

show_ranking("Science", tab1)
show_ranking("Business", tab2)
show_ranking("Humanity", tab3)

# --- FOOTER ---
st.markdown("""
<div style='text-align:center;margin-top:50px'>
  <small>© 2025 HSC Result Portal, Chittagong. Developed by Adhish Bhattacharjee.</small>
</div>
""", unsafe_allow_html=True)
