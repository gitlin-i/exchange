from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from main import MODE
from app.secret import database_secret

def database_url_generator(dbms, port, db ,user_name, password, host_name):
    return dbms + "://" + user_name + ":" + password +"@" + host_name + ":" + port + "/" + db

aws_endpoint = database_secret.aws_rds_endpoint
aws_user = database_secret.aws_rds_user1
aws_user_password = database_secret.aws_rds_user1_password
aws_db1 = database_secret.aws_rds_oper_db_name
aws_db2 = database_secret.aws_rds_test_db_name

local_dev_database_url = database_url_generator("mysql+mysqldb","3306", "test","test","test","localhost")
aws_operation_database_url = database_url_generator("mysql+mysqldb","3306",aws_db1,aws_user,aws_user_password,aws_endpoint)
aws_test_database_url = database_url_generator("mysql+mysqldb","3306",aws_db2,aws_user,aws_user_password,aws_endpoint)

url = aws_test_database_url if MODE =="OPERATION" else local_dev_database_url


async_engine = create_async_engine(url,echo=True,pool_pre_ping= True)
engine = create_engine(url,echo=True,pool_pre_ping=True)

SessionLocal = sessionmaker(engine,autoflush=False,autocommit=False)
AsyncSessionLocal = async_sessionmaker(async_engine, autoflush= False, autocommit= False)
class Base(AsyncAttrs, DeclarativeBase):
    pass
