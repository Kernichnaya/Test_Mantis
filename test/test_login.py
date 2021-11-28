def test_login(app):
    if app.session.is_logged_in():
        app.session.ensure_logout()
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")