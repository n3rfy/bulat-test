FROM python:3.11

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install gcc libc-dev g++ libffi-dev libxml2 libffi-dev libpq-dev unixodbc-dev -y

ARG USERNAME=app
ARG WDIR=/home/$USERNAME

WORKDIR $WDIR

COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONPATH=$WDIR

CMD ["python", "-m", "src.main"]
