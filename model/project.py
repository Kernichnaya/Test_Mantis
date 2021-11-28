import random
import string
from sys import maxsize


class Project:

    status_variables = ['development', 'release', 'stable', 'obsolete']
    view_state_variables = ['public', 'private']

    def __init__(self, id=None, name=None, status=None, view_state=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.status_code = self.set_status_code(status)
        self.view_state = view_state
        self.view_state_code = self.set_view_state_code(view_state)
        self.description = description

    def __repr__(self):
        return f"{self.id}: {self.name} - {self.status}"

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        return int(self.id) if self.id else maxsize

    def set_status_code(self, status):
        codes = dict(zip(self.status_variables, [10, 30, 50, 70]))
        return codes[status]

    def set_view_state_code(self, view_state):
        states = dict(zip(self.view_state_variables, [10, 50]))
        return states[view_state]

    @staticmethod
    def generate_random_name():
        return 'test_project_' + str(random.choice(range(1, 100)))

    @staticmethod
    def generate_random_status():
        return random.choice(['development', 'release', 'stable', 'obsolete'])

    @staticmethod
    def generate_random_view_state():
        return random.choice(['public', 'private'])

    @staticmethod
    def generate_random_description(maxlen=10):
        symbols = string.ascii_letters + string.digits + string.punctuation + " " * 10
        return ''.join(random.choice(symbols) for i in range(random.randrange(maxlen)))