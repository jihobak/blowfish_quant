from datetime import datetime
from sqlalchemy import Table, Column, Integer, Numeric, String, DateTime
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key = True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)

    # This establishes a one-to-many relationship.
    user = relationship("User", backref=backref('orders', order_by=order_id))

    def __repr__(self):
        return "Order(user_id={self.user_id}, " \
                "shipped={self.shipped})".format(self=self)


class Cookie(Base):
    __tablename__ = 'cookies'


    cookie_id = Column(Integer(), primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
                "cookie_recipe_url='{self.cookie_recipe_url}', " \
                "cookie_sku='{self.cookie_sku}', " \
                "quantity={self.quantity}, " \
                "unit_cost={self.unit_cost})".format(self=self)


class LineItem(Base):
    __tablename__ = 'line_items'

    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))

    order = relationship("Order", backref=backref('line_items', order_by=line_item_id))
    cookie = relationship("Cookie", backref=backref('cookies', uselist=False))

    def __repr__(self):
        return "LineItems(order_id={self.order_id}, " \
                "cookie_id={self.cookie_id}, " \
                "quantity={self.quantity}, " \
                "extended_cost={self.extended_cost})".format(self=self)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=True)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "User(username='{self.username}', " \
            "email_address='{self.email_address}', " \
            "phone='{self.phone}', " \
            "password='{self.password}')".format(self=self)


if  __name__ == "__main__":
    CONN_STRING = "postgresql+psycopg2://testid:testpw@localhost:7890/stockdb"
    engine = create_engine(CONN_STRING, echo=False)

    # Creates the tables in the database defined by the engine
    Base.metadata.create_all(engine) ##

    # The session is the way SQLAlchemy ORM interacts with the database.
    #Session = sessionmaker(bind=engine)
    #session = Session()

    #cc_cookie = Cookie(cookie_name='chocolate chip',
    #                   cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
    #                   cookie_sku='CC01',
    #                   quantity=12,
    #                   unit_cost=0.50)
    #session.add(cc_cookie)
    #session.commit()