FROM python:3.10

WORKDIR /postgres_to_es

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD python main.py