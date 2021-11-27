from model.project import Project


def test_add_project(app, data_projects):
    old_projects = app.project.get_project_list()
    project = data_projects
    app.project.create_new_project(project)
    new_projects = app.project.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
