import newscatcher
from mako.template import Template
from mako.lookup import TemplateLookup
from css_html_js_minify import css_minify, html_minify
from bs4 import BeautifulSoup
import boto3
import click
import os
import sys
import shutil
import subprocess
import tempfile
import fcntl
import yaml
import datetime

module_path = os.path.dirname(os.path.abspath(__file__))
templates = TemplateLookup(directories=[os.path.join(module_path,'templates')])
# Add user yarn directory to PATH
os.environ['PATH'] = f'{os.path.join(os.path.expanduser("~"),".yarn","bin")}:{os.environ["PATH"]}'

def gather_news(sites):
    news = {}
    for site in sites:
        news[site] = newscatcher.Newscatcher(site).get_news()
        for article in news[site]['articles']:
            article.summary = clean_html(article.get("summary", ""))
    return news

def make_html(news, title, date):
    template = templates.get_template('news.html')
    return template.render(news=news, title=title, date=date)

def purge_css(css_path, html_glob):
    if not shutil.which('purgecss'):
        raise AssertionError('purgecss command not found. Install via: `yarn global add purgecss`')
    out_path = tempfile.mkstemp('.css')[1]
    cmd = f'purgecss --css {css_path} --content {html_glob} --output {out_path}'
    if subprocess.call(cmd, shell=True) != 0:
        raise RuntimeError('purgecss did not run sucessfully')
    with open(out_path, 'r', encoding='utf-8') as f:
        return css_minify(f.read())

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for thing in soup(["script", "style", "img"]):
        thing.extract()
    return str(soup)

def put_s3(html, bucket, path="index.html"):
    s3_client = boto3.client("s3")
    s3_client.put_object(ACL="public-read", Body=html, ContentType="text/html", Bucket=bucket, Key=path)

def add_sites_to_db(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        conf = yaml.safe_load(f)
    for feed in conf['feeds']:
        newscatcher.add_url(feed['site'], feed['feed'],
                            topic=feed.get("topic", "news"),
                            language=feed.get("language", "en"),
                            country=feed.get("country", "US"),
                            main=feed.get("main", True))

def make_news(sites, output=None, title='"News"'):
    news = gather_news(sites)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    html = make_html(news, title, date)
    tmp_out = tempfile.mkstemp()[1]
    with open(tmp_out,'w') as f:
        f.write(html)
    css = purge_css(os.path.join(module_path, 'blunt.css'), tmp_out)
    html = html_minify(html.replace('<style id="blunt"></style>', f'<style>{css}</style>'))

    return html

@click.command()
@click.option("--title", help="Page title", metavar='TITLE', default='"News"')
@click.option("--upload-s3", help="Upload to S3 bucket index.html", metavar="BUCKET")
@click.option("--add-sites", help="Add sites from YAML file to database", metavar="YAML_FILE")
@click.option('-o', '--output', help='HTML file to create', default=None, metavar="HTML_FILE")
@click.argument("sites", nargs=-1)
def main(output, sites, add_sites, title, upload_s3):
    if add_sites:
        add_sites_to_db(add_sites)
    else:
        if len(sites) < 1:
            print("You must provide at least one news source as an argument")
            exit(1)
        if upload_s3 is not None:
            if 'AWS_ACCESS_KEY_ID' not in os.environ or 'AWS_SECRET_ACCESS_KEY' not in os.environ:
                print("In order to upload to S3, you must set environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
                exit(1)

        html = make_news(sites, title)

        # https://github.com/travis-ci/travis-ci/issues/4704#issuecomment-348435959
        flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL)
        fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags&~os.O_NONBLOCK)

        if output is None:
            print(html)
        else:
            with open(output,'w') as f:
                f.write(html)
        if upload_s3 is not None:
            put_s3(html, upload_s3)

if __name__ == '__main__':
    main()
