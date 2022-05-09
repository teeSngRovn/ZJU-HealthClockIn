import requests
import re

class website(object):
    def __init__(self):
        self.login_url = "https://zjuam.zju.edu.cn/cas/login?service=https%3A%2F%2Fhealthreport.zju.edu.cn%2Fa_zju%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fhealthreport.zju.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
        self.base_url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
        self.save_url = "https://healthreport.zju.edu.cn/ncov/wap/default/save"
        self.pubkey_url = "https://zjuam.zju.edu.cn/cas/v2/getPubKey"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }
        self.sess = requests.Session()
    def login(self, User):
        
        response = self.sess.get(self.login_url, headers=self.headers)
        execution = re.search(
            "name=\"execution\" value=\"(.*?)\"", response.text).group(1)
        
        response = self.sess.get(
            url=self.pubkey_url, headers=self.headers).json()
        modulus, exponent = response["modulus"],response["exponent"]
        encrypt_passwd = self.encrypt(User.passwd, modulus, exponent)
        
        datas = {
            "username" : User.username,
            "password" : encrypt_passwd,
            "execution" : execution,
            "_eventId" : "submit"
        }
        
        response = self.sess.post(self.login_url, data = datas, headers = self.headers)
        if "通行证" in response.content.decode():
            print("login error")
        return self.sess
    
    def encrypt(self, password_str, mod, exp):
        password_int = int.from_bytes(bytes(password_str,"ascii"), "big")
        e_int = int(exp, 16)
        M_int = int(mod, 16)
        result_int = pow(password_int, e_int, M_int)
        return hex(result_int)[2:].rjust(128, '0')    

class student(object):
    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd



if __name__=="__main__":
    user = student("1","2")
    web = website()
    print(web.login(user))