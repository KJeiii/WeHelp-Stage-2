import json
from MySQLTool import MySQLTool

with open('data/taipei-attractions.json', mode = "r") as file:
    result = file.read()
    data = json.loads(result)['result']['results']

# 1. database called taipei_travel
# 2. create 3 tables :
#   2-a. mrt : id, name, attraction amount
#   2-b. attraction : id, name, category, description, address, transport
#   2-c. image : id, foreign_key (attractions's id), img_url

# ------ 2-a. organize data for table "mrt" -----
mrts_raw = [_["MRT"] for _ in data]
mrts_set = set(mrts_raw)
mrts_and_attraction = { _ : mrts_raw.count(_) for _ in mrts_set }

mrts_dict = {} # create a dict for attraction table building foreign key
n = 0
for _ in mrts_set:
    n += 1
    mrts_dict[_] = {"id" : n,
                    "attraction_amount" : mrts_and_attraction[_]
                    }

mrts_list = [] # create for insert data to MySQL
for _ in mrts_dict:
        mrts__list_element  = {"name" : _,
                "id" : mrts_dict[_]["id"],
                "attraction_amount" : mrts_dict[_]["attraction_amount"]
             }
        mrts_list.append(mrts__list_element)
        
# db = MySQLTool(mrts_to_update = mrts_list)
# db.Update_mrt()


# ------ 2-b. organize data for table "attractions" -----
attractions_raw = [_["name"] for _ in data]
attractions_id_dict = {}  # create a dict for image table building foreign key
n = 0
for _ in attractions_raw:
    n += 1
    attractions_id_dict[_] = n

attractions_list = []
for _ in data:
    
    # append orgaized data to "attraction" list
    info = {
        "id": attractions_id_dict[_["name"]],
        "mrt_id": mrts_dict[_["MRT"]]["id"],
        "name": _["name"],
        "category": _["CAT"],
        "description": _["description"],
        "address": _["address"],
        "transport": _["direction"],
        "lat": _["latitude"],
        "lng": _["longitude"]
    }
    attractions_list.append(info)

# db = MySQLTool(attractions_to_update = attractions_list)
# db.Update_attraction()


# ----- 2-c. organize data for table "image" -----
images_list = []
for _ in data:
    # delete img files which are not JPG or PNG
    file = _["file"]
    file_list = file.split("https://")


    for file in file_list:
        if len(file) >= 4 and (file[-4:].lower() == ".jpg" or file[-4:].lower() == ".png"):
            url = "https://" + file

            # append orgaized data to "attraction" list
            info = {
                "attraction_id": attractions_id_dict[_["name"]],
                "image": url
            }
            images_list.append(info)

# db = MySQLTool(images_to_update = images_list)
# db.Update_image()




