from TaipeiTravel import app
from flask import render_template

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")