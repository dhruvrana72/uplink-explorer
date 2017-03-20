FROM ubuntu
RUN apt-get update && apt-get -y -q install \
python-pip \
python-dev build-essential \
python-software-properties \
software-properties-common \
libssl-dev \
openssl

USER root
COPY . /bexplorer
WORKDIR /bexplorer

# Python requirements
COPY requirements.txt .

RUN pip install -r requirements.txt --src /usr/local/src

EXPOSE 5000
CMD ["python run.py server"] --port 5000