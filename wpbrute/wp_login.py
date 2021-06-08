from urllib.parse import quote
import requests
import re
class UserWordpress:
    def __init__(self, username, password, url, cookie, headers) -> None:
        self.username = username
        self.password = password
        self.wordpress = url
        self.cookie = cookie
        self.headers = headers
    def __str__(self) -> str:
        return f"<[username: {self.username}  password: {self.password[:5]}{'...' if len(self.password)>5 else ''}]>"
    def __repr__(self) -> str:
        return self.__str__()
class login:
    def __init__(self, url) -> None:
        self.headers = {
            "User-Agent":"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "origin":url
        }
        self.url = url
        self.ses = requests.Session()
        self.req = self.ses.get(url+"/wp-login.php", headers=self.headers)
    def login(self, username, password):
        if self.req.status_code  == 200 :
            data = {
                "log":username,
                "pwd":password,
                **dict(re.findall("type=\"submit\" name=\"(.*?)\" .*? value=\"(.*?)\"", self.req.text)),
                **dict(re.findall("name=\"(.*?)\" type=\"checkbox\" .*? value=\"(.*?)\"",self.req.text)),
                **dict(re.findall("type=\"hidden\" name=\"(.*?)\" value=\"(.*?)\"", self.req.text))
            }
            req=self.ses.post(self.url+"/wp-login.php", data=data, headers=self.headers|{"referer":self.url+"/wp-login.php?redirect_to="+quote(self.url+"/wp-admin/&reauth=1"), "Upgrade-Insecure-Requests":"1"})
            if '<div id="login_error">' in req.text:
                return None
            else:
                print("TRUE")
                return UserWordpress(username, password, self.url, dict(req.cookies), req.headers)
        else:
            print("stats")
            return None
        