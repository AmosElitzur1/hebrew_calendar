import streamlit as st
from imports.calendar_functions import *
from imports.html import page_layout

def main():
  st.set_page_config(
    page_title="ימים ותאריכים",
    page_icon="🌞",
  )
  st.markdown(page_layout, unsafe_allow_html=True)
  st.title("לוח עברי")
  st.header("בחר תאריך עברי וראה באלו ימים בשבוע הוא יכול לחול")
  day = st.selectbox("בחר יום",days_list)
  month = st.selectbox("בחר חודש", months)
  date = hebrew_date(days_list.index(day), month)
  if date.validation() == 0:
    st.subheader(f"{day} {month} יכול לחול בימים {', '.join(date.possible_days())}")
  else:
    st.subheader(f'בחודש {month} יש רק 29 ימים')
  
  st.markdown("")
  st.page_link("home_page.py", label="חזרה לדף הבית",icon="🏠")
  st.markdown("")
  st.markdown("כל הזכויות שמורות לעמוס אליצור")

if __name__ == "__main__":
  main()    

