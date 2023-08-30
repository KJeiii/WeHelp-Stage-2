from flask import *
from MySQLTool import MySQLTool

def to_dict(attraction_result:list, image_result:list):
	data = [{
		"id": _["attraction_id"],
		"name": _["attraction_name"],
		"category": _["category"],
		"description": _["description"],
		"address": _["address"],
		"transport": _["transport"],
		"mrt": _["mrt_name"],
		"lat": _["lat"],
		"lng": _["lng"],
		"img": image_result[_["attraction_id"]]
	} for _ in attraction_result]
	return data

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# build MySQL connection
db = MySQLTool()

# Pages
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")


@app.route("/booking")
def booking():
	return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# API
@app.route("/api/attractions")
def attractions():

	# parse parameters
	page  = request.args.get("page")
	keyword = request.args.get("keyword")

	# count total attractions data and total pages 
	total_attraction_amount = db.total_attractions()
	total_pages = int(round(total_attraction_amount/12, 0)) - 1

	# ------- Response error if it is not provided (page parameter is required) --------
	if page == None:
		response = {
			"error": True,
			"message": f'please provide page parameter ranged from 0 to {total_pages}.'
		}
		return jsonify(response), 500
	
	# ------- Response error if page parameter exceeds maximum. ------
	page = int(page)
	if page > total_pages:
		response = {
			"error": True,
			"message": f'maximum page is {total_pages}'
		}
		return jsonify(response), 500
	
	# ------ if page parameter is given, reponse data. ------
	# set nextPage value
	attraction_range = (page*12+1, page*12+12)
	if page == 4:
		nextPage = None
	else:
		nextPage = page + 1

	# search image
	image_list = db.Search_image(
		attraction_id_start = attraction_range[0],
		attraction_id_end = attraction_range[1]
	)
	image_result = {}
	for n in range(attraction_range[0], attraction_range[1]+1):
		for _ in image_list:
			if _["attraction_id"] == n:
				try:
					image_result[n].append(_["image"])
				except:
					image_result[n] = [_["image"]]
		
		
	# set keyword value
	if keyword == None:
		keyword = ""

	# search attraction
	attraction_result = db.Search_attraction(
		id_start = attraction_range[0],
		id_end = attraction_range[1],
		keyword = keyword
	)
	# orgainze response
	response = {
		"nextPage": nextPage,
		"data": to_dict(
		attraction_result = attraction_result, 
		image_result = image_result
		)
	}
	return jsonify(response)

@app.route("/api/mrts")
def mrts():
	try:
		result = db.Search_mrt()
		mrt_list = [_["mrt_name"] for _ in result]
		response = {"data": mrt_list}
		return jsonify(response)
	
	except:
		response = {
			"error": True,
			"message": "The database is empty."
		}
		return jsonify(response), 500


app.run(host="0.0.0.0", port=3000, debug=True)