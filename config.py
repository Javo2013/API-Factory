class Config:
    SECRET_KEY = "supersecretkey123!"  # must be a STRING
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False