from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('db.link', echo=True)
base = declarative_base()


class DatasAboutProject(base):
    __tablename__ = 'Datas_about_project'