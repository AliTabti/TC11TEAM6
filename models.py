from sqlalchemy import Column, Integer, String, Enum, Date, Time, ForeignKey
from database import Base
from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime
import enum
from typing import List
from sqlalchemy.orm import relationship


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


class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    numero: str
    role: RoleEnum
    password: str
    nb_presence: int
    nb_absence: int
    nb_retard: int


class UserTache(Base):  # Corrected class name to follow camel case convention
    __tablename__ = "user_tache"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key for the relationship
    tache_id = Column(Integer, ForeignKey('taches.id'), nullable=False)


# SQLAlchemy Model for User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    numero = Column(String(20), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String(255), nullable=False)
    nb_presence = Column(Integer, default=0)
    nb_absence = Column(Integer, default=0)
    nb_retard = Column(Integer, default=0)
    taches = relationship("Taches", secondary=UserTache, back_populates="users")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    numero = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)  # Adjusted size of password


class Conge(Base):
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
    heure_retard = Column(Time, nullable=False)


class Absence(Base):
    __tablename__ = "absence"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_absence = Column(Date, nullable=False)


class EmploiDuTemps(Base):
    __tablename__ = "edt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_travail = Column(Date, nullable=False)
    heure_debut = Column(Time, nullable=False)
    heure_fin = Column(Time, nullable=False)


class TaskCreate(BaseModel):
    user_ids: List[int]
    date_aff: date
    etat_tache: EtatTache
    task_content: str
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Taches(Base):
    __tablename__ = "taches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_aff = Column(Date, nullable=False)
    etat_tache = Column(Enum(EtatTache), nullable=False)
    task_content = Column(String(255), nullable=False)

    # Relationship with the 'users' table
    users = relationship("User", secondary=UserTache, back_populates="taches")


class CheckCreate(BaseModel):
    date_checkin: date
    heure_checkin: time
    heure_checkout: time
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Check(Base):
    __tablename__ = "check"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_checkin = Column(Date, nullable=False)
    heure_checkin = Column(Time, nullable=False)
    heure_checkout = Column(Time, nullable=False)