from news import getNewsFromTopic, getTopics
from flask import Flask, render_template, redirect, url_for, request

application = Flask(__name__)

@application.route("/")
def homepage():
    """
    Define the home page elements
    """
    return render_template("welcome.html")


@application.route("/news", methods = ["GET", "POST"] )
def news():
    """
    Accepts both GET and POST requests. If it's a GET request,
    you wouldn't have a last selected thing, so it's set to an
    empty string. If it's a POST request, we fetch the selected
    thing and return the same template with the pre-selected
    thing.
    """
    selectedNewsSection = ''
    topics = getTopics()
    if request.method == "GET":
        # Render just the template when method is "GET"
        return render_template ( "hotNews.html", topics = topics  )

    if request.method == "POST":
        selectedNewsSection = request.form["newsSection"]
        news = getNewsFromTopic(selectedNewsSection)

        return render_template( "hotNews.html" , \
                                topics = topics, \
                                selectedNewsSection = selectedNewsSection, \
                                result = news \
                            )

if __name__ == "__main__":
    application.run()
