import json

data = {
    "name": "Белый хозяин",
    "id": 2,
    "face_image": [
        "face/white1.png",
        "face/white2.png"
    ]
}

with open('data1.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)