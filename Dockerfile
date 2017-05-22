FROM ubuntu

RUN apt-get update && apt-get -y -q install \
python-pip \
python-dev build-essential \
python-software-properties \
software-properties-common \
libssl-dev \
libffi-dev \
openssl \ 
git

USER root
COPY . /bexplorer
WORKDIR /bexplorer

# Assure github is a recognized ssh hostname
RUN mkdir -p /root/.ssh
RUN ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts

# Copy a local ssh public key to the docker image
COPY id_rsa /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa

# Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --src /usr/local/src

# Remove the public ssh key from the docker image
RUN rm /root/.ssh/id_rsa

EXPOSE 5000
EXPOSE 8545
CMD ["./runner"] --port 5000
