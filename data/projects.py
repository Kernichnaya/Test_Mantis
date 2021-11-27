from model.project import Project

testdata = [Project(name=Project.generate_random_name(),
                    status=Project.generate_random_status(),
                    view_state=Project.generate_random_view_state(),
                    description=Project.generate_random_description())]