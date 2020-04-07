# Importing flask
from flask import request
from flask import render_template
from flask import Flask
from flask import send_file
from geopy.geocoders import ArcGIS
import pandas

# Creating a flask object
app = Flask(__name__)

# Creating a route
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/success-table', methods=['POST'])
def success_table():
	if request.method == 'POST':
		file = request.files["file"]
		df = pandas.read_csv(file)
		nom = ArcGIS(timeout=10)
		df["Coordinates"] = df["Address"].apply(nom.geocode)
		df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude)
		df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude)
		df = df.drop("Coordinates", 1)
		df.to_csv("uploads/geocoded.csv", index=None)
		return render_template("index.html", text=df.to_html(), btn="download.html")

@app.route('/download')
def download():
	return send_file("uploads/geocoded.csv", attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
	app.run(debug=True, port="8080")