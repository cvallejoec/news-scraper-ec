import scrapy
from urllib.parse import urlsplit, urlunsplit

class ElComercioSpider(scrapy.Spider):
  name = "el_comercio"
  start_urls = [
    'https://www.elcomercio.com/ultima-hora'
  ]
  custom_settings = {
    # 'FEED_URI': 'el-comercio.json',
    # 'FEED_FORMAT': 'json',
    'MEMUSAGE_NOTIFY_MAIL': [
      'cvallejo.ec@gmail.com'
    ],
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
    'FEED_EXPORT_ENCODING': 'utf-8',
  }

  TITLES = '//h3[@class="list-item__title"]/a/text()'
  NEXT_PAGE = '//footer/a[contains(@class, "next")]/@href'
  
  pages_to_scrap = 3
  counter = 0

  def parse(self, response):
    titles = response.xpath(self.TITLES).getall()

    next_link = response.xpath(self.NEXT_PAGE).get()
    yield response.follow(next_link, callback=self.parse_only_titles, cb_kwargs={'titles': titles})


  def parse_only_titles(self, response, **kwargs):
    self.counter += 1
    if kwargs:
      titles = kwargs['titles']

    titles.extend(response.xpath(self.TITLES).getall())

    next_link = response.xpath(self.NEXT_PAGE).get()
    if self.counter + 1 < self.pages_to_scrap:
      yield response.follow(next_link, callback=self.parse_only_titles, cb_kwargs={'titles': titles})
    else:
      yield {
        'el_comercio': titles
      }
    