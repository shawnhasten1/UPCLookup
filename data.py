import requests
import json
from decimal import Decimal, InvalidOperation

class foodez(): 
    def __init__(self):
        print("Class Started")
        self.twoPlaces = Decimal('0.01')

    def _getDecimal(self, value):
        try:
            value = Decimal(value).quantize(self.twoPlaces)
        except:
            value = Decimal(0)
        return str(value)

    def getFood(self, upc):
        url = 'https://fdc.nal.usda.gov/portal-data/external/search'

        #input1 = input()
        #Monster 070847022909
        dataSent = {
            "generalSearchInput": str(upc)
            }
        requestHeader = {
                "Host": "fdc.nal.usda.gov",
                "Connection": "keep-alive",
                "Content-Length": "275",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://fdc.nal.usda.gov",
                "Sec-Fetch-Mode": "cors",
                "Content-Type": "application/json",
                "Sec-Fetch-Site": "same-origin",
                "Referer": "https://fdc.nal.usda.gov/fdc-app.html",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9"
        }

        req = requests.post(url, json=dataSent, headers=requestHeader)
        reqJson = req.json()

        fdcId = reqJson['foods'][0]['fdcId']
        foodData = {}
        foodNutrients = reqJson['foods'][0]['foodNutrients']
        foodIngredients = reqJson['foods'][0]['ingredients']

        foodData["ingredients"] = foodIngredients
        foodData['values'] = {}
        
        for x in range(0, len(foodNutrients)):
            nutr = foodNutrients[x]
            nutrLabel = nutr['nutrientName']
            value = str(nutr['value']) + " " + str(nutr['unitName'])
            foodData['values'][nutrLabel] = {'description' : nutr['derivationDescription'], 'value' : value}
        return foodData

    def getEdamam(self, upc):
        #04963406
        #04900000634
        #049000006346
        if len(str(upc)) == 8:
            definingDigit = upc[6]
            newUPC = ''
            if definingDigit == '0' or definingDigit == '1' or definingDigit == '2':
                newUPC = '0'+upc[1]+upc[2]+definingDigit+'0000'+upc[3]+upc[4]+upc[5]
            elif definingDigit == '3':
                newUPC = '0'+upc[1]+upc[2]+upc[3]+'00000'+upc[4]+upc[5]
            elif definingDigit == '4':
                newUPC = '0'+upc[1]+upc[2]+upc[3]+upc[4]+'00000'+upc[5]
            else:
                newUPC = '0'+upc[1]+upc[2]+upc[3]+upc[4]+upc[5]+'0000'+definingDigit
            
            check = 0
            total = 0
            for digit in newUPC:
                if check%2 == 0:
                    total = total + (int(digit)*3)
                else:
                    total = total + (int(digit)*1)
                check+=1

            checkDigit = 10-(total%10)
            
            upc = newUPC + str(checkDigit)
            print(upc)

        foodData = {}

        url = 'https://api.upcitemdb.com/prod/trial/lookup?upc='+ str(upc)
        req = requests.get(url)
        reqJson = req.json()
        try:
            img = reqJson['items'][0]['images'][0]
        except:
            img = None
        try:
            cleanName = reqJson['items'][0]['offers'][0]['title']
        except:
            cleanName = None

        url = 'https://api.edamam.com/api/food-database/v2/parser?upc='+ str(upc) +'&app_id=a5673f68&app_key=19e3c97afd04e087d29c808aaaa54418'

        #input1 = input()
        #Monster 070847022909
        

        req = requests.get(url)
        reqJson = req.json()
        try:
            foodID = reqJson["hints"][0]["food"]["foodId"]

            dataSent = {
                "ingredients": [
                    {
                    "quantity": 1,
                    "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_serving",
                    "foodId": foodID
                    }
                ]
            }

            url = "https://api.edamam.com/api/food-database/v2/nutrients?app_id=a5673f68&app_key=19e3c97afd04e087d29c808aaaa54418"
            
            
            req = requests.post(url, json=dataSent)
            reqJson = req.json()

            #return reqJson

            if cleanName:
                foodData["name"] = cleanName
            else:
                foodData["name"] = reqJson["ingredients"][0]["parsed"][0]["food"]
            foodData["labels"] = reqJson["healthLabels"]
            foodData["ingredients"] = reqJson["ingredients"][0]["parsed"][0]["foodContentsLabel"].split('; ')
            foodData['img'] = img

            foodNutr = reqJson["totalNutrients"]
            totalDaily = reqJson["totalDaily"]
            foodData['values'] = {}

            for key in foodNutr.keys():                
                nutrLabel = foodNutr[key]["label"]
                value = self._getDecimal(foodNutr[key]["quantity"]) + " " + str(foodNutr[key]["unit"])
                foodData['values'][nutrLabel] = {
                    'description' : nutrLabel, 
                    'nutrLabel' : nutrLabel, 
                    'value' : value,
                    'quantity' : self._getDecimal(foodNutr[key]["quantity"])
                }

            for key in totalDaily.keys():            
                nutrLabel = foodNutr[key]["label"]
                if foodData['values'].get(nutrLabel):           
                    foodData['values'][nutrLabel]['percDaily'] = self._getDecimal(totalDaily[key]['quantity'])
                else:
                    foodData['values'][nutrLabel]['percDaily'] = self._getDecimal(0)
            return foodData

        except:
            url = 'https://fdc.nal.usda.gov/portal-data/external/search'

            #input1 = input()
            #Monster 070847022909
            dataSent = {
                "generalSearchInput": str(upc)
                }
            requestHeader = {
                    "Host": "fdc.nal.usda.gov",
                    "Connection": "keep-alive",
                    "Content-Length": "275",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": "https://fdc.nal.usda.gov",
                    "Sec-Fetch-Mode": "cors",
                    "Content-Type": "application/json",
                    "Sec-Fetch-Site": "same-origin",
                    "Referer": "https://fdc.nal.usda.gov/fdc-app.html",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9"
            }

            req = requests.post(url, json=dataSent, headers=requestHeader)
            reqJson = req.json()

            fdcId = reqJson['foods'][0]['fdcId']
            foodData = {}
            foodData["name"] = reqJson['foods'][0]['lowercaseDescription']
            foodData["labels"] = ''
            foodNutrients = reqJson['foods'][0]['foodNutrients']
            foodIngredients = reqJson['foods'][0]['ingredients']
            foodData['img'] = img

            foodData["ingredients"] = foodIngredients
            foodData['values'] = []
            
            for x in range(0, len(foodNutrients)):
                nutr = foodNutrients[x]
                nutrLabel = nutr['nutrientName']
                value = str(nutr['value']) + " " + str(nutr['unitName'])
                foodData['values'].append({
                    'description' : nutr['derivationDescription'], 
                    'nutrLabel' : nutrLabel, 
                    'value' : value
                })
            return foodData