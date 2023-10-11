from flask import Flask
from dotenv import load_dotenv

# from TaipeiTravel.attraction import attraction_bp
# from TaipeiTravel.itinerary import itinerary_bp
# from TaipeiTravel.member import member_bp
# from TaipeiTravel.payment import payment_bp
# from TaipeiTravel.thankyou import thankyou_bp

load_dotenv()
app=Flask(__name__, 
          template_folder="./views/templates",
          static_folder="./views/static")
app.config["JSON_AS_ASCII"]=False
app.json.ensure_ascii = False
app.config["TEMPLATES_AUTO_RELOAD"]=True



# app.register_blueprint(attraction_bp)
# app.register_blueprint(itinerary_bp)
# app.register_blueprint(member_bp)
# app.register_blueprint(payment_bp)
# app.register_blueprint(thankyou_bp)

