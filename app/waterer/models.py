import sqlite3 as dbapi2
from flask import current_app as app
from sqlalchemy.ext.automap import automap_base
# import os

Base = automap_base()
# reflect the tables
Base.prepare(app.db.engine, reflect=True)

# def create_tables(engine):
#     """ create a table from the create_table_sql statement
#     :param conn: Connection object
#     :param create_table_sql: a CREATE TABLE statement
#     :return:
#     """
#     metadata = MetaData(engine)
#     # Create a table with the appropriate Columns
#     Table(WATERHIST, metadata,
#           Column('KEY', Integer, primary_key=True, nullable=False),
#           Column('EVENTTIME', Datetime),
#           Column('DURATION', float))
#     Table(MOISTHIST, metadata,
#           Column('KEY', Integer, primary_key=True, nullable=False),
#           Column('EVENTTIME', Datetime),
#           Column('STATUS', boolean))
#     # Implement the creation
#     metadata.create_all()


class MoistHist(app.db.Model):
    # __table__ = app.db.Model.Table('MoistHist', Base.metadata,
    #                 autoload=True, autoload_with=app.db.engine)
    id = app.db.Column(app.db.Integer, primary_key=True)
    eventtime = app.db.Column(app.db.DateTime, nullable=False)
    status = app.db.Column(app.db.Integer, nullable=False)

    app.db.create_all()

    def __repr__(self):
        return '<MoistHist %r>' % self.eventtime

    # def add_obs(self, eventtime, status):
    #     self.add()

class WaterHist(app.db.Model):
    # __table__ = Table('MoistHist', Base.metadata,
    #                   autoload=True, autoload_with=app.db.engine)
    id = app.db.Column(app.db.Integer, primary_key=True)
    eventtime = app.db.Column(app.db.DateTime, nullable=False)
    status = app.db.Column(app.db.Float, nullable=False)

    app.db.create_all()

    def __repr__(self):
        return '<MWaterHist %r>' % self.eventtime

    # def init_db(self):
    #     with
    #         "CREATE TABLE IF NOT EXISTS MOISTHIST (KEY integer PRIMARY KEY,eventtime datetime NOT NULL,status INTEGER NOT NULL);"
    #         "CREATE TABLE IF NOT EXISTS WATERHIST (KEY integer PRIMARY KEY,eventtime datetime NOT NULL,DURATION FLOAT NOT NULL);"
    def add_obs(self, status):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO MOISTHIST (EVENTTIME, STATUS) VALUES (?, ?);"
            cursor.execute(query, (status["eventtime"], status["status"]))
            connection.commit()
            self.last_key = cursor.lastrowid

    def delete_obs(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM MOISTHIST WHERE (ID = ?)"
            cursor.execute(query, (key,))
            connection.commit()

    def correct_obs(self, key, status):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE MOISTHIST SET EVENTTIME = ?, STATUS = ? WHERE (ID = ?)"
            cursor.execute(query, (status["eventtime"], status["status"], key))
            connection.commit()

    def get_numobs(self, numobs):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT KEY, EVENTTIME,STATUS FROM MOISTHIST ORDER BY EVENTTIME DESC LIMIT ?"
            cursor.execute(query, [numobs])
            moist_hist = cursor.fetchall()
        return moist_hist

    def get_timeobs(self, obssince):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT KEY, EVENTTIME,STATUS FROM MOISTHIST WHERE EVENTTIME > ?"
            cursor.execute(query, [obssince])
            moist_hist = cursor.fetchall()
        return moist_hist

    def get_allobs(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT KEY, EVENTTIME,STATUS FROM MOISTHIST ORDER BY EVENTTIME DESC"
            cursor.execute(query)
            moist_hist = [(key, eventtime, status)
                          for key, eventtime, status in cursor]
            return moist_hist

    def add_water(self, status):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO WATERHIST (EVENTTIME, DURATION) VALUES (?, ?);"
            cursor.execute(query, (status["eventtime"], status["duration"]))
            connection.commit()
            self.last_key = cursor.lastrowid

    def get_numwater(self, numobs):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT KEY, EVENTTIME,DURATION FROM WATERHIST ORDER BY  EVENTTIME DESC LIMIT ?"
            cursor.execute(query, [numobs])
            water_hist = cursor.fetchall()
        return water_hist

    def get_timewater(self, obssince):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT KEY, EVENTTIME,DURATION FROM WATERHIST WHERE EVENTTIME > ?"
            cursor.execute(query, [obssince])
            water_hist = cursor.fetchall()
        return water_hist

    def get_allwater(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT KEY, EVENTTIME, DURATION FROM WATERHIST ORDER BY  EVENTTIME DESC"
            cursor.execute(query)
            water_hist = cursor.fetchall()
            return water_hist


