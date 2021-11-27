from flask import request,session,redirect,url_for,flash
from requests import get
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('welcome_page'))

    return wrap


def get_form_data_signup() -> tuple:
    """
    This method is used to retrieve sign-up form input values.
    :return: <tuple> user authentication data (username:str, email:str, password:str)
    """
    username: str = str(request.form.get('usrnm'))
    email: str = str(request.form.get('eml'))
    password: str = str(request.form.get('pswd'))
    return username, email, password


def get_form_data_login() -> tuple:
    """
    This method is used to retrieve sign-in form input values.
    :return: <tuple> user authentication data (email:str, password:str)
    """
    email: str = str(request.form.get('eml'))
    password: str = str(request.form.get('pswd'))
    return email, password


def get_app_id(selected_item) -> int:
    """
    This method returns the application id using the given name
    :param selected_item: <str> application name
    :return: <int> application id
    """
    app = get(f'http://localhost:80/apps-api/v1/apps/id?app-name={selected_item}').json()
    app_id: int = int(app[0][0])
    return app_id


def get_apps_name() -> list:
    """
    This method returns the application names
    :return:  <list> application names
    """
    apps: list = get("http://localhost/apps-api/v1/apps").json()
    apps_name: list = [str(app_name)[2:-2] for app_name in apps]
    return apps_name


def get_images_path(app_id: int = 0) -> list:
    """
    This method returns the application images paths using the given application id
    :param app_id: <int> application id
    :return: <list> application images path
    """
    images: list = get(f"http://localhost/apps-api/v1/images?app-id={str(app_id)}").json()
    images_path: list = [img_path[1] for img_path in images]
    return images_path
