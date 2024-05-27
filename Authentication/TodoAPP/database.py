from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={'check_same_thread':False})


# Enlazar el motor que se ha creado
SessionLocal=sessionmaker(autocommit=False,
                          autoflush=False,
                          bind=engine)


# Crear la base de datos y luego podrá ser capaz de interacturar con ella

Base = declarative_base()

