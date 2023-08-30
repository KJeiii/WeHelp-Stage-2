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
		"img":''
	} for _ in attraction_result]
	print(image_result)
	return data

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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


@app.route("/api/attractions")
def attractions():

	# A. according to page parameter, 
	# 1. caculate id 
	# 2. select data in attraction table by id column

	# B. filter data after step A,
	# 1. if keyword input is empty, do not filter;
	# 2. otherwise, exact match mrt name in mrt table, or fuzzily match attraction name in attraction table

	page  = int(request.args.get("page"))
	keyword = request.args.get("keyword")
	db = MySQLTool()

	total_attraction_amount = db.total_attractions()
	total_pages = int(round(total_attraction_amount/12, 0)) - 1

	if page == None:
		response = {
			"error": True,
			"message": f'please provide page parameter ranged from 0 to {total_pages}.'
		}
		return jsonify(response)
		
	if page > total_pages:
		response = {
			"error": True,
			"message": f'maximum page is {total_pages}'
		}
		return jsonify(response)
	
	# set nextPage value
	attraction_range = (page*12+1, page*12+12)
	if page == 4:
		nextPage = "This is the last page."
	else:
		nextPage = page + 1

	# search image
	attraction_id_tuple = (_ for _ in range(attraction_range[0], attraction_range[1]+1))
	attraction_id_str = f'{str(attraction_id_tuple).replace("(","").replace(")","")}'
	image_result = db.Search_image(attraction_id = attraction_id_str)
		
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



app.run(host="0.0.0.0", port=3000, debug=True)