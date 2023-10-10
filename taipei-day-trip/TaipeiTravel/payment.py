from TaipeiTravel import app
import jwt, os, requests
from flask import request, jsonify, render_template
from TaipeiTravel.models import PaymentTool, ItineraryTool
import datetime as dt


paymentTool = PaymentTool.PaymentTool()
itinTool = ItineraryTool.itineraryTool()


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
			"x-api-key": os.environ.get("tappay_partner_key")
		}

		POST_request_body = {
			"prime": order_info["prime"],
			"partner_key": os.environ.get("tappay_partner_key"),
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

		# return payment status and message 
		payment_status = payment_response["status"]
		payment_message = "付款成功"
		payment_description_mysql = "已付款"
		if payment_response["status"] != 0:
			payment_message = "付款失敗"
			payment_description_mysql = "未付款"

		# create data in payment table and delete bookd itinerary
		paymentTool.CreatePayment(
								payment_id = int(POST_request_body["order_number"]),
								user_id = int(payload["usi"]),
								phone = f"{order_info['contact']['phone']}",
								payment_status = payment_description_mysql
								)
		itinTool.DeleteItinerary(user_id = payload["usi"])
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

@app.route("/api/order/<orderNumber>", methods = ["GET"])
def show_order(orderNumber):
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
		payment_info = paymentTool.SearchPayment(payment_id = orderNumber)
		
		status = 0
		if payment_info["payment_status"] != "已付款":
			status = 1

		response = {
			"data": {
				"number": payment_info["payment_id"],
				"price": payment_info["price"],
				"trip": {
					"attraction": {
						"id": payment_info["attraction_id"],
						"name": payment_info["attraction_name"],
						"address": payment_info["address"],
						"image": payment_info["image"]
					},
					"date": payment_info["date"],
					"time": payment_info["time"]
				},
				"contact": {
					"name": payload["usn"],
					"email": payload["eml"],
					"phone": payment_info["phone"]
				},
				"status": status
			}
		}
		return jsonify(response), 200

	except Exception as error:
		print(error)
		raise error

