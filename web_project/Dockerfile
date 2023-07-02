FROM python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# install Redis
RUN apt-get update && apt-get install -y redis-server

# define the port number the container should expose
EXPOSE 5000

# run Redis server
CMD redis-server --daemonize yes

# run the application
CMD [ "python3", "app.py" ]

