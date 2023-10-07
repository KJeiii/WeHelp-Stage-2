from flask import *
import TaipeiTravel.AttractionTool, TaipeiTravel.MemberTool, TaipeiTravel.ItineraryTool, TaipeiTravel.PaymentTool
import math, jwt, os, requests, json
from werkzeug.security import generate_password_hash, check_password_hash
import datetime as dt


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.json.ensure_ascii = False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# use TaipeiTravel module package 
attrTool = TaipeiTravel.AttractionTool.attrTool()
memberTool = TaipeiTravel.MemberTool.memberTool()
itinTool = TaipeiTravel.ItineraryTool.itineraryTool()
paymentTool = TaipeiTravel.PaymentTool.PaymentTool()

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

# ------ Attraction API -------
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


# ------ Member API -------

@app.route("/api/user", methods = ["POST"])
def signup():
	if request.method == "POST":
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
		
# ----- Itienrary API -----

@app.route("/api/booking", methods = ["GET", "POST", "DELETE"])
def itinerary():
	BearerJWT = request.headers.get("authorization")

	# Allow request API when BearerJWT is provided
	if BearerJWT != None:

		# GET for searching itinerary
		if request.method == "GET":
			try:
				JWT = request.headers.get("authorization").split(" ")[1]
				payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")


				itinerary = itinTool.SearchItinerary(payload["usi"])
				if len(itinerary) > 0:
					itinerary_info = itinerary[0]
					response = {
						"data": {
							"attraction": {
								"id": itinerary_info["attraction_id"],
								"name": itinerary_info["attraction_name"],
								"address": itinerary_info["address"],
								"image": itinerary_info["images"].replace("[", "").replace("]", "").replace('"',"").split(", ")[0]
							},
						"date": itinerary_info["date"],
						"time": itinerary_info["time"],
						"price": itinerary_info["price"]
						}
					}
					return jsonify(response), 200
				else:
					response = {
						"data": None
					}
					return jsonify(response), 200

			
			except Exception as error:
				print(f'Error in itinerary(GET) : {error}')
				response = {
					"error": True,
					"message": "伺服器內部錯誤"
				}

				return jsonify(response), 500

		# POST for creating new itinerary
		if request.method == "POST":
			try:
				JWT = request.headers.get("authorization").split(" ")[1]
				payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")
				print(request.json)

				try: 
					# check whether user has already booked itinerary
					if len(itinTool.SearchItinerary(user_id = payload["usi"])) > 0:

						itinTool.UpdateItinerary(
							user_id = payload["usi"],
							attraction_id = int(request.json["attraction_id"]),
							date = request.json["date"],
							time = request.json["time"],
							price = int(request.json["price"])
						)
					else:
						itinTool.CreateItinerary(
						user_id = payload["usi"],
						attraction_id = int(request.json["attraction_id"]),
						date = request.json["date"],
						time = request.json["time"],
						price = int(request.json["price"])
						)
				except Exception as error:
					print(f'Error in itinerary(POST)-update itinerary : {error}')
					response = {
						"error": True,
						"message": "建立失敗，輸入不正確或其他原因"
					}
					return jsonify(response), 400

				else:
					response = {
						"ok": True
					}
					return jsonify(response), 200
			
			except Exception as error:
				print(f'Error in itinerary(POST) : {error}')
				response = {
					"error": True,
					"message": "伺服器內部錯誤"
				}
				return jsonify(response), 500
			
		# DELETE itinerary
		if request.method == "DELETE":
			try:
				JWT = request.headers.get("authorization").split(" ")[1]
				payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")

				itinTool.DeleteItinerary(user_id = payload["usi"])

				response = {
					"ok": True
				}
				return jsonify(response), 200

			except Exception as error:
				print(f'Error in itinerary(DELETE) : {error}')

	
	# Deny access to API when BearerJWT is not provided
	response = {
		"error": True,
		"message": "未登入系統，拒絕存取"
	}

	return jsonify(response), 403


# ----- payment API -----
@app.route("/api/orders", methods = ["POST"])
def payment():
	BearerJWT = request.headers.get("authorization")

	# Deny access to API when BearerJWT is not provided
	if BearerJWT == None:
		response = {
			"error": True,
			"message": "未登入系統，拒絕存取"
		}
		return jsonify(response), 403
	
	try:
		JWT = request.headers.get("authorization").split(" ")[1]
		payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")

		# Return 400 if one of prime, name, email, phone is empty.
		order_info = request.json
		conditions_for_create_order = [
			order_info["prime"],
			order_info["contact"]["name"],
			order_info["contact"]["email"],
			order_info["contact"]["phone"]
		]
		
		if "" in conditions_for_create_order:
			response = {
				"error": True,
				"message": "訂單建立失敗，輸入不正確或其他原因"
			}
			return jsonify(response), 400
		
		POST_request_headers = {
			"Content-Type": "application/json",
			"x-api-key": "partner_GTkXXVJq79qyvWZvJfM9I5sv3wSOv69IW13f7a3TXHyKse6kLaQidEGr"
		}

		POST_request_body = {
			"prime": order_info["prime"],
			"partner_key": "partner_GTkXXVJq79qyvWZvJfM9I5sv3wSOv69IW13f7a3TXHyKse6kLaQidEGr",
			"merchant_id": "mark81816_ESUN",
			"amount": order_info["order"]["price"],
			"order_number": dt.datetime.now().strftime("%Y%m%d%I%M%S"),
			"bank_transaction_id": f"BTID{dt.datetime.now().strftime('%Y%m%d%I%M%S')}",
			"details": f"{order_info['order']['trip']['attraction']['name']}{order_info['order']['trip']['date']}{order_info['order']['trip']['time']}",
			"cardholder": {
				"phone_number": f"{order_info['contact']['phone']}",
				"name": f"{order_info['contact']['name']}",
				"email": f"{order_info['contact']['email']}",
				"zip_code": "",
				"address": "",
				"national_id": "",
			},
			"product_image_url": order_info['order']['trip']['attraction']['image']
			# "three_domain_secure": True,
			# "result_url": {
			# 	"frontend_redirect_url": url_for("thankyou"),
			# 	"backend_notify_url": url_for("itinerary"),
			# 	"go_back_url": url_for("itinerary")
			# }
		}

		tappay_response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime',
						json = POST_request_body,
						headers = POST_request_headers)
		payment_response = tappay_response.json()
		# print(tappay_response.status_code, payment_response)

		# create data in database (payment table)
		paymentTool.CreatePayment(
								payment_id = int(POST_request_body["order_number"]),
								user_id = int(payload["usi"]),
								phone = f"{order_info['contact']['phone']}",
								payment_status = payment_response["status"]
								)

		# return payment status and message 
		payment_status = payment_response["status"]
		payment_message = "付款成功"
		if payment_response["status"] != 0:
			payment_message = "付款失敗"

		response = {
			"data": {
				"number": payment_response["order_number"],
				"payment": {
					"status": payment_status,
					"message": payment_message}
					}}
		return jsonify(response), 200
	
	except Exception as error:
		print(error)
		response = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(response), 500



app.run(host="0.0.0.0", port=3000, debug=True)