# Hebrew Calendar

This is a Python project for a Hebrew calendar. The project uses the Streamlit module and offers a simple website with three functions: converting Hebrew dates to Gregorian dates, converting Gregorian dates to Hebrew dates, and selecting a Hebrew date to determine the day of the week it can fall on.

Additionally, the project includes a standalone Python module for Hebrew gematria. You can get the numeric value of a letter, word, or sentence, as well as get the value in letters for any number.

The project supports the Hebrew language and displays content from right to left.

The project can be run in two ways:

1. **Without Docker:**
   
  Run the following commands:
  ```bash
  pip install streamlit
  streamlit run home_page.py
  ```
  The project will be available in the browser at `localhost:8501`

2. **With Docker:**

  Run the following commands:
  ```bash
  docker build -t hebrew-calendar .
  docker run -p 80:8501 -d hebrew-calendar
  ```
  The project will be available in the browser at `localhost`
