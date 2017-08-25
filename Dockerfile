FROM python:2.7-alpine

WORKDIR /usr/src/app
RUN apk add --update git openssh gcc musl-dev libffi-dev openssl-dev


# since image we push to the registry is squashed, our keys stay secret
RUN mkdir -p ~/.ssh

RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD pytest -s -vv /usr/src/app/tests/ && pytest -s -vv /usr/src/app/tests/ && ENV=PROD gunicorn app:app -b 0.0.0.0:80 --workers=5 -k gevent
