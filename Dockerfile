FROM python:3.9.5

ADD . /todo
WORKDIR /todo

COPY . .

# Download dependancies
RUN pip3 install -r requirements.txt

EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python3 app.py