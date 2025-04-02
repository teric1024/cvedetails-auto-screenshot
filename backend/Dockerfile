FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

WORKDIR /code/app

# Reference: https://medium.com/@hao66bmbm/docker-%E5%BB%BA%E7%BD%AE%E6%89%93%E5%8C%85-python-selenium-chromedriver-chrome-f74387266131
RUN apt-get update
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

CMD ["uvicorn", "api:app", "--log-level", "debug", "--host", "0.0.0.0", "--reload" ]