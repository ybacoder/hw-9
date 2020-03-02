from flask import Flask, jsonify, render_template
import pandas as pd
import pymongo
import scrape_mars


# Initialize PyMongo to work with MongoDBs
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_db
collection = db.mars
# result = scrape_mars.scrape()
# for item in result:
#     collection.insert_one(item)

app = Flask(__name__)

@app.route("/")
def init_app():
    scrape = scrape_mars.scrape()
    facts = scrape["facts"].to_html()
    return render_template(
        "index.html",
        news=scrape["news"],
        image=scrape["image"],
        weather=scrape["weather"],
        facts=facts,
        hemispheres=scrape["hemispheres"]
        )

# @app.route("/scrape")
# def scrape():
#     return scrape_mars.scrape()


if __name__ == "__main__":
    app.run(debug=True)
    
