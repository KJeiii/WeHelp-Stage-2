from TaipeiTravel import app
import jwt, os
from flask import request, jsonify, render_template
from TaipeiTravel.models import ItineraryTool

itinTool = ItineraryTool.itineraryTool()


		
# ----- Itienrary API -----

@app.route("/api/booking", methods = ["GET", "POST", "DELETE"])
def itinerary():
	BearerJWT = request.headers.get("authorization")

	# Deny access to API when BearerJWT is not provided
	if BearerJWT == None:
		response = {
			"error": True,
			"message": "未登入系統，拒絕存取"
		}
		return jsonify(response), 403

	# GET for searching itinerary
	if request.method == "GET":
		try:
			JWT = request.headers.get("authorization").split(" ")[1]
			payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")
			itinerary = itinTool.SearchItinerary(payload["usi"])

			# response empty data if there is no booked itinerary
			if len(itinerary) == 0:
				response = {
					"data": None
				}
				return jsonify(response), 200

			# response data if there is booked itinerary
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

		except Exception as error:
			print(f'Error in itinerary(GET) : {error}')
			response = {
				"error": True,
				"message": "伺服器內部錯誤"
			}
			return jsonify(response), 500
		
	# POST for creating new itinerary and update old one
	if request.method == "POST":
		try:
			JWT = request.headers.get("authorization").split(" ")[1]
			payload = jwt.decode(JWT, os.environ.get("JWTsecret"), algorithms = "HS256")
			# print(request.json)

			try: 
				# 1. update itinerary if user has already booked
				# 2. otherwise; create itinerary
				itinTool.UpdateItinerary(
					user_id = payload["usi"],
					attraction_id = int(request.json["attraction_id"]),
					date = request.json["date"],
					time = request.json["time"],
					price = int(request.json["price"])
				)
				response = {
					"ok": True
				}
				return jsonify(response), 200
			
			except Exception as error:
				print(f'Error in itinerary(POST)-update itinerary : {error}')
				response = {
					"error": True,
					"message": "建立失敗，輸入不正確或其他原因"
				}
				return jsonify(response), 400
			
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


