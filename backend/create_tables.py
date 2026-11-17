
from backend.database import engine, Base
from backend import models

Base.metadata.create_all(bind=engine)

print("DeepGuard database tables created successfully!")
