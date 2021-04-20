from flask import Flask, jsonify, request, Response, make_response
from bson.json_util import dumps
from api import Api
import json
import pymongo



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.development



# 写真を貰い、色リストを返す
@app.route("/api/getColorList", methods=['POST'])
def api_get_color_list():
    uuid = request.form['uuid']
    colorNum = request.form['colorNum']
    img = request.form['picture']
    filename = request.form['filename']

    # form内容をcast
    return Api.get_color_list(colorNum, img, filename)


@app.route("/api/getMainRecipes", methods=['POST'])
def api_get_mainrecipes():
    colors = request.form['color']
    uuid = request.form['uuid']

    colors = colors.split(',')

    return Api.get_main_recipes(uuid, colors, db)




@app.route("/api/getSubRecipes/<string:uuid>/<string:subRecipesType>/<string:imageType>", methods=['GET'])
def api_get_subrecipes(uuid, subRecipesType, imageType):
    return Api.get_sub_recipes(uuid, subRecipesType, imageType, db)


@app.route("/api/saveRecipe", methods=['POST'])
def api_save_recipe():
    uuid = request.form['uuid']
    vegetable_id = int(request.form['vegetable_id'])
    img = request.form['img']

    # main&meat is like '1,2,3'
    main_id = request.form['main_id']
    meat_id = request.form['meat_id']

    main_ids = main_id.split(',')
    for i, m in enumerate(main_ids):
        main_ids[i] = int(m)

    meat_ids = meat_id.split(',')
    for i, m in enumerate(meat_ids):
        meat_ids[i] = int(m)

    # save & generate RecipeId
    recipe_id = Api.save_recipe(uuid, main_ids, meat_ids, vegetable_id, img, db)

    return Api.select_recipe(uuid, recipe_id, db)


@app.route("/api/recipeIndex/<string:uuid>", methods=['GET'])
def api_get_index(uuid):
    return Api.get_index(uuid, db)


@app.route("/api/selectRecipe/<string:uuid>/<string:recipeId>", methods=['GET'])
def api_select_recipe(uuid, recipeId):
    return Api.select_recipe(uuid, recipeId, db)


@app.route("/api/getAllergens/<string:uuid>", methods=['GET'])
def api_get_allergens(uuid):
    return Api.get_allergens(uuid, db)


@app.route("/api/updateAllergens", methods=['POST'])
def api_update_allergens():
    allergens = json.loads(request.json)
    uuid = allergens['uuid']

    return Api.update_allergens(allergens, uuid, db)

@app.route("/api/getHateMaterial/<string:uuid>", methods=['GET'])
def api_get_hate_material(uuid):
    return Api.get_hate_meterial(uuid, db)


@app.route("/api/updateHateVegetable", methods=['POST'])
def api_update_hate_vegetable():
    hate_vegetable = json.loads(request.json)
    uuid = hate_materials['uuid']

    return Api.update_hate_material(hate_vegetable, uuid, db)


@app.route("/api/getEatTimes/<string:uuid>", methods=['GET'])
def api_get_eat_times(uuid):
    return Api.get_eat_times(uuid, db)
    

@app.route("/api/reloadMainRecipes", methods=['POST'])
def api_reload_main_recipes():
    color = request.form['color']
    uuid = request.form['uuid']

    another_color_recipe_id = request.form['another_color_recipe_id']
    another_color_recipe_id = another_color_recipe_id.split(',')
    for i, c in enumerate(another_color_recipe_id):
        another_color_recipe_id[i] = int(c)

    return Api.reload_main_recipes(uuid, color, another_color_recipe_id, db)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)