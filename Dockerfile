#Install python library
FROM python:3.6.1-alpine

# Install app dependencies.
COPY ./requirements.txt .
COPY ./manolo.py .
RUN pip3 install -r requirements.txt

#Copy de env token
ARG SLACK_TOKEN
ENV SLACK_TOKEN=$SLACK_TOKEN

# Bundle app source.
RUN printenv
CMD [ "python3", "./manolo.py" ]