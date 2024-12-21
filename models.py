from sqlalchemy import Column, Integer, String , Enum , Date ,Time
from database import Base
from sqlalchemy.orm import validates
import enum

class EtatTache(enum.Enum):
    terminé = "terminé"
    attente = "attente"
    encours = "encours"
    
class EtatConge(enum.Enum):
    accepté = "accepté"
    attente = "attente"
    refusé = "refusé"
    
class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class User(Base):
    __tablename__ = 'users'

    # Définition des colonnes
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    numero = Column(String(20), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String(255), nullable=False)  # Assurez-vous de hacher le mot de passe avant de le stocker
    nb_presence = Column(Integer, default=0)
    nb_absence = Column(Integer, default=0)
    nb_retard = Column(Integer, default=0)

    
    @validates('phone')
    def validate_phone(self, key, value):
        if len(value) < 10:
            raise ValueError("Le numéro de téléphone doit avoir au moins 10 chiffres.")
        return value
    
class Admin(Base):
     __tablename__ = "admin"
    
     id = Column(Integer, primary_key=True, autoincrement=True)
     nom = Column(String(50), nullable=False)
     prenom = Column(String(50), nullable=False)
     email = Column(String(100), unique=True, nullable=False)
     numero = Column(String(20), nullable=False)
     password = Column(String(20), nullable= False)

class Congé(Base):
    __tablename__ = "conge"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cause = Column(String(200), unique=True, nullable=False)
    etat = Column(Enum(EtatConge), nullable=False)
    date_demande = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    
class Retard(Base):
     __tablename__ = "retard"

     id = Column(Integer, primary_key=True, autoincrement=True)
     date_retard = Column(Date, nullable=False)
     heure_retard = Column(Time , nullable= False)

class Absence   (Base):
     __tablename__ = "absence"
     id = Column(Integer, primary_key=True, autoincrement=True)
     date_absence = Column(Date, nullable=False)
    
class EmploiDuTemps(Base):
    __tablename__ = "edt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_travail = Column(Date, nullable=False)
    heure_debut = Column(Time , nullable= False)
    heure_fin = Column(Time , nullable= False)
    
    
class Taches(Base):    
    __tablename__ = "taches"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_aff = Column(Date, nullable=False) 
    heure_aff = Column(Time , nullable= False)
    etat_tache = Column(Enum(EtatConge), nullable=False)
    
class Check(Base):
        
    __tablename__ = "check"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_checkin = Column(Date, nullable=False) 
    heure_checkin = Column(Time , nullable= False)
    heure_checkout = Column(Time , nullable= False)

     
    
    
    
