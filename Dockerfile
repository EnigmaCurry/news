FROM python:3
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt update && apt install -y yarn && \
    yarn global add purgecss
COPY . /dist
RUN pip install /dist && \
    news --add-sites /dist/news.yaml && \
    rm -rf /dist && \
    adduser news-guy --gecos GECOS --shell /bin/bash --disabled-password --home /home/news
USER news-guy
WORKDIR /home/news
ENTRYPOINT ["news"]
