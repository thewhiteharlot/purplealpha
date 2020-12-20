FROM movecrew/one4ubot:alpine-latest

RUN git clone https://github.com/thewhiteharlot/PurpleBot -b sql-extended /One4uBot
RUN chmod 777 /One4uBot
ENV PATH="/One4uBot/bin:$PATH"
WORKDIR /One4uBot


COPY ./sample_config.env ./userbot.session* ./config.env* /One4uBot/

EXPOSE 80 443

CMD ["python3","-m","userbot"]
