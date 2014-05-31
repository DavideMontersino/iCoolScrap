# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class IcoolhuntItem(Item):
	"""
	Defines a prey
	"""
	description = Field()
	image = Field()
	user_name = Field()
	user_link = Field()
	prey_link = Field()
	data_stream_id = Field()
	tag_name = Field()
	tag_link = Field()
	last = Field()
