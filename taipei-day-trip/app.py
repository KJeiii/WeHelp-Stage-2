from TaipeiTravel import app
from TaipeiTravel.attraction import attraction_bp
from TaipeiTravel.itinerary import itinerary_bp
from TaipeiTravel.member import member_bp
from TaipeiTravel.payment import payment_bp
from TaipeiTravel.views.views import *


app.register_blueprint(attraction_bp)
app.register_blueprint(itinerary_bp)
app.register_blueprint(member_bp)
app.register_blueprint(payment_bp)

app.run(host="0.0.0.0", port=3000, debug=True)
