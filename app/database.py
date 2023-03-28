from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Integer, Column, String, create_engine, Date, Time, ForeignKey
from sqlalchemy_utils import create_database, database_exists


engine = create_engine("sqlite:///app.db?check_same_thread=False")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# class Event(Base):
#     __tablename__ = "events"
#
#     id = Column("id", Integer, primary_key=True)
#     date = Column("date", String)
#     time = Column("time", String, nullable=True)
#     header = Column("header", String(80))
#     description = Column("description", String(240), nullable=True)
#     user = Column("user", Integer, ForeignKey("users.id"))
#
#     def __init__(self, date, time, header, description, user):
#         super().__init__()
#         self.date = date
#         self.time = time
#         self.header = header
#         self.description = description
#         self.user = user


class Users(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)
    quote = Column("quote", String, nullable=True)

    def __init__(self, username,  quote, password):
        super().__init__()
        self.username = username
        self.password = password
        self.quote = quote


class WishList(Base):
    __tablename__ = "wish_list"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    author = Column("author", String)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))

    def __init__(self, title,  author, user_id):
        super().__init__()
        self.title = title
        self.author = author
        self.user_id = user_id


if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
