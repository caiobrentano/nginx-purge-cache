from api.app import db
from api.models import Base

Base.metadata.create_all(bind=db.engine)
