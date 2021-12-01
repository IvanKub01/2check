
from mahlo2 import app
# from tornado.wsgi import WSGIContainer
# from tornado.httpserver import HTTPServer
# from tornado.ioloop import IOLoop

import os
# import loggingEverything

def GetHigherLevelPath(level:int):
    # vyzaduje import os
    # vrati cestu o 'level' levelov vyssiu, ako je aktualna;
    # priklad: 
    # aktualna cesta je C:\__ecosystem\__work\kaizen
    # input:    1
    # output:   C:\__ecosystem\__work\
    # input:    2
    # output:   C:\__ecosystem\
    # input:    3
    # output:   C:\
    # input:    4
    # output:   error

    # ak sa vrati error, tak potom nasledne zhavaruje hlavny modul, ktory importuje support_global, resp. cokolvek,
    # co vyzaduje tento import / vystup z GetHigherPath

    # https://stackoverflow.com/questions/17359698/how-to-get-the-current-working-directory-using-python-3/17361545
    os.chdir(os.path.dirname(__file__))
    cur_path = str(os.getcwd()) + chr(92)

    c1 = cur_path.count(chr(92))

    if level>=c1:
        return "error"

    c21 = c1-level
    c11 = 0
    result = ""
    for znak in cur_path:
        result = result + znak
        if znak == chr(92):
            c11 = c11 + 1
            if c11 == c21:
                break
    return result

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5005, ssl_context=(GetHigherLevelPath(1) + "cert.pem", GetHigherLevelPath(1) + "server.key"))


