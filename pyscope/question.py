from bs4 import BeautifulSoup

class GSQuestion():

    def __init__(self, qid, title, weight, children, parent_id, content, crop):
        '''Create a assignment object'''
        self.title = title
        self.qid = qid
        self.children = children
        self.weight = weight
        self.parent_id = parent_id
        self.content = content
        self.crop = crop
        
    def to_patch(self):
        children = [child.to_patch() for child in self.children]
        output = {'id': self.qid, 'title': self.title, 'weight': self.weight, 'crop_rect_list': self.crop}
        print('length of children:', len(self.children))
        if len(children) != 0:
            output['children'] = children
        return output
