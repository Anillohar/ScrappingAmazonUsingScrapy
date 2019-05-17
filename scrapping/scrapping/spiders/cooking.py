import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import time

class CookingSpider(scrapy.Spider):
	name = 'cooking'
	allowed_domains = ['www.amazon.in']
	start_urls = ['https://www.amazon.in/b/ref=in_pantry-wayfinder-1-1_1??node=9735693031']
	# start_urls = ['https://www.amazon.in/pantry-cooking-essentials/b?ie=UTF8&node=9735693031']

	def parse(self, response):

		price = []
		mrp = []
		linktoimg = []
		title = response.css('div.s-item-container h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract()
		image_urls = response.css('div.s-item-container img.s-access-image.cfMarker::attr(src)').extract()
		images = response.css('div.s-item-container img.s-access-image.cfMarker::attr(src)').extract()
		prices = response.css('div.a-row.a-spacing-none')
		links = response.css('.a-section.a-spacing-none')
		links = links.css('a.a-link-normal::attr(href)').extract()
		# print('these are the links here : \n'+str(links))
		for link in links:
			linktoimg.append(str(link))

		
		for value in prices:
			value1 = value.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract()
			value2 = value.css('span.a-size-small.a-color-secondary.a-text-strike::text').extract()
			if value1:
				if value2:
					price.append(value1)
					mrp.append(value2)
				else:
					mrp.append(' ')
					price.append(value1)

		compressed = zip(title, price, mrp, image_urls ,linktoimg)
		
		for item in compressed:

			response.urljoin(item[4])
			yield scrapy.Request(url=item[4], callback = self.inside_page)
			
			quantity = re.sub(r'^[\D]+', '', str(item[0]))
			title = str(item[0])
			# title = str(item[0]).replace(quantity, '')
			# title = re.sub(r'[\-\(\)\s\,]+$', '', title)
			# title = re.sub(r'^[\(\'\s\"]+', '', title)
			quantity = re.sub(r'[\-\,\"\'\s]+$', '', quantity)
			data = {
			'Title':title,
			'Quantity':quantity,
			'Price':item[1][0],
			'MRP':item[2][0],
			'image_urls': [item[3]],
			'anything' : item[4]
			}
			yield data
		
		# pagination for scrapping from multiple pages until the last page is reached
		next_page = response.css('a#pagnNextLink.pagnNext::attr(href)').extract_first()
		print(next_page)
		if next_page:
			next = response.urljoin('http://www.amazon.in'+str(next_page))
			yield scrapy.Request(url='http://www.amazon.in'+str(next_page), callback = self.parse)

	def inside_page(self, response):
		data = response.css('#altImages')
		imgs = data.css('img::attr(src)').extract()

		for i in imgs:
			if '.gif' in imgs:
				pass
			else:
				data = {
				'image_urls' : [i]
				}
			yield data
