class Config:
    SECRET_KEY = "supersecretkey123!" 
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #cache system
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60