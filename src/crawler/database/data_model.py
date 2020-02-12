from datetime import datetime
from sqlalchemy import Table, Column, Integer, SmallInteger, Numeric, String, DateTime
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stocks'
    
    code = Column(String(6), primary_key=True, index=True)
    company = Column(String(20), nullable=False, unique=True, index=True)
    market_type = Column(SmallInteger(), nullable=False)
    
    sector = Column(SmallInteger(), nullable=True, index=True)
    industry_group = Column(SmallInteger(), nullable=True, index=True)
    industry = Column(SmallInteger(), nullable=True, index=True)
    
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    delisted_on = Column(DateTime(), nullable=True)    

    def __repr__(self):
        return "Stock(code='{self.code}', " \
               "company='{self.company}', " \
               "market_type='{self.market_type}', " \
               "created_on='{self.created_on}', " \
               "updated_on='{self.updated_on}')".format(self=self)
            



if  __name__ == "__main__":
    CONN_STRING = "postgresql+psycopg2://testid:testpw@localhost:7890/stockdb"
    engine = create_engine(CONN_STRING, echo=False)

    # Creates the tables in the database defined by the engine
    Base.metadata.create_all(engine) ##

    # The session is the way SQLAlchemy ORM interacts with the database.
    Session = sessionmaker(bind=engine)
    session = Session()