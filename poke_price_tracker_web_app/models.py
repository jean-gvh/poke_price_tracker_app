from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 

Base = declarative_base()

class PokemonBloc(Base):
    __tablename__ = 'pokemon_bloc'
    bloc_ID = Column(Integer, primary_key=True,autoincrement=True)
    bloc_name = Column(String(length=255), nullable=False)

class PokemonSet(Base):
    __tablename__ = 'pokemon_set'
    set_ID =  Column(Integer, primary_key=True,autoincrement=True)
    set_name = Column(String(length=255), nullable=False)
    release_date = Column(String(length=255), nullable=False)
    cards_count = Column(Integer, nullable=False)
    bloc_ID = Column(Integer, ForeignKey('pokemon_bloc.bloc_ID'), nullable=False)




class EbaySalesData(Base):
    __tablename__ = 'ebay_sales_data'
    ebay_sale_ID = Column(Integer, primary_key=True,autoincrement=True)
    card_name = Column(String(length=255), nullable=False)
    card_price_EUR = Column(Integer)
    sold_date = Column(DateTime, nullable=False)
    seller_ID = Column(Integer, ForeignKey('ebay_seller.seller_ID'), nullable=False)
    set_ID = Column(Integer, ForeignKey('pokemon_set.set_ID'), nullable=False)
    pokemon_set = relationship("PokemonSet")
    bloc_ID = Column(Integer, ForeignKey('pokemon_bloc.bloc_ID'), nullable=False)


class EbaySeller(Base):
    __tablename__ = 'ebay_seller'
    seller_ID = Column(Integer, primary_key=True,autoincrement=True)
    seller_name = Column(String(length=255), nullable=False)  # Spécifiez la longueur ici
    seller_reviews = Column(Integer, default=0)
    seller_ratings = Column(Float, default=0)