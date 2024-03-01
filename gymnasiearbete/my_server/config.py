class Config:
    SECRET_KEY = 'hemlignyckel'
    DB_PATH = 'gyar.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gyar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
