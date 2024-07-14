import streamlit as st
from datetime import date
from imports.calendar_functions import *
from imports.html import page_layout

def main():
  st.set_page_config(
    page_title="המרת תאריך לועזי לעברי",
    page_icon="🌙",
  )
  st.markdown(page_layout, unsafe_allow_html=True)
  st.title("לוח עברי")
  st.header("בחר תאריך לועזי כדי להמיר אותו לתאריך עברי")
  mydate = st.date_input("לחץ כדי לבחור תאריך")
  year = mydate.year
  month = mydate.month
  day = mydate.day
  if st.checkbox("לבחירת תאריכים נוספים"):
    year = int(st.selectbox("בחר שנה לועזית", range(1,10000), index=2023))
    month = int(st.selectbox("בחר חודש", range(1,13)))        
    day = int(st.selectbox("בחר יום",range(1,days_month(month,year)+1)))
  hebrew_date = get_hebrew_date(date(year,month,day))
  if date(year,month,day) >= zero_point["Calendar"]:
    st.subheader(f" התאריך העברי של  {day}/{month}/{year} הוא {hebrew_date}")
  else:
    st.subheader(f"אי אפשר לבחור תאריך לפני {format_hebrew_date(zero_point['Hebrew'])}, {zero_point['Calendar'].strftime('%d/%m/000%Y')}")
  
  st.markdown("")
  st.page_link("home_page.py", label="חזרה לדף הבית",icon="🏠")
  st.markdown("")
  st.markdown("כל הזכויות שמורות לעמוס אליצור")


if __name__ == "__main__":
  main()    
