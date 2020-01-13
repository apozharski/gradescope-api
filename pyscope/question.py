from bs4 import BeautifulSoup

class GSQuestion():

    def __init__(self, qid, title, weight, children, parent_id, content):
        '''Create a assignment object'''
        self.title = title
        self.qid = qid
        self.children = []
        self.weight = weight
        self.parent_id = parent_id
        self.content = content
        
    
