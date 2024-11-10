from model.project import Project

def test_add_new_project(app):
    username = "administrator"
    password = "root"
    old_projects_soap = app.soap.get_projects_list(username, password)
    old_projects = [app.project.convert_to_project(p) for p in old_projects_soap]
    project_name = "test"
    existing_project = next((p for p in old_projects if p.name == project_name), None)
    if existing_project:
        app.project.open_projects_page()
        app.project.delete_by_name(project_name)
        old_projects_soap = app.soap.get_projects_list(username, password)
        old_projects = [app.project.convert_to_project(p) for p in old_projects_soap]
    project = Project(name="test", status="release", view_status="private",
                      description="test desc")
    app.project.open_new_project_form()
    app.project.create(project)
    new_projects_soap = app.soap.get_projects_list(username, password)
    new_projects = [app.project.convert_to_project(p) for p in new_projects_soap]
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=lambda project: project.id_or_max()) == sorted(new_projects, key=lambda
        project: project.id_or_max())