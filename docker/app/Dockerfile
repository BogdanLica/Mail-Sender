FROM python:3-slim


WORKDIR /usr/src/app

COPY *.py ./

#COPY docker/attachments ./

COPY requirements.txt ./
#COPY servers.txt ./

RUN pip install -r requirements.txt && mkdir files

#EXPOSE 3001

CMD [ "python", "main.py" ]