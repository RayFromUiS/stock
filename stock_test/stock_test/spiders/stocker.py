from datetime import date
from datetime import datetime

import scrapy
from stock_test.model import db_connect,create_table,StockTrading
from stock_test.items import StockTestItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from stock_test.helpers import read_companies
from bs4 import BeautifulSoup
from bs4 import Tag

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker



class StockerSpider(scrapy.Spider):
    name = 'stocker'
    file = 'stock_test/spiders/companies'
    # allowed_domains = ['example.com']
    companies = read_companies(file)
    start_urls = [f'https://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol={company}' for company in companies]

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)


    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse_com,
                wait_time=30,
                wait_until=EC.presence_of_element_located((By.ID, 'datatbl')),
                cb_kwargs={'stock_code':url.split('=')[-1]}
            )

    def parse_com(self, response,stock_code):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = StockTestItem()
        table_ele = response.css('table#datatbl').get()
        soup = BeautifulSoup(table_ele,'lxml')
        rows = soup.find_all(lambda tag: tag.name == 'tr')[1:]
        for row in rows:
            row_detail = []
            for desc in row.descendants:
                if isinstance(desc, Tag):
                    row_detail.append(desc.text)
            # print(row_detail[0])
            item['deal_time'] = datetime.strptime(row_detail[0],'%H:%M:%S')
            item['deal_price'] = row_detail[1]
            item['increment'] = row_detail[2]
            # print(row_detail[3])
            item['price_variation'] = row_detail[3]
            item['shares'] = row_detail[4]
            item['volume'] = row_detail[5]
            item['status'] = row_detail[6]
            item['stock_code'] = stock_code
            item['date'] = date.today()

            result = self.session.query(StockTrading) \
                .filter(and_(StockTrading.deal_time==item['deal_time'],StockTrading.open_date==item['date']))\
                .first()
            if not result:
                yield item









