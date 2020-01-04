FROM ubuntu

RUN apt-get update && \
	apt-get -y install sudo 

RUN sudo apt-get -y install python3-pip

WORKDIR /

RUN pip3 install grpcio grpcio-tools

COPY . /

ENTRYPOINT [ "python3" ]

CMD []