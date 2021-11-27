from flask import render_template, request, redirect, url_for, session, jsonify, flash
from app import app
# helper methods for retrieve data and api call
from helpers import get_form_data_signup, get_form_data_login, get_app_id, \
    get_apps_name, get_images_path, login_required
# database operations
from model import close_connection, create_record, user_authentication
# converting library
from image_operations import convert_to_webp, move_converted_file
from pathlib import Path


# http://127.0.0.1.5000
@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    """
    This method is used to redirect sign in and sign up page.
    Method allows users to sign in and sign up to system
    :return: <flask.Response> HTML view
    """
    if request.method == 'GET':
        return render_template('welcome/welcome_page.html')
    elif request.method == 'POST':
        # user sign in
        if request.form.get("signin_btn"):
            email, password = get_form_data_login()
            # database operations managed well.
            # authentication or query parameters passed well
            # FIXME exception part can be better
            try:
                # query and data preparation
                sql_query: str = "SELECT * FROM apps_case_study.users WHERE email=%s AND password=%s;"
                query_data: tuple = (email, password,)
                # database crud operations
                account, connection, db_cursor = user_authentication(sql_query, query_data)
                # email and password matched. Sign in successful
                if account:
                    session['logged_in'] = True
                    close_connection(connection, db_cursor)
                    return redirect(url_for('random_select'))
                # email and password did not matched. Sign in unsuccessful
                else:
                    close_connection(connection, db_cursor)
                    return redirect(url_for('welcome_page'))
            # database related error.
            # authentication or query based reasons
            except Exception as error:
                return f'{error}'
        # user sign up
        elif request.form.get("signup_btn"):
            username, email, password = get_form_data_signup()
            # query and data preparation
            sql_query: str = "SELECT * FROM apps_case_study.users WHERE email=%s"
            query_data: tuple = (email,)
            # database crud operations
            account, connection, db_cursor = user_authentication(sql_query, query_data)
            close_connection(connection, db_cursor)
            # user already existed
            if account:
                return redirect(url_for('welcome_page'))
            # user is not existed. You can register to system
            else:
                session['logged_in'] = True
                # query and data preparation
                sql_query: str = "INSERT INTO apps_case_study.users (username,email,password) VALUES(%s,%s,%s)"
                query_data: tuple = (email, email, password,)
                # database crud operations
                db_cursor, connection = create_record(sql_query, query_data)
                close_connection(connection, db_cursor)
                return redirect(url_for("random_select"))


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('welcome_page'))


# http://127.0.0.1.5000/random-select
@app.route('/random-select', methods=['GET', 'POST'])
@login_required
def random_select():
    # get apps name with api call to fulfill dropdown
    apps_name = get_apps_name()
    if request.method == 'GET':
        # initial images before any app selected
        images_path: list = ['paşam1.jpg', 'paşam2.jpg']
        return render_template('randomize/randomize.html', req_method=request.method, apps_name=apps_name,
                               images_path=images_path)

    # user selected a game and system picked random game
    elif request.method == 'POST':
        if request.form.get('randomize_btn'):
            # get selected item from drop down
            selected_item: str = str(request.form.get('game_select'))
            # get app id with api call
            app_id = get_app_id(selected_item)
            # get all images path with app id via api call to full fill slider
            images_path = get_images_path(app_id)
            return render_template('randomize/randomize.html', req_method=request.method, apps_name=apps_name,
                                   images_path=images_path)
        elif request.form.get('upload_btn'):
            return redirect(url_for('upload_file'))
        elif request.form.get('logout_btn'):
            return redirect(url_for('logout'))


# http://127.0.0.1.5000/upload-file
@app.route('/upload-file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'GET':
        return render_template('upload/upload.html', req_method=request.method)
    elif request.method == 'POST':
        try:
            # all form fields are filled
            if request.form.get('app-id') and request.form.get('image-path'):
                req_status=True
                image_path = str(request.form.get('image-path'))
                converted_img = str(convert_to_webp(Path(image_path)))
                converted_img = converted_img.replace("\\", "/", )
                file_name = move_converted_file(converted_img,
                                                'D:/my_works/Not_Important/INTERVIEW-TASKS/APSS_POC/static/img'
                                                '/uploaded_images')
                print(file_name)
                flash('Image successfully uploaded')
                return render_template('upload/upload.html', image_path=file_name, req_status=req_status)
            # form include wrong parameters
            else:
                req_status = False
                flash('Please fulfill all mandatory fields')
                return render_template('upload/upload.html', req_status=req_status)
        except Exception as error:
            return render_template("upload/upload.html")


if __name__ == '__main__':
    app.run()
