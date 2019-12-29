

class GSAssignment():

    def __init__(self, name, aid, points, percent_graded, complete, regrades_on):
        '''Create a assignment object'''
        self.name = name
        self.aid = aid
        self.points = points
        self.percent_graded = percent_graded
        self.complete = complete
        self.regrades_on = regrades_on

    def add_instructor_submission(self, fname):
        '''
        Upload a PDF submission.
        '''
        pass

    def publish_grades(self):
        pass

    def unpublish_grades(self):
        pass
