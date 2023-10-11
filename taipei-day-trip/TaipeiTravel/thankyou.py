from flask import render_template, Blueprint

thankyou_bp = Blueprint("thankyou_bp",__name__)

# Pages
@thankyou_bp.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")
