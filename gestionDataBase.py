import sqlite3,os,glob


def addOneTechs(CompleteFileName) :
    s,level,filename=CompleteFileName.split("\\")
    name=filename.split(".")[0].replace("_"," ")
    video=filename
    sound=filename.replace(".mp4",".mp3")
    keywords=name.replace("_"," ")
    level=int(level[0])
    request=f"""INSERT INTO 'techs' ('name', 'video', 'sound', 'keywords', 'level')
    VALUES ('{name}','{video}','{sound}','{keywords}',{level});"""
    return request

def addTechsFromFolder(folder) :
    """Présuppose que les vidéos sont correctement nommées.
    Génère une liste de requête sqlite pour intégrer  toutes les techniques d'un dossier."""
    return [addOneTechs(v) for v in glob.glob(os.path.join(folder,"*.mp4"))]

def addAllTechs(basefolder) :

    listRequest=[]
    for f in os.listdir(basefolder) :
        if 'Kyu' in f :
            listRequest+=addTechsFromFolder(os.path.join(basefolder,f))
    return listRequest



with sqlite3.connect('static/bdd.db') as conn :
    c=conn.cursor()
    c.execute("DROP TABLE 'user'")
    c.execute("""CREATE TABLE 'user' 
    ('id' INTEGER PRIMARY KEY AUTOINCREMENT,
 'login' TEXT NOT NULL,
 'password' TEXT,
 'AlmostUnknownTechs' TEXT,
 'AlmostKnownTechcs' TEXT,
 'WellKnownTechs' TEXT,
 'level' INTEGER NOT NULL,
 'LastConn' DATE NOT NULL,
 'Last10Techs' TEXT);
    """)
    c.execute("DROP TABLE 'techs'")
    c.execute("""CREATE TABLE 'techs' 
('id' INTEGER PRIMARY KEY AUTOINCREMENT,
 'name' TEXT NOT NULL,
 'video' TEXT,
 'sound' TEXT,
 'keywords' TEXT,
 'level' TEXT)
 ;
""")

    c.execute("""INSERT INTO 'user'('id','login','password','level','LastConn') 
VALUES (NULL,'admin','1234',0,'2020-04-18');
""")

    for t in addAllTechs('static') :
        c.execute(t)

