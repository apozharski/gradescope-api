from bs4 import BeautifulSoup
try:
   from question import GSQuestion
except ModuleNotFoundError:
   from .question import GSQuestion
import json

class GSAssignment():

    def __init__(self, name, aid, points, percent_graded, complete, regrades_on, course):
        '''Create a assignment object'''
        self.name = name
        self.aid = aid
        self.points = points
        self.percent_graded = percent_graded
        self.complete = complete
        self.regrades_on = regrades_on
        self.course = course
        self.questions = []
        
    # TODO
    def add_instructor_submission(self, fname):
        '''
        Upload a PDF submission.
        '''
        pass

    # TODO
    def publish_grades(self):
        pass

    # TODO
    def unpublish_grades(self):
        pass

    def _lazy_load_questions(self):
        
        outline_resp = self.course.session.get('https://www.gradescope.com/courses/' + self.course.cid +
                                               '/assignments/' + self.aid + '/outline/edit')
        parsed_outline_resp = BeautifulSoup(outline_resp.text, 'html.parser')

        props = parsed_outline_resp.find('div',
                                         attrs={'data-react-class':'AssignmentOutline'}).get('data-react-props')
        json_props = json.loads(props)
        outline = json_props['outline']

        for question in outline:
            qid = question['id']
            title = question['title']
            parent_id = question['parent_id']
            weight = question['weight']
            content = question['content']

            children = []
            qchildren = question.get('children', [])
            
            for subquestion in qchildren:
                c_qid = subquestion['id']
                c_title = subquestion['title']
                c_parent_id = subquestion['parent_id']
                c_weight = subquestion['weight']
                c_content = subquestion['content']
                children.append(GSQuestion(c_qid, c_title, c_weight, [], c_parent_id, c_content))
            self.questions.append(GSQuestion(qid, title, weight, children, parent_id, content))
