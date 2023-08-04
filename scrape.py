#!/usr/bin/env python3

import hashlib
import feedparser
from newspaper import Article

out = '/home/dustin/public_html/pocket/'

unreadFeed = feedparser.parse('http://getpocket.com/users/dustindikes/feed/unread')

indexHtml = '<!DOCTYPE html><html lang="en"><head><title>Pocket Articles</title></head><body><ul>'

for e in unreadFeed.entries:
    articleHtml = '<!DOCTYPE html><html lang="en"><head><title>'+e.title+'</title><style type="text/css">body{font-size:20px;}</style></head><body>'
    guid = hashlib.md5(e.id.encode()).hexdigest()
    indexHtml += '<li><a href="'+guid+'.html">'+e.title+'</a></li>'

    article = Article(e.link)
    try:
        article.download()
        article.parse()
    except BaseException:
        continue;

    articleHtml += '<h1>'+e.title+'</h1>'
    articleHtml += '<p><strong>Source: ' + e.link + '</strong></p><p>'

    articleHtml += article.text.replace('\n','<br>')

    articleHtml += '</p></body></html>'
    articleFile = open(out + guid + '.html', 'w')
    articleFile.write(articleHtml)
    articleFile.close()

indexHtml += '</ul></body></html>'

indexFile = open(out + 'index.html', 'w')
indexFile.write(indexHtml)
indexFile.close()
