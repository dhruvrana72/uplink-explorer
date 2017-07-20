FROM ubuntu

WORKDIR /bexplorer
USER root

RUN apt-get update && apt-get -y -q install \
python-pip \
python-dev build-essential \
python-software-properties \
software-properties-common \
libssl-dev \
libffi-dev \
openssl \ 
git

# Assure github is a recognized ssh hostname
RUN mkdir -p /root/.ssh
RUN ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts

# Copy a local ssh public key to the docker image
COPY id_rsa /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa

# Python requirements
ADD ./requirements.txt /bexplorer/requirements.txt
RUN pip install -r requirements.txt 
ADD . /bexplorer

# Remove the public ssh key from the docker image
RUN rm /root/.ssh/id_rsa

EXPOSE 5000
EXPOSE 8545
CMD ["./runner-gcloud"] 
