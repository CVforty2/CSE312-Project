FROM python:3.9.5

ADD . /todo
WORKDIR /todo

COPY . .

# Download dependancies
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD python3 app.py