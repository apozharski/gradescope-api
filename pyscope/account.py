from bs4 import BeautifulSoup
try:
   from course import GSCourse
except ModuleNotFoundError:
   from .course import GSCourse

class GSAccount():
    '''A class designed to track the account details (instructor and student courses'''

    def __init__(self, email, session):
        self.email = email
        self.session = session
        self.instructor_courses = {}
        self.student_courses = {}

    def add_class(self, cid, name, shortname, year, instructor = False):
        if instructor:
            self.instructor_courses[cid] = GSCourse(cid, name, shortname, year, self.session)
        else:
            self.student_courses[cid] = GSCourse(cid, name, shortname, year, self.session)

    # TODO add default exceptions when doing unsafe things.
    def delete_class(self, cid):
        self.instructor_courses[cid].delete()
        del self.instructor_courses[cid]

    def create_course(self, name, shortname, description, term, year, school, entry_code_enabled = False):
        '''Returns course ID'''
        account_resp = self.session.get("https://www.gradescope.com/account")
        parsed_account_resp = BeautifulSoup(account_resp.text, 'html.parser')

        create_modal = parsed_account_resp.find('div', id = 'createCourseModal')
        authenticity_token = create_modal.find('input', attrs = {'name': 'authenticity_token'}).get('value')
        schools = create_modal.find('select', id = 'course_school_id')
        school_id = schools.find('option', text = school).get('value') # TODO Fix this on bad params.
        course_data = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "course[shortname]": shortname,
            "course[name]": name,
            "course[description]": description,
            "course[term]": term,
            "course[year]": year,
            "course[school_id]": school_id,
            "course[entry_code_enabled]": 1 if entry_code_enabled else 0,
            "commit": "Create Course",
        }
        
        course_resp = self.session.post("https://www.gradescope.com/courses", params=course_data)
        # TODO This is brittle
        cid = course_resp.history[0].headers.get('Location').rsplit('/', 1)[1]
        # TODO fix term, year union
        self.add_class(cid, name, shortname, term+" "+year, instructor = True )
        return cid
        
