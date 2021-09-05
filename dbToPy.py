from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base
# Database data classes
from sqlalchemy import Column, Integer, SmallInteger, DECIMAL, String, Date, Boolean,\
    ForeignKey, CheckConstraint

from localDbUrl import url_str

# Variable to handle the db session
db_engine = create_engine(url_str, echo=False)

# Objects used to build Python classes for database tables
Base = declarative_base()
metadata = MetaData()


# Articles
class Articles(Base):
    __tablename__ = 'Articles'
    __table_args__ = {"schema": "atroosproject"}

    id = Column('id', Integer, CheckConstraint('id>=0'), primary_key=True)
    name = Column('name', String(70), nullable=False)
    price = Column('price', DECIMAL(6, 2), CheckConstraint('price>0.0'), nullable=False)
    quantity = Column('quantity', SmallInteger, CheckConstraint('quantity>=0'), nullable=False)


# Users
class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = {"schema": "atroosproject"}

    name = Column('name', String(20), nullable=False)
    surname = Column('surname', String(30), nullable=False)
    email = Column('email', String(320), primary_key=True)
    phone_number = Column('phoneN', String(10))
    birth_date = Column('birthDate', Date)

    country = Column('country', String(20), nullable=False)
    city = Column('city', String(30), nullable=False)
    address = Column('address', String(70), nullable=False)
    civic_number = Column('civicN', SmallInteger, nullable=False)
    cap = Column('cap', String(5), nullable=False)


# Orders
class Orders(Base):
    __tablename__ = 'Orders'
    __table_args__ = {"schema": "atroosproject"}

    id = Column('id', Integer, primary_key=True)
    article_id = Column('articleId', Integer, primary_key=True)

    user_email = Column(ForeignKey('users.email'), nullable=False)

    state = Column('state', Boolean, nullable=False, default=False)
    quantity = Column('quantity', SmallInteger, nullable=False)


# Safe creation of python tables
metadata.create_all(db_engine)


# SQL QUERIES

# Return logged in user information
def get_logged_in_user(connection):
    # The user Mario Rossi is already considered logged in
    # To implement SQL queries, it's also possible to import select() from sqlalchemy.sql
    # statement = select(Users).where(Users.email == 'rossimario72@gmail.com')
    statement = ('SELECT * '
                 'FROM atroosproject.users U '
                 'WHERE U.email=\'{email}\''
                 ).format(email='rossimario72@gmail.com')

    result = connection.execute(statement)

    for record in result:
        return record


# Retrieve user's pending order cart
def get_cart(connection, user_email):
    statement = ('SELECT O.id AS order_id, O.articleId AS article_id,'
                 '  A.name AS article_name, A.price AS price, O.quantity AS quantity '
                 'FROM atroosproject.orders O '
                 '  JOIN atroosproject.articles A ON O.articleId = A.id '
                 'WHERE O.userEmail=\'{email}\' AND O.state=FALSE'
                 ).format(email=user_email)

    return connection.execute(statement).all()


# Delete one article of a certain order from orders table
def remove_article_from_orders(connection, order_id, article_id):
    statement = ('DELETE FROM atroosproject.orders O '
                 'WHERE O.id=\'{order_id}\' AND O.articleId=\'{article_id}\''
                 ).format(order_id=order_id, article_id=article_id)

    return connection.execute(statement)


# Change article request of order
def update_order_article_quantity(connection, order_id, article_id, quantity):
    statement = ('UPDATE atroosproject.orders O '
                 'SET O.quantity=\'{quantity}\' '
                 'WHERE O.id=\'{order_id}\' AND O.articleId=\'{article_id}\''
                 ).format(quantity=quantity, order_id=order_id, article_id=article_id)

    return connection.execute(statement)


# Check articles availability
def check_availability(connection, order_id):
    statement = ('SELECT A.id '
                 'FROM atroosproject.articles A '
                 '  JOIN atroosproject.orders O ON A.id = O.articleId '
                 'WHERE O.id=\'{order_id}\' AND A.quantity<O.quantity'
                 ).format(order_id=order_id)

    # Return an empty list if articles are available, if not a list of unavailable article ids
    return connection.execute(statement).all()


# Retrieve order state
def get_order_state(connection, order_id):
    statement = ('SELECT O.state AS state '
                 'FROM atroosproject.orders O '
                 'WHERE O.id=\'{id}\''
                 ).format(id=order_id)

    result = connection.execute(statement)

    for record in result:
        return record.state


# Set order as settled
def set_settled(connection, order_id):
    statement = ('UPDATE atroosproject.orders O '
                 'SET O.state=TRUE '
                 'WHERE O.id=\'{id}\''
                 ).format(id=order_id)

    return connection.execute(statement)
