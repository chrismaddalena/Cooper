#Use the Python 2.7 image
FROM python:2.7.10
MAINTAINER Chris Maddalena <chris.maddalena@gmail.com>
#Move to root and clone the Cooper repo
WORKDIR /root
RUN git clone https://github.com/chrismaddalena/Cooper.git
#Move into the Cooper folder and install dependencies
WORKDIR /root/Cooper/setup
RUN pip install -r requirements.txt
WORKDIR /root/Cooper
