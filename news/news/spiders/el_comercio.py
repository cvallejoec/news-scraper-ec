import scrapy
import w3lib.html

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

  LINKS = '//section[@class="content"]//h3[@class="list-item__title"]/a/@href'
  TITLE = '//header/h1[@class="entry__title"]/text()'
  VIDEO_TITLE = '//h1[@class="entry__title"]/text()'
  PARAGRAPHS = '//div[@class="entry__content"]//p'
  VIDEO_DESCRIPTION = '//p[contains(@class, "entry__description")]/text()'
  TIME = '//div[contains(@class, "entry__date")]/time/text()'
  VIDEO_TIME = '//div[contains(@class, "entry__meta")]//time/text()'
  CATEGORY = '//nav//li[contains(@class, "text-uppercase")]//b/text()'
  NEXT_PAGE = '//footer/a[contains(@class, "next")]/@href'
  
  pages_to_scrap = 5
  counter = 0

  def parse(self, response):
    self.counter += 1

    news_links = response.xpath(self.LINKS).getall()

    for link in news_links:
      yield response.follow(link, callback=self.parse_full_new, cb_kwargs={ 'url': link })

    next_link = response.xpath(self.NEXT_PAGE).get()
    if self.counter < self.pages_to_scrap:
      yield response.follow(next_link, callback=self.parse)

  def parse_full_new(self, response, **kwargs):
    link = kwargs["url"]
    title = response.xpath(self.TITLE).get()

    if (title):
      # Is a "normal" new 
      paragraphs_raw = response.xpath(self.PARAGRAPHS).getall()
      time = response.xpath(self.TIME).get().strip()
      category = response.xpath(self.CATEGORY).get()

      body = []

      for paragraph in paragraphs_raw:
        output = w3lib.html.remove_tags(paragraph)
        body.append(output)

      yield {
        'url': link,
        'title': title,
        'time': time,
        'category': category,
        'body': body,
      }

    else:
      # Is a video type new
      title = response.xpath(self.VIDEO_TITLE).get()
      paragraph = response.xpath(self.VIDEO_DESCRIPTION).get()
      body = [paragraph]
      time = response.xpath(self.VIDEO_TIME).get()

      yield {
        'url': link,
        'title': title,
        'time': time,
        'category': 'Video',
        'body': body,
      }

    

