import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Shop, Publisher, Stock, Sale, Book
import json

DSN = 'postgresql://postgres:@localhost:5432/netology_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as file:
    data = json.load(file)

for string in data:
    model = {"publisher" : Publisher,
             "shop" : Shop,
             "book" : Book,
             "stock" : Stock,
             "sale" : Sale}[string.get("model")]
    session.add(model(id=string.get('pk'), **string.get('fields')))
session.commit()

pub = input('Введите ID Publisher: ')
q1 = session.query(Publisher).filter(Publisher.id == pub)
q2 = session.query(Book).join(Publisher.books).filter(Publisher.id == pub)

for p in q1.all():
    print(f'Издатель с ID {pub} - {p.name}')

print(f'Данный издатель выпустил следующие книги: ')

for b in q2.all():
    print(f'"{b.title}"')

session.close( )