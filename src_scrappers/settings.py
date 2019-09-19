# -*- coding: utf-8 -*-
BOT_NAME = 'music_scrapper'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'\
    ' (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.'\
    '0.3809.100 Safari/537.36'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.1
TELNETCONSOLE_ENABLED = False


DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# SPIDER_MIDDLEWARES = {
#    'src.middlewares.SrcSpiderMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'middlewares.CustomRedirectMiddleware': 300
}

# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

ITEM_PIPELINES = {
    'pipelines.SrcPipeline': 300,
}
