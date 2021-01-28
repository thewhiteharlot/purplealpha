FROM sahyam/docker:groovy

#
# Clone repo and prepare working directory
#
RUN git clone -b purplealpha https://github.com/thewhiteharlot/purplealpha /root/userbot
RUN mkdir /root/userbot/.bin
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install  -r https://raw.githubusercontent.com/thewhiteharlot/purplealpha/purplealpha/requirements.txt --upgrade pip

CMD ["python3","-m","userbot"]