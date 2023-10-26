from TaipeiTravel import app
from flask  import render_template

# attraction pages
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


# booking page
@app.route("/booking")
def booking():
	return render_template("booking.html")

# Pages
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
