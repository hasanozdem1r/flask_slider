from flask import render_template,request,redirect,url_for
from model import mysql_obj,close_connection,create_record,user_authentication
from app import app
from requests import get

# http://127.0.0.1.5000
@app.route('/',methods=['GET','POST'])
def welcome_page():
    """
    This method is used to redirect sign in and sign up page.
    Method allows users to sign in and sign up to system
    :return: <flask.Response> HTML view
    """
    if request.method=='GET':
        return render_template('welcome/welcome_page.html')
    elif request.method=='POST':
        # user sign in
        if request.form.get("signin_btn"):
            email, password = get_form_data_login()
            try:
                sql_query:str="SELECT * FROM apps_case_study.users WHERE email=%s AND password=%s;"
                query_data:tuple=(email,password,)
                account,connection,db_cursor = user_authentication(sql_query,query_data)
                if account:
                    return redirect("random_select")
                else:
                    return redirect(url_for('welcome_page'))
                close_connection(connection, db_cursor)
            except Exception as error:
                return f'{error}'
        # user sign up
        elif request.form.get("signup_btn"):
            username,email, password= get_form_data_signup()
            sql_query:str="SELECT * FROM apps_case_study.users WHERE email=%s"
            query_data: tuple = (email,)
            account, connection, db_cursor = user_authentication(sql_query,query_data)
            close_connection(connection, db_cursor)
            # user already existed
            if account:
                return redirect(url_for('welcome_page'))
            # user is not existed. You can register to system
            else:
                sql_query:str = "INSERT INTO apps_case_study.users (username,email,password) VALUES(%s,%s,%s)"
                query_data: tuple = (email,email,password,)
                db_cursor,connection=create_record(sql_query,query_data)
                close_connection(connection, db_cursor)
                return redirect("random_select")

# HELPER FUNCTIONS
def get_form_data_signup()->tuple:
    """
    This method is used to retrieve sign-up form data.
    :return: <tuple> user authentication data
    """
    username: str = str(request.form.get('usrnm'))
    email: str = str(request.form.get('eml'))
    password: str = str(request.form.get('pswd'))
    return username,email, password

def get_form_data_login()->tuple:
    """
    This method is used to retrieve sign-im form data.
    :return: <tuple> user authentication data
    """
    email = str(request.form.get('eml'))
    password = str(request.form.get('pswd'))
    return email, password


# http://127.0.0.1.5000/random_select
@app.route('/random_select',methods=['GET','POST'])
def random_select():
    if request.method=='GET':
        apps:list=get("http://localhost:80/apps-api/v1/apps").json()
        apps_name=[app_name[1] for app_name in apps]
        images:list=get("http://localhost/apps-api/v1/images?app-id=51").json()
        images_path=[img_path[1] for img_path in images]
        return render_template('randomize/randomize.html',apps_name=apps_name,images_path=images_path)
    elif request.method=='POST':
        select = request.form.get('game_select')
        return render_template("randomize/randomize.html")

# http://127.0.0.1.5000/upload_file
@app.route('/upload_file')
def upload_file():
    return render_template('upload/upload.html')

if __name__ == '__main__':
    app.run()
