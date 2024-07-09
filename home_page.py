import streamlit as st
from imports.calendar_functions import hebrew_today, format_hebrew_date
from imports.html import page_layout
from datetime import date

def main():
  st.set_page_config(
    page_title="אתר הלוח העברי",
    page_icon="✡️",
  )
  st.markdown(page_layout, unsafe_allow_html=True)
  st.title("לוח עברי")
  st.header("ברוכים הבאים לאתר הלוח העברי!")
  st.subheader(f"היום {format_hebrew_date(hebrew_today())}, {date.today().strftime('%d/%m/%Y')}")
  st.markdown("")
  st.page_link("pages/המרת_תאריך_עברי_ללועזי.py", label="המרת תאריך עברי ללועזי",icon="🗓️")
  st.page_link("pages/המרת_תאריך_לועזי_לעברי.py", label="המרת תאריך לועזי לעברי",icon="🌙")
  st.page_link("pages/באיזה_ימים_בשבוע_יכול_לחול_כל_תאריך_עברי.py", label="באיזה ימים בשבוע יכול לחול כל תאריך עברי",icon="🌞") 
  st.markdown("")
  st.markdown("כל הזכויות שמורות לעמוס אליצור")

if __name__ == "__main__":
  main()    

