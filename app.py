from flask import Flask,render_template

app = Flask(__name__)


# http://127.0.0.1.5000
@app.route('/')
def welcome_page():  # put application's code here
    return render_template('welcome/welcome_page.html')


# http://127.0.0.1.5000/random_select
@app.route('/random_select')
def random_select():
    return render_template('randomize/randomize.html')


# http://127.0.0.1.5000/upload_file
@app.route('/upload_file')
def upload_file():
    return render_template('upload/upload.html')

if __name__ == '__main__':
    app.run()
