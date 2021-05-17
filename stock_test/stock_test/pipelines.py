# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface



import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from stock_test.model import StockTrading


class StockTestPipeline:
    def process_item(self, item, spider):
        new_item = StockTrading(stock_code=item.get('stock_code'),
                                open_date=item.get('date'),
                                deal_time=item.get('deal_time'),
                                deal_price=item.get('deal_price'),
                                increment=item.get('increment'),
                                price_vary=item.get('price_variation'),
                                shares=item.get('shares'),
                                volume=item.get('volume'),
                                status=item.get('status'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

