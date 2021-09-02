
#python base image in version 2.7
FROM python:2.7

LABEL maintainer="Juliana Fogg"

COPY ./techtrends /app

WORKDIR /app

#install packages defined in the requirements.txt file
RUN pip install -r requirements.txt

#database is initialized with the pre-defined posts in the init_db.py
RUN python ./init_db.py

#expose the application port 3111
ENV PORT 3111
EXPOSE ${PORT}

# command to run on container start
CMD [ "python3", "app.py" ]


