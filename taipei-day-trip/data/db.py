import json

with open('data/taipei-attractions.json', mode = "r") as file:
    result = file.read()
    data = json.loads(result)['result']['results']

# 1. database called taipei_travel
# 2. create two tables :
#   2-a. attraction : id, name, CAT, description, MRT, address, direction
#   2-b. image : id, foreign_key (attractions's id), img_url

# 2-a. organize data for table "attractions"
attraction = []
for _ in data:

    # append orgaized data to "attraction" list
    info = {
        "name": _["name"],
        "CAT": _["CAT"],
        "description": _["description"],
        "MRT": _["MRT"],
        "address": _["address"],
        "diretion": _["direction"]
    }
    attraction.append(info)

# 2-b. organize data for table "image"
image = []
id = 0
for _ in data:
    id += 1

    # delete img files which are not JPG or PNG
    file = _["file"]
    file_list = file.split("https://")

    img_url = []
    for file in file_list:
        if len(file) >= 4 and (file[-4:].lower() == ".jpg" or file[-4:].lower() == ".PNG"):
            url = "https://" + file
            img_url.append(url)

    # append orgaized data to "attraction" list
    info = {
        "id": id,
        "image": img_url
    }
    image.append(info)

# print(attraction)
print(image)

