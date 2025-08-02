ALLOWED_HOSTS = ["*"]
DEBUG = True

DATABASES = {
    "default" : {
        "ENGINE" : "django.db.backends.postgresql",
        "NAME" : "db_crm2",
        "USER" : "postgres",
        "PASSWORD" : "mukhibillo",
        "HOST" : "localhost",
        "PORT" : "5432",
        "ATOMIC_REQUEST" : True,
    }
}

HOST = "https://localhost:8000"

