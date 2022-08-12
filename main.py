import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Sale, Stock
import json

DSN = "postgresql://postgres:lala@localhost:5432/alchemy_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

filename = 'test_data.json'
with open(filename, 'r') as file:
    j_data = json.load(file)
    for elem in j_data:
        model = elem['model']
        fields = elem['fields']
        if model == 'publisher':
            field = Publisher(**fields)
        elif model == 'book':
            field = Book(**fields)
        elif model == 'shop':
            field = Shop(**fields)
        elif model == 'stock':
            field = Stock(**fields)
        elif model == 'sale':
            field = Sale(**fields)
        session.add(field)
    session.commit()

    # поиск магазина по издателю, находящемуся в продаже
    publisher_ident = input('Enter publisher name or id: ')

    if publisher_ident and publisher_ident.isdigit():
        shop_name_from_publisher = session.query(Shop).join(Stock).join(Book).join(Publisher).join(Sale).filter(Publisher.id==publisher_ident)
    elif publisher_ident and isinstance(publisher_ident, str):
        shop_name_from_publisher = session.query(Shop).join(Stock).join(Book).join(Publisher).join(Sale).filter(
            Publisher.name == publisher_ident)
    else:
        print('Error. Publisher not found')

    if shop_name_from_publisher:
        for s in shop_name_from_publisher.all():
            print(s.id, s.name)
    else:
        print('Error')

session.commit()


