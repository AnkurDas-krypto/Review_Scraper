# doing necessary imports

from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)  # initialising the flask app with the name 'app'
CORS(app)
@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

# base url + /
#http://localhost:8000 + /
@app.route('/scrap',methods=['POST']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
        try:

            flipkart_url = "https://www.flipkart.com/search?q=" + searchString  # preparing the URL to search the product on flipkart
            uClient = uReq(flipkart_url)  # requesting the webpage from the internet
            flipkartPage = uClient.read()  # reading the webpage
            uClient.close()  # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser")  # parsing the webpage as HTML
            bigboxes = flipkart_html.findAll("div",{"class": "_2pi5LC col-12-12"})
            del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0]  # taking the first iteration (for demo)
            '''
            productLink = "https://www.flipkart.com" + box.div.div.div.a[
                'href']  # extracting the actual product link
            prodRes = requests.get(productLink)  # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser")  # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {
                'class': "_3nrCtb"})  # finding the HTML section containing the customer comments
            '''
            #table = db[searchString]  # creating a collection with the same name as search string. Tables and Collections are analogous.
            # filename = searchString+".csv" #  filename to save the details
            # fw = open(filename, "w") # creating a local file to save the details
            # headers = "Product, Customer Name, Rating, Heading, Comment \n" # providing the heading of the columns
            # fw.write(headers) # writing first the headers to file
            reviews = []  # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for bigbox in bigboxes:
                try:
                    name = (bigbox.div.div.div.a.div.div.div.div.img['alt'])

                except:
                    name = 'No Name'

                try:
                    price = bigbox.findAll("div", {"class": "_30jeq3 _1_WHN1"})[0].text

                except:
                    price = 'No Price'

                try:
                    rating = bigbox.findAll("span", {"class": "_2_R_DZ"})[0].span.span.text
                except:
                    rating = 'No rating'
                try:
                    features = bigbox.findAll("li", {"class": "rgWa7D"})
                    speciality = features[0].text
                except:
                    speciality = 'No specialty'
                # fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
                mydict = {"Product": searchString, "Name": name, "Price": price, "Rating": rating,
                          "Speciality": speciality}  # saving that detail to a dictionary
                #x = table.insert_one(mydict)  # insertig the dictionary containing the rview comments to the collection
                reviews.append(mydict)  # appending the comments to the review list
            return render_template('results.html', reviews=reviews)  # showing the review to the user
        except:
            return 'something is wrong'
            # return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8000, debug=True)  # running the app on the local machine on port 8000