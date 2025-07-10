# setup_db.py
from app.db.database import Base, engine
from app.models import *

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")