from bs4 import BeautifulSoup

class GSAssignment():

    def __init__(self, name, qid, points):
        '''Create a assignment object'''
        self.name = name
        self.qid = qid
        self.children = {}
        self.points = points
        

    def add_child(self, child):
        self.children[self.child.name] = child
