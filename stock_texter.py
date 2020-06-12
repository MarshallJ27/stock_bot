from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
import ast

app = Flask('__name__')

def get_jsonparsed_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        #return Json data as a string
        data = json.dumps(data)
        #remove brackets from string
        data = data.strip("][")
        if data:
            #Convert string into dict
            data = ast.literal_eval(data)
        if not data:
            data = "Not a valid ticker"

        return data
    


@app.route('/bot', methods=['POST'])
def bot():
        
        incoming_msg = request.values.get('Body', '').lower()
        resp = MessagingResponse()
        msg = resp.message()
        stock = incoming_msg
        stock = stock.upper()
        url = ("https://financialmodelingprep.com/api/v3/quote-short/{stock}?[YOUR API KEY HERE]").format(stock=stock)
        
        return_msg = get_jsonparsed_data(url)
        try:
            return_msg = f'{return_msg["symbol"]} is {return_msg["price"]}'
        except:
            return_msg = "Not a valid ticker"
        
        msg.body(return_msg)
        return str(resp)