import os
from flask import Flask,request
from twilio.rest import Client
from dotenv import load_dotenv


# flask app
app=Flask(__name__)

load_dotenv()
# twilio
client=Client(os.environ.get("twilio_SID"),os.environ.get("twilio_auth_token"))


def send_notification(message:str):
  message = client.messages.create(
    body=message,
    from_=os.environ.get('twilio_assigned_phone_number'),
    to=os.environ.get("phone_number")
  )
  print("Message sent")
  
  
def extract_data(data:dict)->str:
  number_of_pizza=data.get("number_of_pizzas")
  toppings=data.get("pizza_toppings")
  address=data.get("address")
  phone_number=data.get("phone_number")
  
  # formated message
  message=f"🔔New order alert.\n A customer with phone number {phone_number} has place an order of {number_of_pizza} pizza with {toppings} toppings to be delivered to {address}"

  return message

@app.route("/new-order",methods=["POST"])
def new_order():
  data=request.get_json()
  if int(data.get("choice_confirmation"))==1:
    print("new order confirmed")
    message=extract_data(data)
    send_notification(message)
  else:
    print("new order cancelled")
  return "Received"


if __name__ == "__main__":
  app(port=5000,debug=True)
