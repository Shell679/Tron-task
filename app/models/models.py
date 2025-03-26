from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import MetaData

models_metadata = MetaData()
Base = declarative_base(metadata=models_metadata)
