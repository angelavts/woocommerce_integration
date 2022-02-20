from woocommerce import API

# LOCAL DATA(TEST)
LOCAL_KEY = "ck_04c7be916fe8a2cfc9a1d114a1896c4f9c5d2f62"
LOCAL_SECRET = "cs_63c03d4df8e7d03e0f9b49d19488295157c14403"
LOCAL_URL = "http://localhost/wordpress/"

# SERVER DATA
SERVER_KEY = "ck_da9d1afb7938fbc35035dbfaa9289dc681d4e208"
SERVER_SECRET = "cs_7e6a337cbafbefdc58d4f33449549371cbe2060a"
SERVER_URL = "http://argemtshop.com"

# conexión con la API

wcapi = API(
    url=LOCAL_URL,
    consumer_key=LOCAL_KEY,
    consumer_secret=LOCAL_SECRET,
    version="wc/v3"
)