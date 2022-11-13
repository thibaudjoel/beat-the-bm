import sys
print(sys.path)
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)