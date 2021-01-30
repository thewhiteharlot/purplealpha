FROM kenhv/kensurbot:alpine

RUN git clone -b purplealpha https://github.com/thewhiteharlot/purplealpha /root/userbot
RUN chmod 777 /root/userbot
WORKDIR /root/userbot

RUN pip3 install  -r https://raw.githubusercontent.com/thewhiteharlot/purplealpha/purplealpha/requirements.txt --upgrade pip

EXPOSE 80 443

CMD ["python3","-m","userbot"]