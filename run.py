from flask import Flask, render_template, request
app = Flask(__name__,
            static_folder = "flaskvue/dist/static",
            template_folder = "flaskvue/dist")
import requests
from backend.integrate import integrate, integrate_details
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
	restaurant = request.args.get('restaurant', None)
	response = integrate(restaurant)
	
	return render_template("search.html", result=response, resto=restaurant) 

@app.route('/details')
def details():
	name = request.args.get('name', None)
	foody_name = request.args.get('fd', None)
	address = request.args.get('addr', None)
	response = integrate_details(name, foody_name, address)
	return render_template("details.html")

if __name__ == "__main__":
	app.run()