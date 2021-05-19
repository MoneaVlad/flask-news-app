FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY news_app news_app
COPY run.py run.py

EXPOSE 5000

CMD [ "python3", "run.py"]