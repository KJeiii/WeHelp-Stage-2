from flask import *
from MySQLTool import MySQLTool
import math

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.json.ensure_ascii = False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# build MySQL connection
db = MySQLTool()

# build funfciton for json format 
def to_dict(attraction_result:list, image_result:dict):
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
		"images": image_result[_["attraction_id"]]
	} for _ in attraction_result]
	return data

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

	# search MySQL data by keyword
	if keyword == None:
		keyword = ""
	attraction_result = db.Search_attraction(keyword = keyword)

	# count total data and total pages matching keyword 
	total_attraction_amount = len(attraction_result)
	total_pages = int(math.ceil(total_attraction_amount/12))

	# Search attraction and build page_attraction_dict 
	page_attraction_dict = {}
	count = total_attraction_amount
	for _ in range(total_pages):
		if count >= 12:
			for n in range(_*12, 12+_*12):
				try:
					page_attraction_dict[_].append(attraction_result[n])
				except:
					page_attraction_dict[_] = [attraction_result[n]]
		else:
			for n in range(_*12, _*12 + count):
				try:
					page_attraction_dict[_].append(attraction_result[n])
				except:
					page_attraction_dict[_] = [attraction_result[n]]	
		count -= 12

	# ------- Response error if page is not provided (page parameter is required) --------
	if page == None:
		response = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(response), 500

	# ------- Response error if page parameter exceeds maximum. ------
	page = int(page)
	if page > total_pages-1:
		response = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(response), 500
	
	# ------ Reponse data, if page parameter is given correctly. ------
	# set nextPage value
	if page + 1 == total_pages:
		nextPage = None
	else:
		nextPage = page + 1

	# search image
	attraction_id_list = [_["attraction_id"] for _ in page_attraction_dict[page]]
	image_list = db.Search_image(attraction_id_list=attraction_id_list)
	image_result = {}
	for id in attraction_id_list:
		for _ in image_list:
			if _["attraction_id"] == id:
				try:
					image_result[id].append(_["image"])
				except:
					image_result[id] = [_["image"]]
	print(image_result)
			
	# orgainze response
	response = {
		"nextPage": nextPage,
		"data": to_dict(
		attraction_result = page_attraction_dict[page], 
		image_result = image_result
		)
	}
	return jsonify(response)


@app.route("/api/attraction/<attraction_id>")
def attraction_by_id(attraction_id):
	# count total attractions data and total pages 
	total_attraction_amount = db.total_attractions()

	try:
		# ------- Response error if attraction_id is incorrect --------
		attraction_id = int(attraction_id)
		if attraction_id > total_attraction_amount or attraction_id <= 0:
			response = {
				"error": True,
				"message": '景點編號不正確'
			}
			return jsonify(response), 400
		
		# ------ Reponse data, if attraction_id is given correctly. ------
		# set keyword value
		keyword = ""

		# search attraction
		attraction_result = db.Search_attraction(
			id_start = attraction_id,
			id_end = attraction_id,
			keyword = keyword
		)

		# search image
		image_list = db.Search_image(
			attraction_id_start = attraction_id,
			attraction_id_end = attraction_id
		)

		image_result = {}
		for _ in image_list:
			try:
				image_result[attraction_id].append(_["image"])
			except:
				image_result[attraction_id] = [_["image"]]

		# orgainze response
		response = {
			"data": to_dict(
			attraction_result = attraction_result, 
			image_result = image_result
			)[0]
		}

		return response
	
	except:
	# ------- Response error --------
		response = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(response), 500

 
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