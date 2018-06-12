#Install python library
FROM python:3.6.1-alpine

# Install app dependencies.
COPY ./requirements.txt .
COPY ./manolo.py .
COPY ./.env . 
RUN pip3 install -r requirements.txt

# Bundle app source.
CMD [ "python3", "./manolo.py" ]