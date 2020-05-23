# "News"

This is a minimal self-hosted news aggregator that produces a single static HTML
page. You can run it on a cron job and host it on any webserver. 

News sources are aggregated by their RSS feeds contained in the included
[newscatcher database](https://github.com/kotartemiy/newscatcher/). Minimal
responsive layout designed with [Blunt.css](https://github.com/f-prime/Blunt/)
and pruned with [PurgeCSS](https://purgecss.com/)

## Quickstart

Run the pre-built docker image with any number of news sites as individual arguments:

```
docker run --rm enigmacurry/news news.ycombinator.com ap.org reuters.com foxnews.com > news.html
```

The html is printed to STDOUT, which in this example, is redirected to the file
called `news.html`.

## Adding your own news sources

The included [newscatcher database](https://github.com/kotartemiy/newscatcher/)
contains several thousand websites and RSS feeds. This lets you simply specify
the domain name alone, rather than needing to specify the full RSS feed URL. If
you have news sources that are not contained in this database, you can add the
RSS feeds to your own local database.

If you add your own news sources, you will need to build your own docker image
to include them. 

Clone this repository, then edit the file
[news.yaml](https://raw.githubusercontent.com/EnigmaCurry/news/master/news.yaml)
and write your own sources following the format of the included examples.

Next build the docker image in the same directory:

```
docker build -t news .
```

Now test running your own image and include your own domains:

```
docker run --rm news news.ycombinator.com ap.org reuters.com foxnews.com > news.html
```

## Run without docker

Docker is not a hard requirement, it is simply for convenience. If you rather
install this as a regular python package, you can!

```
pip install https://github.com/EnigmaCurry/news/archive/master.zip
```

You will also need [nodejs](https://nodejs.org/) and
[yarn](https://classic.yarnpkg.com/en/docs/install) installed. This is so that
you can install `purgecss`:

```
yarn global add purgecss
```

Now you can run the `news` executable:

```
news news.ycombinator.com ap.org reuters.com foxnews.com > news.html
```

You can also add your own sources to the database like so (you will need to save
[news.yaml](https://raw.githubusercontent.com/EnigmaCurry/news/master/news.yaml)
someplace and edit it first):

```
news --add-sites news.yaml
```
