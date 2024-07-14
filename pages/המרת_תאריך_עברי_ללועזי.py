import streamlit as st
from datetime import date
from imports.calendar_functions import *
from imports.gimatria import number_to_hebrew, hebrew_year_to_number
from imports.html import page_layout

def main():
  st.set_page_config(
    page_title="המרת תאריך עברי ללועזי",
    page_icon="🗓️",
  )
  st.markdown(page_layout, unsafe_allow_html=True)
  st.title("לוח עברי")
  st.header("בחר תאריך עברי כדי להמיר אותו לתאריך לועזי")
  heb_year = st.text_input("הקלד שנה עברית")
  year = hebrew_year_to_number(heb_year,deafault_value=hebrew_today().year)
  month = st.selectbox("בחר חודש", year_months[type_year(year)][1:])        
  heb_day = st.selectbox("בחר יום",days_list[0:days_heb_month(year_months[type_year(year)].index(month),year)])
  day = days_list.index(heb_day)
  if year >= zero_point["Hebrew"][0]:
    st.subheader(f" התאריך הלועזי של  {heb_day} {month} {number_to_hebrew(year)} הוא {get_calendar_date(day+1,month,year).strftime('%d/%m/%Y')}")
  else:
    st.subheader(f"אי אפשר לבחור תאריך לפני {format_hebrew_date(zero_point['Hebrew'])}, {zero_point['Calendar'].strftime('%d/%m/000%Y')}")
  
  st.markdown("")
  st.page_link("home_page.py", label="חזרה לדף הבית",icon="🏠")
  st.markdown("")
  st.markdown("כל הזכויות שמורות לעמוס אליצור")

if __name__ == "__main__":
  main()    



