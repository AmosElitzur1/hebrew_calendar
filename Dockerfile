FROM python:3.9.17
RUN pip install streamlit
COPY . .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "home_page.py", "--server.address=0.0.0.0"] 
