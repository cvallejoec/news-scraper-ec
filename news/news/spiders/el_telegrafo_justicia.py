import scrapy
import w3lib.html

class ElComercioSpider(scrapy.Spider):
  name = "el_telegrafo_justicia"
  start_urls = [
    'https://www.eltelegrafo.com.ec/contenido/categoria/12/justicia',
  ]
  custom_settings = {
    # 'FEED_URI': 'el-telegrafo-justicia.json',
    # 'FEED_FORMAT': 'json',
    'MEMUSAGE_NOTIFY_MAIL': [
      'cvallejo.ec@gmail.com'
    ],
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
    'FEED_EXPORT_ENCODING': 'utf-8',
  }

  LINKS = '//div[@id="k2Container"]//div[@class="row"]//article/h1/a/@href'
  TITLE = '//article[contains(@class, "full-article")]//h1[@class="story-heading"]/span/text()'
  PARAGRAPHS = '//div[@class="itemFullText"]//p'
  TIME = '//article[contains(@class, "full-article")]//span[contains(@class, "story-publishup")]//text()'
  
  def parse(self, response):
    news_links = response.xpath(self.LINKS).getall()

    for link in news_links:
      yield response.follow(link, callback=self.parse_full_new, cb_kwargs={ 'url': link })

  def parse_full_new(self, response, **kwargs):
    link = kwargs["url"]
    title = response.xpath(self.TITLE).get()

    paragraphs_raw = response.xpath(self.PARAGRAPHS).getall()
    time_raw = response.xpath(self.TIME).getall()
    time = time_raw[0].strip() + ' ' + time_raw[1].strip()

    category = "Justicia"

    body = []

    for paragraph in paragraphs_raw:
      output = w3lib.html.remove_tags(paragraph)
      body.append(output)

    yield {
      'url': 'https://www.eltelegrafo.com.ec/' + link,
      'title': title,
      'time': time,
      'category': category,
      'body': body,
    }


    

