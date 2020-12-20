FROM kenhv/kensurbot:alpine

RUN git clone -b purplealpha https://github.com/thewhiteharlot/purplealpha /root/userbot
RUN chmod 777 /root/userbot
WORKDIR /root/userbot/


COPY ./sample_config.env ./userbot.session* ./config.env* /One4uBot/

EXPOSE 80 443

CMD ["python3","-m","userbot"]
