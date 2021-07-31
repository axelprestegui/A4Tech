class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/am4zonas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER =  "instance"