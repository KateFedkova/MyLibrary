from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Integer, Column, String, create_engine, ForeignKey, DateTime
from sqlalchemy_utils import create_database, database_exists

engine = create_engine("sqlite:///app.db?check_same_thread=False")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password


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


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    author = Column("author", String)
    review = Column("review", String)
    date_added = Column("date_added", DateTime)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))

    def __init__(self, title,  author, review, date_added, user_id):
        super().__init__()
        self.title = title
        self.author = author
        self.review = review
        self.date_added = date_added
        self.user_id = user_id


if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
