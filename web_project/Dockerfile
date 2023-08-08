FROM python:3.10

# set a directory for the app
WORKDIR /home/yotam/Desktop/docker/ferari_docker/web_project/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# run the application with MySQL
CMD [ "python3", "app.py" ]
