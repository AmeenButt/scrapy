# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookspiderPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all sapaces from field_names
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                print(value)
                adapter[field_name] = value.strip()

        # converting all into lower case
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # convery currency into dollar
        currency_type = ['price', 'price_excl_tax', 'price_incl_tax']
        for dollar in currency_type:
            value = adapter.get(dollar)
            # Remove the currency symbol and any leading/trailing whitespace
            value = value.replace('£', '').strip()
            adapter[dollar] = value

        # converting rating into int
        ratings = adapter.get('star_rating')
        split_star = ratings.split(' ')
        lower_star = split_star[1].lower()
        if lower_star == 'zero':
            adapter['star_rating'] = 0
        elif lower_star == 'one':
            adapter['star_rating'] = 1
        elif lower_star == 'two':
            adapter['star_rating'] = 2
        elif lower_star == 'three':
            adapter['star_rating'] = 3
        elif lower_star == 'four':
            adapter['star_rating'] = 4
        elif lower_star == 'five':
            adapter['star_rating'] = 5

        # availability in just int
        available_stock = adapter.get('availability')
        split_stock = available_stock.split('(')
        if len(available_stock) < 2:
            adapter['availability'] = 0
        else:
            split_int = split_stock[1].split(' ')
            adapter['availability'] = int(split_int[0])

        return item



import mysql.connector

class SaveToMYSQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Malik|5awan)',
            database='book'
        )
        self.cur = self.conn.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books(
                id int NOT NULL auto_increment,
                title TEXT,
                price DECIMAL,
                star_rating INTEGER,
                product_type TEXT,
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                availability INTEGER,
                category VARCHAR(255),
                PRIMARY KEY (id)
            )
        ''')

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT INTO books(
                title,
                price,
                star_rating,
                product_type,
                price_excl_tax,
                price_incl_tax,
                availability,
                category
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )''', (
            item['title'],
            item['price'],
            item['star_rating'],
            item['product_type'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['availability'],
            item['category']
        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
        self.cur.close()

