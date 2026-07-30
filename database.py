from sqlalchemy import create_engine
#to create connection with database
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://root:sravanthi%401234@localhost:3306/product_db"
DATABASE_URL = "postgres://avnadmin:AVNS_YebMrQt0bjL6T9VAgut@pg-17488285-bonthasravanthi850-750a.k.aivencloud.com:19191/defaultdb?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
