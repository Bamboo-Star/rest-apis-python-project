# specify the base image
FROM python:3.10
# port number to run command
EXPOSE 5000
# go into a folder within docker image
WORKDIR /app
# copy and run the requirements.txt into current folder in image
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# copy everything from current local folder, to the /app folder in image
COPY . .
# run the command as container
# allows an external client to request flask app running in container 
CMD [ "flask", "run", "--host", "0.0.0.0"]




# run docker in command line
# docker run -dp 5005:5000 rest-apis-flask-python
# 5005(local port):5000(port in the docker image)
# use local port between ":{local_port_#}/"in to access the apis in local

# use a volume to aviod rebuilding and rerunning docker container everytime
# -v creates a volume -w within the /app folder. 
# (pwd) current work directory
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest-apis-sql


# docker build -t rest-apis-sql .
# docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest-apis-sql



# each line above makes a layer, i.e., cached

# benefit of "COPY requirements.txt ." before "COPY . ."
# if the requirements.txt file does not change, would not run "RUN pip install..."
# if use "COPY . .", everytime any updates in local folder
#   the image would run "RUN pip install..." again