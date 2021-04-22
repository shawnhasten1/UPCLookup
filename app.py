import json

# Third Party
from flask import Flask, render_template, request, redirect, jsonify, session

# Internal Libraries are loaded after we set up logging
import data

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

foodez = data.foodez()

# A welcome message to test our server
@app.route('/')
def index():
    return render_template('scan-new.html')

@app.route('/api/v1/getFood')
def getViewEntries():
    upc = request.args.get('upc')
    
    food = foodez.getFood(upc)

    return jsonify(food)

@app.route('/api/v1/getEdamam')
def getEdamamEntries():
    print("Searching")
    upc = request.args.get('upc')
    
    food = foodez.getEdamam(upc)

    return jsonify(food)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", threaded=True, port=5001, debug=True)