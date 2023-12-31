import math
from flask import request, jsonify, Blueprint, render_template
from TaipeiTravel.models import AttractionTool

attrTool = AttractionTool.attrTool()
attraction_bp = Blueprint("attraction_bp", 
						  __name__, 
						  template_folder="templates",
						  static_folder="static")


# ------ Attraction API -------
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

@attraction_bp.route("/api/attractions")
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
						image_result[id].attraction_bpend(_["image"])
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
	


@attraction_bp.route("/api/attraction/<attraction_id>")
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

 
@attraction_bp.route("/api/mrts")
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

