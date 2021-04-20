# from pymongo import MongoClient
import pymongo
from flask import Flask, request, Response, jsonify, json, send_file
import base64
import random
import string
import secrets

import os

import numpy as np
import cv2
import requests


from image_processing import ImageProcess


# 以下、機械学習
import i2v
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model('pck_model_activationSigmoid.h5', compile=False)
illust2vec = i2v.make_i2v_with_chainer("illustration2vec/"+"illust2vec_ver200.caffemodel")


CASH = []

class Api():
    def __init__(self):
        pass


    def mongo_init():
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        c = client.list_database_names()
        return c
    

    def get_color_list(colorNum, img, filename):
        # バイト列をnumpy配列に
        img_stream = base64.b64decode(img)

        img_array = np.asarray(bytearray(img_stream), dtype=np.uint8)
        img_bgr = cv2.imdecode(img_array, 3)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        img_bgr = ImageProcess.byte2np(img)
        colors = ImageProcess.get_color_list(img_bgr, int(colorNum))


        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        result_real = illust2vec.extract_feature([img_rgb])
        pre = model.predict(result_real)
        pre = float(pre[0][0])
        if pre > 0.5:
            pre = 'animal'
        else:
            pre = 'person'


        # predict した結果もワラップする
        res = {"color" : colors}
        res = {"color" : colors, "classification" : pre}
        return jsonify(res)


    def get_main_recipes(uuid, colors, db):
        col = db['main_recipe_collection']
        return_data = {"recipe" : []}

        arry = []

        allergys = Api.get_allergys_list(uuid, db)
        hate_vegetables = Api.get_hate_vegetables_list(uuid, db)
        
        for color in colors:
            r = col.find_one({'color':color},{'_id':0})
            if r['id'] == 15:
                arry.append(r)
                continue
                
                
            recipe_num =col.count_documents({'$and' : [{'material':{'$nin':allergys}}, {'color':color}, {'material':{'$in':hate_vegetables}}]})

            if recipe_num == 0:
                recipe_num = col.count_documents({'$and' : [{'material':{'$nin':allergys}}, {'color':color}]})
                res_index = random.randint(0, recipe_num - 1)
                color_recipes = col.find({'$and' : [{'material':{'$nin':allergys}}, {'color':color}]}, {'_id':0})
                res_recipe = color_recipes[res_index]
            else:
                res_index = random.randint(0, recipe_num - 1)
                color_recipes = col.find({'$and' : [{'material':{'$nin':allergys}}, {'color':color}, {'material':{'$in':hate_vegetables}}]}, {'_id':0})
                res_recipe = color_recipes[res_index]

            # res_recipeのドキュメントからedam_idをとりだしapiをたたく
            # res_recipeのmaterial, color, rgb, id
            # edamからurl, title, imageをとりだしpack
            edam_id = res_recipe['edam_id']

            res_recipe['image'], res_recipe['title'], res_recipe['url'] = Api.get_by_edam(edam_id)

            print(color, 'FALSE')

            arry.append(res_recipe)
        
        arry = sorted(arry, key=lambda x: x['color'])
        
        return_data["recipe"] = arry

        return jsonify(return_data)



    def get_hate_vegetables_list(uuid, db):
        hate_col = db["hete_vegetable_collection"]
        hate_vegetable = hate_col.find_one({'uuid':uuid}, {'_id':0, 'uuid':0})

        pairs = hate_vegetable["hate_vegetable"]

        hate_vegetables = []
        for pair in pairs:
            if pair['hate']:
                hate_vegetables.append(pair["name"])
        
        return hate_vegetables


    def get_allergys_list(uuid, db):
        alle_col = db["allergens_collection"]

        alle = alle_col.find_one({'uuid':uuid}, {'_id':0, 'uuid':0})

        pairs = alle["allergens"]

        allergys = []
        for pair in pairs:
            if pair['aler']:
                allergys.append(pair["name"])
        
        return allergys

    
    def get_sub_recipes(uuid, sub_recipes_type, imageType, db):
        return_data = {'recipes' : []}
        if sub_recipes_type == 'meat':
            col = db['meat_recipe_collection']
        else:
            col = db['vegetable_recipe_collection']

        charactor_col = db["charactor_side_collection"]
        recipe_num = charactor_col.count_documents({'$and' : [{'image_type':imageType}, {'dish_type':sub_recipes_type}]})
        res_index = random.randint(0, recipe_num - 1)
        
        all_charactor_recipes = charactor_col.find({'$and' : [{'image_type':imageType}, {'dish_type':sub_recipes_type}]}, {"_id":0})
        in_recipe = all_charactor_recipes[res_index]

        return_data['recipes'].append(in_recipe)


        recipe_num =col.count_documents({})
        recipes = col.find({}, {'_id':0})

        l = list(range(0, recipe_num))
        random.shuffle(l)
        for i in l[0:2]:
            recipe = recipes[i]
            edam_id = recipe['edam_id']

            recipe['image'], recipe['title'], recipe['url'] = Api.get_by_edam(edam_id)
            
            return_data['recipes'].append(recipe)

        return return_data

    
    def get_sub_recipes_include_machine(uuid, sub_recipes_type, imageType, db):
        return_data = {'recipes' : []}
        if sub_recipes_type == 'meat':
            col = db['meat_recipe_collection']
        else:
            col = db['vegetable_recipe_collection']

        allergys = Api.get_allergys_list(uuid, db)
        hate_vegetables = Api.get_hate_vegetables_list(uuid, db)
        
        recipe_num =col.count_documents({})
        
        l = list(range(0, recipe_num))
        random.shuffle(l)
        for i in l[0:2]:
            recipe = recipes[i]
            edam_id = recipe['edam_id']
            recipe['image'], recipe['title'], recipe['url'] = Api.get_by_edam(edam_id)
            
            return_data['recipes'].append(recipe)

        return return_data


    def get_by_edam(edam_id):
        for c in CASH:
            if c['edam_id'] == edam_id:
                doc = c['doc']
                return (doc['image'], doc['label'], doc['url'])
        
        
        APP_ID = os.getenv('APP_ID')
        APP_KEY = os.getenv('APP_KEY')

        url = 'https://api.edamam.com/search'
        url += '?r=http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_'
        url += edam_id
        url += '&app_id={}&app_key={}'.format(APP_ID, APP_KEY)


        response = requests.get(url)
        res = response.json()

        if len(res) == 0:
            image = 'https://static.thenounproject.com/png/482114-200.png'
            title = 'ERROR'
            url = 'https://static.thenounproject.com/png/482114-200.png'
        else:
            image = res[0]['image']
            title = res[0]['label']
            url = res[0]['url']

            h = {
                'edam_id':edam_id,
                'doc' : {
                            'image':image,
                            'label':title,
                            'url' : url
                        }
                }
            CASH.append(h)


        return (image, title, url)

    

    # save & generate recipe_id
    def save_recipe(uuid, main_ids, meat_ids, vegetable_id, img, db):
        recipe_id = ''.join(secrets.choice(string.ascii_letters) for i in range(10))
        with open('fixtures/base_complete_recipe.json', mode="r", buffering=-1, encoding='utf-8') as f:
            complete_recipe = json.loads(f.read())

        complete_recipe["recipeId"] = recipe_id
        complete_recipe["uuid"] = uuid
        complete_recipe["image"] = img

        use_all_materials = []

        # sertch recipe by ID
        main_col = db['main_recipe_collection']
        meat_col = db['meat_recipe_collection']
        vegetable_col = db['vegetable_recipe_collection']

        for main_id in main_ids:
            recipe = main_col.find_one({'id':main_id}, {'_id':0})
            complete_recipe["mainRecipes"].append(recipe)

            use_all_materials += recipe['material']
        
        for meat_id in meat_ids:
            if meat_id > 100:
                charctor_col = db['charactor_side_collection']
                recipe = charctor_col.find_one({'id':meat_id}, {'_id':0})
            else:
                recipe = meat_col.find_one({'id':meat_id}, {'_id':0})
                
            complete_recipe["subRecipes"]["meat"].append(recipe)

            use_all_materials += recipe['material']
        
        if vegetable_id < 100:
            recipe = vegetable_col.find_one({"id":vegetable_id}, {"_id":0})
        else:
            charctor_col = db['charactor_side_collection']
            recipe = charctor_col.find_one({'id':vegetable_id}, {'_id':0})

        complete_recipe["subRecipes"]["vegetable"] = recipe
        use_all_materials += recipe['material']

        use_all_materials = list(set(use_all_materials))

        
        complete_recipe['useAllMaterials'] = use_all_materials


        # save
        col = db["complete_recipe_collection"]
        _ = col.insert_one(complete_recipe)

        return recipe_id

    def get_index(uuid, db):
        col = db["complete_recipe_collection"]
        all_recipes = col.find({'uuid':uuid}, {'_id':0})

        res = {'recipes' : []}
        for recipe in all_recipes:
            res['recipes'].append({'recipeId':recipe['recipeId'], 'image':recipe['image']})

        return jsonify(res)


    def select_recipe(uuid, recipeId, db):
        res = {"recipe" : {}}

        col = db['complete_recipe_collection']
        complete_recipe = col.find_one({'recipeId' : recipeId}, {'_id':0})

        # attir manRecipes, subRecipes[vegetable], subRecipes[meat]
        # material
        for i, main_recipe in enumerate(complete_recipe['mainRecipes']):
            if main_recipe['id'] == 15:
                complete_recipe['mainRecipes'][i] = main_recipe
                print('CONTINUE')
                continue
            
            edam_id = main_recipe['edam_id']

            main_recipe['image'], main_recipe['title'], main_recipe['url'] = Api.get_by_edam(edam_id)

            complete_recipe['mainRecipes'][i] = main_recipe
        
        for i, meat_recipe in enumerate(complete_recipe['subRecipes']['meat']):

            if meat_recipe['id'] < 100:
                edam_id = meat_recipe['edam_id']

                meat_recipe['image'], meat_recipe['title'], meat_recipe['url'] = Api.get_by_edam(edam_id)

            
            complete_recipe['subRecipes']['meat'][i] = meat_recipe


        vegetable_recipe = complete_recipe['subRecipes']['vegetable']

        if vegetable_recipe['id'] < 100:
            edam_id = vegetable_recipe['edam_id']
            vegetable_recipe['image'], vegetable_recipe['title'], vegetable_recipe['url'] = Api.get_by_edam(edam_id)



        res["recipe"] = complete_recipe


        return jsonify(res)



    def get_allergens(uuid, db):
        col = db["allergens_collection"]
        datas = col.find_one({'uuid':uuid}, {'_id':0, 'uuid':0})
        
        return jsonify(datas)
    

    def get_hate_meterial(uuid, db):
        col = db["hete_vegetable_collection"]
        datas = col.find_one({'uuid':uuid}, {'_id':0, 'uuid':0})

        return jsonify(datas)
    

    def update_allergens(allergens, uuid, db):
        col = db["allergens_collection"]
        col.delete_one({"uuid" : uuid})
        col.insert_one(allergens)

        return 'secceed'
    

    def update_hate_material(hate_vegetable, uuid, db):
        col = db["hete_vegetable_collection"]
        col.delete_one({"uuid":uuid})
        col.insert_one(hate_vegetable)

        return 'secceed'


    def get_eat_times(uuid, db):
        col = db["eat_times_collection"]
        datas = col.find_one({}, {'_id':0, 'uuid':0})
        
        return jsonify(datas)

        
    def reload_main_recipes(uuid, color, another_color_recipe_id, db):
        col = db['main_recipe_collection']
        return_data = {"recipe" : []}
        arry = []        

        for id in another_color_recipe_id:
            res_recipe = col.find_one({'id' : id}, {'_id':0})
            arry.append(res_recipe)


        recipe_num =col.count_documents({'color':color})
        res_index = random.randint(0, recipe_num - 1)

        color_recipes = col.find({'color':color}, {'_id':0})
        res_recipe = color_recipes[res_index]
        arry.append(res_recipe)


        arry = sorted(arry, key=lambda x: x['color'])
        
        return_data["recipe"] = arry

        return jsonify(return_data)