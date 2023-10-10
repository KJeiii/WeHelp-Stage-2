from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.json.ensure_ascii = False
app.config["TEMPLATES_AUTO_RELOAD"]=True