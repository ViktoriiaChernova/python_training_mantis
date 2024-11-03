from model.project import Project

def test_delete_project(app):
    if len(app.project.get_projects_list()) == 0:
        app.project.open_new_project_form()
        project = Project(name="test", status="release", view_status="private", description="test desc")
        app.project.create(project)
    old_projects = app.project.get_projects_list()
    first_project = old_projects[0]
    app.project.delete_project_by_index(0)
    new_projects = app.project.get_projects_list()
    old_projects.remove(first_project)
    assert old_projects == new_projects
