import random

from model.project import Project


def test_delete_project(app, data_projects):
    if not app.soap.get_projects_list():
        app.project.create_new_project(data_projects)
    old_projects = app.soap.get_projects_list()
    project_for_delete = random.choice(old_projects)
    app.project.delete_project_by_id(project_for_delete.id)
    new_projects = app.soap.get_projects_list()
    old_projects.remove(project_for_delete)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)
