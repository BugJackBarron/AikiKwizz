from  AikiKwizz.__init__ import db,User,Tech
from werkzeug import security
import sqlite3,os,glob


def addOneTechs(CompleteFileName) :
    s,level,filename=CompleteFileName.split("\\")
    name=filename.split(".")[0].replace("_"," ")
    video=filename
    if ".mp4" in filename :
        sound=filename.replace(".mp4",".mp3")
    if ".flv" in filename :
        sound=filename.replace(".flv",".mp3")
    keywords=name.replace("_"," ")
    level=int(level[0])
    return Tech(name=name,video=video,sound=sound,keywords=keywords,level=level)


def addTechsFromFolder(folder) :
    """Présuppose que les vidéos sont correctement nommées.
    Génère une liste de requête sqlite pour intégrer  toutes les techniques d'un dossier."""
    s=[addOneTechs(v) for v in glob.glob(os.path.join(folder,"*.mp4"))]
    s+=[addOneTechs(v) for v in glob.glob(os.path.join(folder,"*.flv"))]
    return s


def addAllTechs(basefolder) :

    listRequest=[]
    for f in os.listdir(basefolder) :
        if 'Kyu' in f :
            listRequest+=addTechsFromFolder(os.path.join(basefolder,f))
            print(f"Finished for {f}")
    return listRequest





db.create_all()

user=User(login='admin',password=security.generate_password_hash('aiki.Nyarlathotep22.kwizz',method='sha256'),level=0)
db.session.add(user)


for t in addAllTechs('static'):
    print(t.name)
    db.session.add(t)
db.session.commit()
db.close_all_sessions()