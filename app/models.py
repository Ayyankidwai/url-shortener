from datetime import datetime

class URLMapping:
    def __init__(self, original_url):               #it creates the original url
        self.original_url = original_url
        self.created_at = datetime.utcnow()     #creates a timestamp for the url
        self.click_count = 0                #it counts the click on the url