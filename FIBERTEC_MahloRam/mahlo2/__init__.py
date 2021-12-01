from flask import Flask,url_for,render_template
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'_5#y"F4Q8z\n\xec]/'


# @app.before_request
# def before_request():
#     if request.endpoint != 'signup':
#         try:
#             dummy = session['session_userLogged']
#             print(dummy)
#         except:
#             print("toto")
            

#     else:
#         print(request.endpoint)
    
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r

from mahlo2.main import *
