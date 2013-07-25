__author__ = 'Dietmar'

import HTMLParser
import re
import random
from feedparser.feedparser.feedparser import FeedParserDict

class ParsedFeedEntry():

    def __init__(self, parentFeed, feedparserEntry):
        html_parser = HTMLParser.HTMLParser()

        # published time stamp
        # Format: time.struct_time
        if 'published_parsed' in feedparserEntry.keys():
            self.published_parsed = feedparserEntry['published_parsed']
        else:
            self.published_parsed = ''

        # links
        # format: [{href, type, rel}]
        links = []
        linksImages = []
        if 'links' in feedparserEntry.keys():
            for link in feedparserEntry['links']:
                if link['rel'] == 'enclosure':
                    linksImages.append(link['href'])
                if link['rel'] == 'alternate':
                    links.append(link['href'])

        # standard link (spoken address)
        # format: string
        if 'link' in feedparserEntry.keys():
            links.append( feedparserEntry['link'] )

        # so many links... one is enough!
        if len(links) > 0:
            self.link = links[0]
        else:
            self.link = ''
        if len(linksImages) > 0:
            self.linkImage = linksImages[0]
        else:
            self.linkImage = ''

        # authors
        # format: [{}]
        authors = []
        if 'authors' in feedparserEntry.keys():
            for author in feedparserEntry['authors']:
                if len(author) > 0:
                    authors.append(author)

        # so many authors... one is enough!
        authorList = authors

        # creator
        # format: string
        if 'author' in feedparserEntry.keys():
            author = feedparserEntry['author']
            authorList.append(author)

        # author detail
        # format: {name} -> (string)
        if 'author_detail' in feedparserEntry.keys():
            author_detail = feedparserEntry['author_detail']['name']
            if len(author_detail) > 0:
                authorList.append(author_detail)

        authorList = list(set(authorList))  # makes the list distinct

        if len(authorList) > 0:
            self.author = authorList[0]
        else:
            self.author = ''

        # tag words
        # format: [{term}]
        self.tags = []
        if 'tags' in feedparserEntry.keys():
            for tag in feedparserEntry['tags']:
                self.tags.append(tag['term'])

        # title
        # format: string
        if 'title' in feedparserEntry.keys():
            self.title = feedparserEntry['title']
        else:
            self.title = ''

        # url to an RSS view with this single feed
        # format: string
        if 'wfw_commentrss' in feedparserEntry.keys():
            self.wfw_commentrss = feedparserEntry['wfw_commentrss']
        else:
            self.wfw_commentrss = ''

        # guid link (no spoken address)
        # format: string
        #if 'id' in feedparserEntry.keys():
            #self.id = re.sub(r'\W+', '', feedparserEntry['id'])
        #else:
        self.id = re.sub(r'\W+', '', feedparserEntry['title'])

        # number of user comments
        # format: string
        if 'slash_comments' in feedparserEntry.keys():
            self.slash_comments = feedparserEntry['slash_comments']
        else:
            self.slash_comments = ''

        # direct link to comment view
        # format: string
        if 'comments' in feedparserEntry.keys():
            self.comments = feedparserEntry['comments']
        else:
            self.comments = ''

        # guid isPermaLink
        # format: string
        if 'guidislink' in feedparserEntry.keys():
            self.guidislink = feedparserEntry['guidislink']
        else:
            self.guidislink = ''

        # the (default) parent feed id
        self.feedId = parentFeed.id

        #the (default) parent feed name
        self.feedName = parentFeed.title

        # published time stamp unparsed as string
        # format: string
        self.published = ''
        self.published += '%(y)02d' % {'y': self.published_parsed.tm_mday} + '.'
        self.published += '%(y)02d' % {'y': self.published_parsed.tm_mon} + '.'
        self.published += '%(y)02d' % {'y': self.published_parsed.tm_year} + ' '
        self.published += '%(y)02d' % {'y': self.published_parsed.tm_hour} + ':'
        self.published += '%(y)02d' % {'y': self.published_parsed.tm_min} + ':'
        self.published += '%(y)02d' % {'y': self.published_parsed.tm_sec}

        # feed title in unicode format
        # format: string
        if 'title_detail' in feedparserEntry.keys():
            self.title_detail_value = html_parser.unescape(feedparserEntry['title_detail']['value'])
        else:
            self.title_detail_value = ''

        # summary with link to read on
        # format: string
        if 'summary' in feedparserEntry.keys():
            str = html_parser.unescape(feedparserEntry['summary'])
            #str = str.replace('<a href="', '<a target="_blank" href="')    # alle enthaltenen links in neuem tab oeffnen
            #str = re.sub('<a .*?/a>.*', '', str)                           # alle <a ... tags mit inhalt entfernen
            str = re.sub('<[^<]*?/?>', '', str)                             # tags ohne inhalt entfernen
            self.summary = str
        #else:
            self.summary = ''

        # feed text in unicode format
        # format: string
        if 'summary_detail' in feedparserEntry.keys():
            str = html_parser.unescape(feedparserEntry['summary_detail']['value'])
            #str = str.replace('<a href="', '<a target="_blank" href="')    # alle enthaltenen links in neuem tab oeffnen
            #str = re.sub('<a .*?/a>.*', '', str)                           # alle <a ... tags mit inhalt entfernen
            str = re.sub('<[^<]*?/?>', '', str)                             # tags entfernen
            self.summary_detail_value = str
        else:
            self.summary_detail_value = ''

        # parse summary values for images
        if not self.linkImage:
            if type(feedparserEntry['summary']) == type(""):
                str = html_parser.unescape(feedparserEntry['summary'])
            elif type(feedparserEntry['summary']) == type({}):
                if 'value' in feedparserEntry['summary'].keys():
                    str = html_parser.unescape(feedparserEntry['summary']['value'])
            else:
                str = ""
            src = re.search('<img .*? src="([^"]+)"', str)
            if src:
                src = re.search('src="([^"]+)"', src.group(0))
                s = (src.group(0))[5:-1]
                self.linkImage = s

        # parse summary_detail values for images
        if not self.linkImage:
            str = html_parser.unescape(feedparserEntry['summary_detail']['value'])
            src = re.search('<img .*? src="([^"]+)"', str)
            if src:
                src = re.search('src="([^"]+)"', src.group(0))
                s = (src.group(0))[5:-1]
                self.linkImage = s

        # parse content (atom-specific, I guess) values for images
        if not self.linkImage:
            if 'content' in feedparserEntry.keys():
                for e in feedparserEntry['content']:
                    if isinstance(e, FeedParserDict)  and  'value' in e.keys():
                        str = html_parser.unescape(e['value'])
                        src = re.search('<img .*? src="([^"]+)"', str)
                        if src:
                            src = re.search('src="([^"]+)"', src.group(0))
                            s = (src.group(0))[5:-1]
                            self.linkImage = s
