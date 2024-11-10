from model.project import Project

def test_delete_project(app):
    username = "administrator"
    password = "root"
    if len(app.soap.get_projects_list(username, password)) == 0:
        app.project.open_new_project_form()
        project = Project(name="test", status="release", view_status="private", description="test desc")
        app.project.create(project)
    old_projects_soap = app.soap.get_projects_list(username, password)
    old_projects = [app.project.convert_to_project(p) for p in old_projects_soap]
    first_project = old_projects[0]
    app.project.open_projects_page()
    app.project.delete_project_by_index(0)
    new_projects_soap = app.soap.get_projects_list(username, password)
    new_projects = [app.project.convert_to_project(p) for p in new_projects_soap]
    old_projects.remove(first_project)
    assert old_projects == new_projects
