import json
from MySQLTool import MySQLTool

with open('data/taipei-attractions.json', mode = "r") as file:
    result = file.read()
    data = json.loads(result)['result']['results']

# 1. database called taipei_travel
# 2. create two tables :
#   2-a. attraction : id, name, CAT, description, MRT, address, direction
#   2-b. image : id, foreign_key (attractions's id), img_url

# ------ 2-a. organize data for table "attractions" -----
attractions = []
for _ in data:

    # append orgaized data to "attraction" list
    info = {
        "name": _["name"],
        "category": _["CAT"],
        "description": _["description"],
        "address": _["address"],
        "transport": _["direction"],
        "mrt": _["MRT"],
        "lat": _["latitude"],
        "lng": _["longitude"]
    }
    attractions.append(info)

# db = MySQLTool(attractions_to_update = attractions)
# db.Update_attraction()


# ----- 2-b. organize data for table "image" -----
images = []
id = 0
for _ in data:
    id += 1
    # delete img files which are not JPG or PNG
    file = _["file"]
    file_list = file.split("https://")

    for file in file_list:
        if len(file) >= 4 and (file[-4:].lower() == ".jpg" or file[-4:].lower() == ".png"):
            url = "https://" + file

            # append orgaized data to "attraction" list
            info = {
                "id": id,
                "image": url
            }
            images.append(info)

# db = MySQLTool(images_to_update = images)
# db.Update_image()



