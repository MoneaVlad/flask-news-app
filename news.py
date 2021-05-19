import feedparser
import time


rssUrlList = {
        "TopStories": { 
            "googlenews"        : "https://news.google.com/rss?oc=5&hl=en-US&gl=US&ceid=US:en"
        },

        "Romania" : {
            "googlenews"        : "https://news.google.com/rss/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE"
        },

        "World" : {
            "googlenews"        : "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB",
            "bbc"               : "http://feeds.bbci.co.uk/news/world/rss.xml"
        },

        "Business" : {
            "googlenews"        : "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB",
            "bbc"               : "http://feeds.bbci.co.uk/news/business/rss.xml"
        },

        "Technology" : {
            "googlenews"        : "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB",
            "bbc"               : "http://feeds.bbci.co.uk/news/technology/rss.xml"
        },

        "Health" : {
            "googlenews"        : "https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ",
            "bbc"               : "http://feeds.bbci.co.uk/news/health/rss.xml"
        }
}

def getNews(topic, mediagroup, url):
    """
    Function to collect data from RSS Feed
    Get only the summary for articles which were published in the last 3 days
    """
    newsitems = []

    cutOffTime = 259200 # 3 * 24 * 60 * 60
    try:
        feed = feedparser.parse(url)
        if feed:
            for entry in feed['entries']:
                newsTxt = ''

                last_updated = time.mktime( entry['published_parsed'] )
                currLocalTime = time.mktime(time.localtime())

                publishedTime = str( entry['published_parsed'][3] ) + " hours ago."
                # Check if the articles are less than a given time period
                if ( currLocalTime - last_updated ) < cutOffTime:
                    newsTxt = entry['title_detail']['value']

                if newsTxt:
                    newsitems.append( (newsTxt + " (Published  " + publishedTime + ")", entry["link"])  )

            if not newsitems:
                newsitems.append( "Pfttt!! Nothing new since the last " \
                    + str( cutOffTime / 3600) + " hours."  )
    except Exception as e:
        print("Error : " + str(e))

    return newsitems

def getNewsFromTopic(topic):
    """
    Function to collect data for a specific topic from all RSS Feeds
    """
    articles = []
    mediagroups = rssUrlList[topic]
    for  mediagroup, url in mediagroups.items():
        articles.extend(getNews(topic, mediagroup, url))
    return articles

def getTopics():
    """
    Function to get all available topics
    """
    return rssUrlList.keys()

