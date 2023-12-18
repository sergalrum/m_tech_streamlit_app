FROM python:3.10
WORKDIR /mtech
COPY . .
RUN pip install -r requirements.txt


COPY . /app
CMD ["streamlit", "run", "streamlit_app.py"]
EXPOSE 8501