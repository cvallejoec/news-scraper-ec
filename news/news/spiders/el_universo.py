import scrapy
import w3lib.html

class ElComercioSpider(scrapy.Spider):
  name = "el_universo"
  start_urls = [
    'https://www.eluniverso.com/'
  ]
  custom_settings = {
    # 'FEED_URI': 'el-universo.json',
    # 'FEED_FORMAT': 'json',
    'MEMUSAGE_NOTIFY_MAIL': [
      'cvallejo.ec@gmail.com'
    ],
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
    'FEED_EXPORT_ENCODING': 'utf-8',
  }

  LINKS = '//h2[contains(@class, "text-base")]/a/@href'
  TITLE = '//div[contains(@class, "chain")]/h1/text()'
  PARAGRAPHS = '//div[contains(@class, "chain")]//section[contains(@class, "article-body")]/p/text()'
  TIME = '//p[contains(@class, "date")]/time/text()'
  CATEGORY = '//div[contains(@class, "overline")]//a/text()'
  
  def parse(self, response):
    self.counter += 1

    news_links = response.xpath(self.LINKS).getall()

    for link in news_links:
      yield response.follow(link, callback=self.parse_full_new, cb_kwargs={ 'url': link })

  def parse_full_new(self, response, **kwargs):
    link = kwargs["url"]
    title = response.xpath(self.TITLE).get()

    paragraphs_raw = response.xpath(self.PARAGRAPHS).getall()
    time = response.xpath(self.TIME).get().strip()
    category = response.xpath(self.CATEGORY).get()

    body = []

    for paragraph in paragraphs_raw:
      output = w3lib.html.remove_tags(paragraph)
      body.append(output)

    yield {
      'url': 'https://eluniverso.com' + link,
      'title': title,
      'time': time,
      'category': category,
      'body': body,
    }


    

