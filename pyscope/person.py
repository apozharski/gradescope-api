from enum import Enum

class GSRole(Enum):
    INSTRUCTOR = 0
    TA = 1
    STUDENT = 2
    READER = 3
    
    def from_str(val):
        if isinstance(val, GSRole):
            return val
        strings = {
            'Instructor': GSRole.INSTRUCTOR,
            'Student': GSRole.STUDENT,
            'TA': GSRole.TA,
            'Reader': GSRole.READER
        }
        role =  strings.get(val)
        if role is not None:
            return role
        else:
            raise GSRoleException("Not a valid role string: " + role)  

    class GSRoleException(Exception):
        pass
    
    
class GSPerson():
    def __init__(self, name, email, role, submissions, linked):
        self.name = name
        self.email = email
        self.role = GSRole.from_str(role)
        self.linked = linked
        self.submissions = submissions
