from TaipeiTravel import app
from TaipeiTravel.models import MemberTool
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, render_template
import datetime as dt
import jwt, os


memberTool = MemberTool.memberTool()

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


