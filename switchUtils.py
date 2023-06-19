import urllib.request, json 


class SwitchController:
    def __init__(self, ip_addr, id):
        self.ip_addr = ip_addr
        self.id = id

    def status(self):
        with urllib.request.urlopen(f'http://{self.ip_addr}/relay/{self.id}') as url:
            data = json.load(url)
            return data.get("ison", False)  
        
    def turnOn(self):
        urllib.request.urlopen(f'http://{self.ip_addr}/relay/{self.id}?turn=on')

    def turnOff(self):
        urllib.request.urlopen(f'http://{self.ip_addr}/relay/{self.id}?turn=off')
