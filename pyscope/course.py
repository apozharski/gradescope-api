from enum import Enum
from bs4 import BeautifulSoup
try:
   from person import GSPerson
except ModuleNotFoundError:
   from .person import GSPerson
try:
   from assignment import GSAssignment
except ModuleNotFoundError:
   from .assignment import GSAssignment


class LoadedCapabilities(Enum):
    ASSIGNMENTS = 0
    ROSTER = 1

class GSCourse():

    def __init__(self, cid, name, shortname, year, session):
        '''Create a course object that has lazy eval'd assignments'''
        self.cid = cid
        self.name = name
        self.shortname = shortname
        self.year = year
        self.session = session
        self.assignments = {}
        self.roster = {} # TODO: Maybe shouldn't dict. 
        self.state = set() # Set of already loaded entitites (TODO what is the pythonic way to do this?)
        
    def _lazy_load_assignments(self):
        '''
        Load the assignment dictionary from assignments. This is done lazily to avoid slowdown caused by getting
        all the assignments for all classes. Also makes us less vulnerable to blocking.
        TODO: Implement
        '''
        assignment_resp = self.session.get('https://www.gradescope.com/courses/'+self.cid+'/assignments')
        parsed_assignment_resp = BeautifulSoup(assignment_resp.text, 'html.parser')
        
        assignment_table = []
        for assignment_row in parsed_assignment_resp.findAll('tr', class_ = 'js-assignmentTableAssignmentRow'):
            row = []
            for td in assignment_row.findAll('td'):
                row.append(td)
            assignment_table.append(row)
        
        for row in assignment_table:
            name = row[0].text
            aid = row[0].find('a').get('href').rsplit('/',1)[1]
            points = row[1].text
            # TODO: (released,due) = parse(row[2])
            submissions = row[3].text
            percent_graded = row[4].text
            complete = True if 'workflowCheck-complete' in row[5].get('class') else False
            regrades_on  = False if row[6].text == 'OFF' else True
            # TODO make these types reasonable
            self.assignments[name] = GSAssignment(name, aid, points, percent_graded, complete, regrades_on)
        self.state.add(LoadedCapabilities.ASSIGNMENTS)
        pass

    def _lazy_load_roster(self):
        '''
        Load the roster list  This is done lazily to avoid slowdown caused by getting
        all the rosters for all classes. Also makes us less vulnerable to blocking.
        '''
        membership_resp = self.session.get('https://www.gradescope.com/courses/' + self.cid + '/memberships')
        parsed_membership_resp = BeautifulSoup(membership_resp.text, 'html.parser')
        
        roster_table = []
        for student_row in parsed_membership_resp.find_all('tr', class_ = 'rosterRow'):
            row = []
            for td in student_row('td'):
                row.append(td)
            roster_table.append(row)

        for row in roster_table:
            name = row[0].text.rsplit(' ', 1)[0]
            email = row[1].text
            role = row[2].find('option', selected="selected").text
            submissions = int(row[3].text)
            linked = True if 'statusIcon-active' in row[4].find('i').get('class') else False
            # TODO Make types reasonable.
            self.roster[name] = GSPerson(name, email, role, submissions, linked)
        self.state.add(LoadedCapabilities.ROSTER)
        
    def _check_capabilities(self, needed):
        '''
        checks if we have the needed data loaded and gets them lazily.
        '''
        missing = needed - self.state
        if LoadedCapabilities.ASSIGNMENTS in missing:
            self._lazy_load_assignments()
        if LoadedCapabilities.ROSTER in missing:
            self._lazy_load_roster()
