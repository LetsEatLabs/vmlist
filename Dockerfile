FROM ubuntu:latest

# Update the system
RUN apt update && apt install -y python3 python3-pip

#Change working directory
RUN mkdir /opt/app/
COPY requirements.txt /opt/app
WORKDIR /opt/app/

RUN python3 -m pip install -r requirements.txt

CMD ["gunicorn", "--bind=0.0.0.0:8000", "vmlist:app"]