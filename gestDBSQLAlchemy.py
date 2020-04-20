from app import db,User,Tech
from werkzeug import security
import sqlite3,os,glob


def addOneTechs(CompleteFileName) :
    s,level,filename=CompleteFileName.split("\\")
    name=filename.split(".")[0].replace("_"," ")
    video=filename
    sound=filename.replace(".mp4",".mp3")
    keywords=name.replace("_"," ")
    level=int(level[0])
    return Tech(name=name,video=video,sound=sound,keywords=keywords,level=level)


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





db.create_all()

user=User(login='admin',password=security.generate_password_hash('1234',method='sha256'),level=0)
db.session.add(user)
user=User(login='fabien',password=security.generate_password_hash('toto',method='sha256'),level=1)
db.session.add(user)


for t in addAllTechs('static'):
    print(t.name)
    db.session.add(t)
db.session.commit()
db.close_all_sessions()