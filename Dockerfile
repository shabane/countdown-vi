FROM ubuntu:latest
RUN apt-get update && apt-get install python3 python3-pip -y
COPY . /var/code
RUN pip3 install -r /var/code/r.txt
WORKDIR /var/code
CMD [ "/bin/python3", "main.py" ]