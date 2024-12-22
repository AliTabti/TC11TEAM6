from database import engine, Base
from models import User , RoleEnum ,Admin , Retard,Absence,Conge,Check,Taches,EmploiDuTemps,EtatConge,EtatTache,UserTache

# Créer toutes les tables dans la base de données
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

if __name__ == "__main__":
    create_tables()
