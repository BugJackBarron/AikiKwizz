import sqlite3

conn=sqlite3.connect('static/bdd.db')

c=conn.cursor()
c.execute("DROP TABLE 'user'")
c.execute("""CREATE TABLE 'user' 
('id' INTEGER PRMIARY KEY NOT NULL,
 'login' TEXT NOT NULL,
 'password' TEXT,
 'AlmostUnknownTechs' TEXT,
 'AlmostKnownTechcs' TEXT,
 'WellKnownTechs' TEXT,
 'level' INTEGER NOT NULL,
 'LastConn' DATE NOT NULL,
 'Last10Techs' TEXT);
""")
