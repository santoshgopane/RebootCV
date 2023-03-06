FROM python:3.9

RUN apt update
RUN apt install python3 -y

WORKDIR /usr/app/src

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python3","./src/app.py"]