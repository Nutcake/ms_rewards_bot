FROM python:3.9 AS msrewards
# set environment
ENV VIRTUAL_ENV=/opt/venv
ENV TZ="Europe/Berlin"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV DISPLAY=:99

# install python deps
RUN python3 -m venv $VIRTUAL_ENV
ADD poetry.lock .
ADD pyproject.toml .
RUN pip install poetry
RUN poetry install

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable iproute2 unzip xvfb

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /bin/

ADD /src/main.py .

CMD ["python3", "main.py"]
