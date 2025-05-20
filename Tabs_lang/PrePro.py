import re

class PrePro():
    def filter(self, txt):
        return re.sub(r'//.*(\r|\n|$)', ' ', txt)
    
