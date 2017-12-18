from flask import Flask, render_template, request
app = Flask(__name__,
            static_folder = "flaskvue/dist/static",
            template_folder = "flaskvue/dist")
import requests
from backend.integrate import integrate
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
	restaurant = request.args.get('restaurant', None)
	response = integrate(restaurant)
	
	return render_template("search.html", result=response, resto=restaurant) 

if __name__ == "__main__":
	app.run()