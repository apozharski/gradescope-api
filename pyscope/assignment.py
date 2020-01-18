import requests
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

    def add_question(self, title, weight, crop = None, content = [], parent_id = None):
        new_q_data = [q.to_patch() for q in self.questions]
        new_crop = crop if crop else [{'x1': 10, 'x2': 91, 'y1': 73, 'y2': 93, 'page_number': 1}]
        new_q = {'title': title, 'weight': weight, 'crop_rect_list': new_crop}
        if parent_id:
            # TODO: This should throw a custom exception if a parent is not found
            parent = [parent for parent in new_q_data if parent['id'] == parent_id][0]
            if parent['children']:
                parent['children'].append(new_q)
            else:
                parent['children'] = [new_q]
        else:
            new_q_data.append(new_q)

        # TODO add id region support
        new_patch = {'assignment': {'identification_regions': {'name': None, 'sid': None}},
                     'question_data': new_q_data}

        outline_resp = self.course.session.get('https://www.gradescope.com/courses/' + self.course.cid +
                                               '/assignments/' + self.aid + '/outline/edit')
        parsed_outline_resp = BeautifulSoup(outline_resp.text, 'html.parser')
        authenticity_token = parsed_outline_resp.find('meta', attrs = {'name': 'csrf-token'} ).get('content')

        patch_resp = self.course.session.patch('https://www.gradescope.com/courses/' + self.course.cid +
                                               '/assignments/' + self.aid + '/outline/',
                                               headers = {'x-csrf-token': authenticity_token,
                                                          'Content-Type': 'application/json'},
                                               data = json.dumps(new_patch,separators=(',',':')))

        if patch_resp.status_code != requests.codes.ok:
            patch_resp.raise_for_status()

        # TODO this should be done smarter :(
        self.questions = []
        self._lazy_load_questions()

    # TODO allow this to be a predicate remove
    def remove_question(self, title=None, qid=None):
        if not title and not qid:
            return
        new_q_data = [q.to_patch() for q in self.questions]

        # TODO Yes this is slow and ugly, should be improved
        if title: 
            new_q_data = [q for q in new_q_data if q['title'] != title]
            for q in new_q_data:
                if q.get('children'):
                    q['children'] = [sq for sq in q['children'] if sq['title'] != title]
        else:
            new_q_data = [q for q in new_q_data if q['id'] != qid]
            for q in new_q_data:
                if q.get('children'):
                    q['children'] = [sq for sq in q['children'] if sq['id'] != qid]

        new_patch = {'assignment': {'identification_regions': {'name': None, 'sid': None}},
                     'question_data': new_q_data}

        outline_resp = self.course.session.get('https://www.gradescope.com/courses/' + self.course.cid +
                                               '/assignments/' + self.aid + '/outline/edit')
        parsed_outline_resp = BeautifulSoup(outline_resp.text, 'html.parser')
        authenticity_token = parsed_outline_resp.find('meta', attrs = {'name': 'csrf-token'} ).get('content')

        patch_resp = self.course.session.patch('https://www.gradescope.com/courses/' + self.course.cid +
                                               '/assignments/' + self.aid + '/outline/',
                                               headers = {'x-csrf-token': authenticity_token,
                                                          'Content-Type': 'application/json'},
                                               data = json.dumps(new_patch,separators=(',',':')))

        if patch_resp.status_code != requests.codes.ok:
            patch_resp.raise_for_status()

        # TODO this should be done smarter :(
        self.questions = []
        self._lazy_load_questions()
        
    # TODO INCOMPLETE
    def add_instructor_submission(self, fname):
        '''
        Upload a PDF submission.
        '''
        submission_resp = self.session.get('https://www.gradescope.com/courses/'+self.course.cid+
                                           '/assignments/'+self.aid+'/submission_batches')
        parsed_assignment_resp = BeautifulSoup(submission_resp.text, 'html.parser')
        authenticity_token = parsed_assignment_resp.find('meta', attrs = {'name': 'csrf-token'} ).get('content')

        submission_files = {
            "file" : open(template_file, 'rb')
        }

        submission_resp = self.session.post('https://www.gradescope.com/courses/'+self.course.cid+
                                            '/assignments/'+self.aid+'/submission_batches',
                                            files = assignment_files
                                            headers = {'x-csrf-token': authenticity_token})
        
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
            crop = question['crop_rect_list']
            children = []
            qchildren = question.get('children', [])
            
            for subquestion in qchildren:
                c_qid = subquestion['id']
                c_title = subquestion['title']
                c_parent_id = subquestion['parent_id']
                c_weight = subquestion['weight']
                c_content = subquestion['content']
                c_crop = subquestion['crop_rect_list']
                children.append(GSQuestion(c_qid, c_title, c_weight, [], c_parent_id, c_content, c_crop))
            self.questions.append(GSQuestion(qid, title, weight, children, parent_id, content, crop))
            
        
