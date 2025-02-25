FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


#expose port 5000
EXPOSE 5000

COPY . .

CMD ["python", "app.py"]
