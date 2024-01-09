'''
Methods to Databases
Description : All logics
'''


## Libraries -----------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # Manejo de componentes de ORM (Object-Relational Mapping)
from sqlalchemy.ext.declarative import declarative_base

## Root Data bases -----------
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db' # Use this location to create a location of this database on our FastAPIAPP

connect_args={'check_same_thread': False} # : Este es un argumento opcional que se pasa a create_engine. En este caso, se está usando para SQLite, que es un sistema de gestión de base de datos que no permite por defecto el uso de conexiones en diferentes hilos. Al establecer 'check_same_thread': False, se permite que múltiples hilos (o solicitudes en el caso de una aplicación web) utilicen la misma conexión, lo cual es necesario en aplicaciones web asíncronas como las creadas con FastAPI.



engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})


## Base ------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base =  declarative_base()