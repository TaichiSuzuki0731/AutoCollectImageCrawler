FROM joyzoursky/python-chromedriver:3.7-selenium
RUN set -x && \
  apt-get update && \
  apt-get install -y vim && \
  apt-get install tree && \
  pip install --upgrade pip && \
  pip install pipenv && \
  pip install icrawler && \
  pip install Pillow