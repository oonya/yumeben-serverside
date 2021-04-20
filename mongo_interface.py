import pymongo
import base64
import urllib.parse

# client = pymongo.MongoClient("mongodb://localhosttmp.jpg', 'rb')
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["development"]


col = db["charactor_side_collection"]





res = [
        {
            "id" : 1004,
            "title":"キャラ弁＊バレリーナの女の子♪",
            "url":"https://recipe.rakuten.co.jp/recipe/1350011467/?rtg=9494215cb616a6d26dc37fe6c7e0a021",
            "image" : 'dammy.jpg',
            "image_type" : "person",
            "dish_type" : "meat",
            "material" : ['ハム', 'チェダーチーズ', 'スライスチーズ']
        },
        {
            "id" : 1005,
            "title":"型抜きポテトサラダ",
            "url":"https://erecipe.woman.excite.co.jp/detail/30a3b0dec4b9c8c944412d8dfdc1a140.html",
            "image" : 'dammy.jpg',
            "image_type" : "animal",
            "dish_type" : "vegetable",
            "material" : ['ジャガイモ', 'ハム', 'ミックスベジタブル']
        },
        {
            "id" : 1006,
            "title":"お弁当の隙間埋め♡野菜バーガー",
            "url":"https://cookpad.com/recipe/3183032",
            "image" : 'dammy.jpg',
            "image_type" : "person",
            "dish_type" : "vegetable",
            "material" : ['ミニトマト', 'キュウリ']
        },
        {
            "id" : 1007,
            "title":"キャラ弁に！ストローで簡単！可愛い猫の手",
            "url":"https://cookpad.com/recipe/1159861",
            "image" : 'dammy.jpg',
            "image_type" : "animal",
            "dish_type" : "vegetable",
            "material" : ['ストロー']
        },
        {
            "id" : 1008,
            "title":"かわいい！きゅうりの飾り切り",
            "url":"https://recipe.rakuten.co.jp/recipe/1590001612/?l-id=r_recom_category",
            "image" : 'dammy.jpg',
            "image_type" : "person",
            "dish_type" : "vegetable",
            "material" : ['キュウリ']
        },
        {
            "id" : 1009,
            "title":"簡単❤ハムリボン",
            "url":"https://recipe.rakuten.co.jp/recipe/1400000975/?l-id=r_recom_category",
            "image" : 'dammy.jpg',
            "image_type" : "person",
            "dish_type" : "meat",
            "material" : ['ハム']
        },
        {
            "id" : 1010,
            "title":"お弁当やキャラ弁に♥ハムとチーズでバラ",
            "url":"https://recipe.rakuten.co.jp/recipe/1400005940/?rtg=9494215cb616a6d26dc37fe6c7e0a021",
            "image" : 'dammy.jpg',
            "image_type" : "person",
            "dish_type" : "meat",
            "material" : ['ハム', 'スライスチーズ']
        }
]

# col.insert_many(res)


col = db["main_recipe_collection"]

res = {
    "id":15,
    "color" : "blue",
    "rgb" : [0, 0, 255],
    "material" : ['卵白', '紫芋', 'マヨネーズ'],
    "url" : "https://cookpad.com/recipe/670503",
    "title" : "水色の薄焼き卵",
    "image" : "",
    "edam_id" : ""
}

col.insert_one(res)



res = [
    {
        "id":7,
        "color":"green",
        "rgb" : [0, 255, 0],
        "material" : ['アスパラガス', '味噌', 'ニンニク'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id': '4a47b500e903f215e3afaad15aaf6626'
    },
    {
        "id":8,
        "color":"brown",
        "rgb" : [205, 133, 63],
        "material" : ['松茸', '七面鳥', 'ニンニク', 'ネギ', 'レタス'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id' : '6f49ca81706424e341df0d4c19742d7d'
    },
    {
        "id":9,
        "color":"green",
        "rgb" : [0, 255, 0],
        "material" : ['インゲン', '味噌', 'ニンニク'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id' : '10cf3ed0056b80a3348518afa50b405a'
    },
    {
        "id":10,
        "color":"brown",
        "rgb" : [205, 133, 63],
        "material" : ['白みそ', 'ゴボウ'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id' : '91e365d5fff27decb59749087fb6c132'
    },
    {
        "id":11,
        "color":"orange",
        "rgb" : [255, 165, 0],
        "material" : ['ジャガイモ', 'パセリ', '卵'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id' : '3d8c9ae4e10a9740a24b68bc1a89d53b'
    },
    {
        "id":12,
        "color":"pink",
        "rgb" : [255, 102, 204],
        "material" : ['レモン', 'ミニトマト', '卵'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id' : 'c0c2e8c72c49b22b2790d7739b735466'
    },
    {
        "id":13,
        "color":"pink",
        "rgb" : [255, 102, 204],
        "material" : ['レモン', 'ミニトマト', '卵'],
        "url":"dammy.com",
        'title':'dammy',
        'image':'dammy.jpg',
        'edam_id' : 'c0c2e8c72c49b22b2790d7739b735466'
    }
]

# col.insert_many(res)



# res = [
#     {
#         "id" : 1,
#         "material" : ['サツマイモ'],
#         "title":'ダミー',
#         'image' : 'dammy.jpg',
#         "url":'dammy.com',
#         "edam_id" : 'http://www.edamam.com/ontologies/edamam.owl#recipe_76d180d8b5185e9e3e206259c2eff508'
#     },
#     {
#         "id" : 2,
#         "material" : ['カブ'],
#         "title":'ダミー',
#         'image' : 'dammy.jpg',
#         "url":'dammy.com',
#         "edam_id" : '6e592a9ee6e702ebf7c94b40d8ddf143'
#     },
#     {
#         "id" : 3,
#         "material" : ['トマト', 'インゲン', 'チーズ'],
#         "title":'ダミー',
#         'image' : 'dammy.jpg',
#         "url":'dammy.com',
#         "edam_id" : '6e2a6d5cedd07fbc912539e34f8ca093'
#     }
# ]

# res = {
#     "uuid" : "firstUser",
#     "eat_times" : [
#         { "name" : "パプリカ", "times" : 4 },
#         { "name" : "ニンジン", "times" : 5 },
#         { "name" : "ピーマン", "times" : 1 },
#         { "name" : "アスパラ", "times" : 3 }
#     ]
# }
# col.insert_one(res)


# col.insert_one({"name":"パプリカ", "times":4})
# col.insert_one({"name":"ニンジン", "times":5})
# col.insert_one({"name":"ピーマン", "times":1})
# col.insert_one({"name":"アスパラ", "times":3})



# main_recipe = {
#     "id" : 4,
#     'image' : img_base64,
#     "material" : ['ごぼう', 'ニンジン', 'ごま油'],
#     "title" : "キンピラごぼう",
#     "url" : "https://ec.crypton.co.jp/pages/prod/virtualsinger/cv01"
# }

# x = col.insert_one(main_recipe)


# res = {
#     "uuid" : "firstUser",
#     "allergens" : [
#         { "name" : "えび", "aler" : False },
#         { "name" : "かに", "aler" : False },
#         { "name" : "小麦", "aler" : False },
#         { "name" : "そば", "aler" : False },
#         { "name" : "卵", "aler" : False },
#         { "name" : "乳", "aler" : False },
#         { "name" : "落花生", "aler" : False },
#         { "name" : "あわび", "aler" : False },
#         { "name" : "いか", "aler" : False },
#         { "name" : "いくら", "aler" : False },
#         { "name" : "オレンジ", "aler" : False },
#         { "name" : "カシューナッツ", "aler" : False },
#         { "name" : "キウイフルーツ", "aler" : False },
#         { "name" : "牛肉", "aler" : False },
#         { "name" : "くるみ", "aler" : False },
#         { "name" : "ごま", "aler" : False },
#         { "name" : "さけ", "aler" : False },
#         { "name" : "さば", "aler" : False },
#         { "name" : "大豆", "aler" : False },
#         { "name" : "鶏肉", "aler" : False },
#         { "name" : "バナナ", "aler" : False },
#         { "name" : "豚肉", "aler" : False },
#         { "name" : "まつたけ", "aler" : False },
#         { "name" : "もも", "aler" : False },
#         { "name" : "やまいも", "aler" : False },
#         { "name" : "りんご", "aler" : False },
#         { "name" : "ゼラチン", "aler" : False }
#     ]
# }
# col.insert_one(res)