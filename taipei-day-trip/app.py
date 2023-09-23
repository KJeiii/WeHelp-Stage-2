from flask import *
import TaipeiTravel.AttractionTool, TaipeiTravel.MemberTool
import math
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
import datetime as dt


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.json.ensure_ascii = False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# build MySQL connection
attrTool = TaipeiTravel.AttractionTool.attrTool()
memberTool = TaipeiTravel.MemberTool.memberTool()

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

# ----------  API  ----------  
# ------ Attraction -------
@app.route("/api/attractions")
def attractions():

	try: 
		# parse parameters
		page  = int(request.args.get("page"))
		keyword = request.args.get("keyword")

		# count total data and total pages matching keyword 
		if keyword == None:
			keyword = ""
		total_attraction_amount = attrTool.total_attractions(keyword = keyword)
		total_pages = int(math.ceil(total_attraction_amount/12))

		# build page_attraction_dict
		page_attraction_dict = {}
		count = total_attraction_amount
		for _ in range(total_pages):
			if count >= 12:
				page_attraction_dict[_] = 12
			else:
				page_attraction_dict[_] = count
			count -= 12
		# print(page_attraction_dict)

		# search MySQL data by keyword
		limit = (page*12, page_attraction_dict[page])
		# print(limit)
		attraction_result = attrTool.Search_attraction(keyword = keyword, limit = limit)

		# # set nextPage value
		if page + 1 == total_pages:
			nextPage = None
		else:
			nextPage = page + 1

		# # search image
		attraction_id_list = [_["attraction_id"] for _ in attraction_result]
		image_list = attrTool.Search_image(attraction_id_list=attraction_id_list)
		image_result = {}
		for id in attraction_id_list:
			for _ in image_list:
				if _["attraction_id"] == id:
					try:
						image_result[id].append(_["image"])
					except:
						image_result[id] = [_["image"]]

		# # orgainze response
		response = {
			"nextPage": nextPage,
			"data": to_dict(
			attraction_result = attraction_result, 
			image_result = image_result
			)
		}
		return jsonify(response)

	except:
		response = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(response), 500
	


@app.route("/api/attraction/<attraction_id>")
def attraction_by_id(attraction_id):
	# count total attractions data and total pages 
	total_attraction_amount = attrTool.total_attractions()

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
		
		# search attraction
		attraction_result = attrTool.Search_attraction(attraction_id = attraction_id)

		# search image
		attraction_id_list = [attraction_result[0]["attraction_id"]]

		image_list = attrTool.Search_image(attraction_id_list=attraction_id_list)
		image_result = {}
		for id in attraction_id_list:
			for _ in image_list:
				if _["attraction_id"] == id:
					try:
						image_result[id].append(_["image"])
					except:
						image_result[id] = [_["image"]]

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
		result = attrTool.Search_mrt()
		mrt_list = [_["mrt_name"] for _ in result]
		response = {"data": mrt_list}
		return jsonify(response)
	
	except:
		response = {
			"error": True,
			"message": "The database is empty."
		}
		return jsonify(response), 500


# ------ Member -------

@app.route("/api/user", methods = ["POST"])
def signup():
	# if request.method == "POST":
		user_name = request.json["user_name"]
		email = request.json["email"]
		password = generate_password_hash(request.json["password"])
		
		same_email_amount = len(memberTool.SearchMember(email = email))

		try:
			if same_email_amount == 0:
				memberTool.SignUp(
				user_name = user_name,
				email = email,
				password = password)

				response = {"ok": True}
				return jsonify(response), 200
			
			response = {
				"error": True,
				"message": "註冊失敗，重複的Email或其他原因"
			  }
			return jsonify(response), 400
		
		except:
			response = {
				"error": True,
				"message": "伺服器內部錯誤"
			}
			return jsonify(response), 500


@app.route("/api/user/auth", methods = ["PUT", "GET"])
def signin():
	if request.method == "PUT":
		try:
			email = request.json["email"]
			password = str(request.json["password"])

			# check if email is registered
			if len(memberTool.SearchMember(email)) != 0:
				member_info = memberTool.SearchMember(email)[0]
				hashed_password = member_info["password"]

				# check if password is correct
				if check_password_hash(hashed_password, password):
					payload = {
						"usi" : member_info["user_id"],
						"usn" : member_info["user_name"],
						"eml" : member_info["email"],
						"exp" : dt.datetime.utcnow() + dt.timedelta(days=7),
						"iat" : dt.datetime.utcnow()
					}


					JWT = jwt.encode(payload, os.environ.get("JWTsecret"), "HS256")

					response = {
						"token": JWT
					}
					return jsonify(response), 200
			
			response = {
				"error": True,
				"message": "登入失敗，帳號或密碼錯誤或其他原因"
			}
			return jsonify(response), 400

		except Exception as error:
			print(f'Error in SignIn (PUT) : {error}')
			response = {
				"error": True,
				"message": "伺服器內部錯誤"
			}
			return jsonify(response), 500
		
	if request.method == "GET":
		try: 
			JWT = request.headers.get("authorization").split(" ")[1]
			payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")
			response = {
				"data": {
					"id": payload["usi"],
					"name": payload["usn"],
					"email": payload["eml"]
				}
			}
			return jsonify(response), 200
		
		except Exception as error:
			print(f'Error in SignIn (GET) : {error}')
			response = {
				"data": None
			}
			return jsonify(response), 200

app.run(host="0.0.0.0", port=3000, debug=True)