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
    #phone = Column(String(20), nullable=False)
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
    Session = sessionmaker(bind=engine)
    session = Session()


    # Delete all rows
    #for c in session.query(Cookie):
    #    session.delete(c)
    #    session.commit()
    #print(session.query(Cookie.cookie_name, Cookie.quantity).first())


    """
    cc_cookie = Cookie(cookie_name='chocolate chip',
                       cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
                       cookie_sku='CC01',
                       quantity=12,
                       unit_cost=0.50)
    session.add(cc_cookie)
    session.commit()
    
    #-----------------

    dcc = Cookie(cookie_name='dark chocolate chip',
                cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
                cookie_sku='CC02',
                quantity=1,
                unit_cost=0.75)
    mol = Cookie(cookie_name='molasses',
                cookie_recipe_url='http://some.aweso.me/cookie/recipe_molasses.html',
                cookie_sku='MOL01',
                quantity=1,
                unit_cost=0.80)
    session.add(dcc)
    session.add(mol)
    session.flush()
    print(dcc.cookie_id)
    print(mol.cookie_id)
    
    #-------------------------
    c1 = Cookie(cookie_name='peanut butter',
            cookie_recipe_url='http://some.aweso.me/cookie/peanut.html',
            cookie_sku='PB01',
            quantity=24,
            unit_cost=0.25)
    c2 = Cookie(cookie_name='oatmeal raisin',
            cookie_recipe_url='http://some.okay.me/cookie/raisin.html',
            cookie_sku='EWW01',
            quantity=100,
            unit_cost=1.00)
    session.bulk_save_objects([c1,c2])
    session.commit()
    print(c1.cookie_id)
    
    #Update-------------------------
    query = session.query(Cookie)
    cc_cookie = query.filter(Cookie.cookie_name == "chocolate chip").first()
    cc_cookie.quantity = cc_cookie.quantity + 120
    session.commit()
    print(cc_cookie.quantity)
    
    query = session.query(Cookie)
    query = query.filter(Cookie.cookie_name == "chocolate chip")
    query.update({Cookie.quantity: Cookie.quantity - 20})
    cc_cookie = query.first()
    print(cc_cookie.quantity)
    
    #Delete-------------------------
    query = session.query(Cookie)
    query = query.filter(Cookie.cookie_name == "dark chocolate chip")
    dcc_cookie = query.one()
    session.delete(dcc_cookie)
    session.commit()
    dcc_cookie = query.first()
    print(dcc_cookie)
    
    query = session.query(Cookie)
    query = query.filter(Cookie.cookie_name == "molasses")
    query.delete()
    mol_cookie = query.first()
    print(mol_cookie)
    
    #----------------------
    cookiemon = User(username='cookiemon',
                email_address='mon@cookie.com',
                password='password')
    cakeeater = User(username='cakeeater',
                email_address='cakeeater@cake.com',
                password='password')
    pieperson = User(username='pieperson',
                email_address='person@pie.com',
                password='password')
    session.add(cookiemon)
    session.add(cakeeater)
    session.add(pieperson)
    session.commit()
    """
    o1 = Order()
    o1.user = cookiemon
    session.add(o1)

    cc = session.query(Cookie).filter(Cookie.cookie_name =="chocolate chip").one()
    line1 = LineItem(cookie=cc, quantity=2, extended_cost=1.00)
    
    pb = session.query(Cookie).filter(Cookie.cookie_name =="peanut butter").one()
    line2 = LineItem(quantity=12, extended_cost=3.00)
    line2.cookie = pb
    line2.order = o1
    
    o1.line_items.append(line1)
    
    
    line_items.append(line2)
    session.commit()
