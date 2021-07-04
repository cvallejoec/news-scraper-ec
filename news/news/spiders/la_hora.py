import scrapy
import w3lib.html

class ElComercioSpider(scrapy.Spider):
  name = "la_hora"
  start_urls = [
    'https://www.lahora.com.ec/categoria/pais/'
  ]
  custom_settings = {
    # 'FEED_URI': 'la-hora.json',
    # 'FEED_FORMAT': 'json',
    'MEMUSAGE_NOTIFY_MAIL': [
      'cvallejo.ec@gmail.com'
    ],
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
    'FEED_EXPORT_ENCODING': 'utf-8',
  }

  LINKS = '//div[contains(@class, "tdb-category-loop-posts")]//div[contains(@class, "td-module-container")]//h3[contains(@class, "entry-title")]//a/@href'
  TITLE = '//div[@class="wpb_wrapper"]//h1[@class="tdb-title-text"]/text()'
  PARAGRAPHS = '//div[@class="vc_column-inner"]//div[@class="tdb-block-inner td-fix-index"]/p'
  TIME = '//div[contains(@class, "tdb-block-inner")]/time/text()'
  NEXT_PAGE = '//div[contains(@class, "page-nav")]//a[last()]/@href'
  
  pages_to_scrap = 2
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

    paragraphs_raw = response.xpath(self.PARAGRAPHS).getall()
    time = response.xpath(self.TIME).get().strip()
    category = "Pais"

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


    

