FROM python:3.6

ENV USER_DIR="/root"

RUN apt-get update
RUN apt-get install -y awscli
RUN apt-get install -y curl && rm -rf /var/lib/apt/lists/*


RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -E  -
RUN apt-get install -y nodejs
RUN apt-get install -y build-essential

ADD . /workspace
WORKDIR /workspace

RUN npm install
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENTRYPOINT bash docker-entrypoint.sh