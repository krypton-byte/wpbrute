import requests
import re
class wp_info:
    def __init__(self, ,url):
        self.text    = requests.get(url, params={"author":1})
        self.version = re.search('WordPress (.*?)\"',self.text.text)[1] if re.search('WordPress (.*?)\"',self.text.text) else False
        self.themes  = re.findall('wp-content\/themes\/(.*?)\/',self.text.text)[1] if re.findall('wp-content\/themes\/(.*?)\/',self.text.text) else False
        self.plugins = list(set(re.findall('wp-content\/plugins\/(.*?)\/',self.text.text))) if re.findall('wp-content\/plugins\/(.*?)\/',self.text.text) else []
        self.author  = re.findall('/author/(.*?)/', self.text.url+"/")[0] if re.findall('/author/(.*?)/', self.text.url+"/") else ""
    def passgen_author(self, iter):
        return map(lambda it:self.author+str(it), iter)