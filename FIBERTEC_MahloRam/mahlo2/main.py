# MAHLO Application


from flask import render_template, request ,redirect, jsonify,flash,json, session ,abort,Response
from requests import Session
from datetime import datetime, timedelta
from mahlo2 import app
import sys
import math
import os 
import pandas as pd
import numpy as np
from PIL import Image
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from datetime import datetime
import pyodbc
import socket
import matplotlib.pyplot as plt
def AdminAuth():
    if(str(session['session_admin']) == "0"):
        print("tt")
        return Response(abort(404))


        # return flask.redirect(next or flask.url_for('index'))

#region USER MONITORING.    D O N T ' T    F O R G E T    to change parameters in 'EvokeUserMonitoring'
# packed in 'region' tag for easier manipulation.

# SHOULD BE CALLED AS A FIRST COMMAND IN EVERY APP ROUTE, WHICH IS INTENDED TO MONITOR
def EvokeUserMonitoring(sURI:str):
    # this command should be in every app route as a first command to get complete monitoring. Should be called like this:
    # EvokeUserMonitoring(str(request.url))

    # first and second parameter must be set in this call.
    #       - first one is a name of application (mRunchart, mTeamboard, ...)                   max length is 50 characters
    #       - second one is MIBA plant (site) (MSSK, MPCC, MSA, ...)                            max length is 50 characters
    # this is the    O N L Y    P L A C E    in whole application where these details must be defined.
    # print("EVOKE USER MONITORING. URI: " + str(sURI))
    SaveUserRequestDetailsIntoDatabase("Heat Map", "mfb", sURI)

# GET LOCAL IP ADDRESS. THERE ARE FEW WAYS HOW TO ACHIEVE IT. WE WILL TRY ALL OF THEM.
def GetLocalIPAddress():
    # many ways how to get local IP address
    sUsersIP1 = []

    # WAY 1          ##############
    try:
        sUsersIP1.append(str(request.environ['REMOTE_ADDR']))
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 2          ##############
    try:
        sUsersIP1.append(str(request.environ['HTTP_X_FORWARDED_FOR']))  # if behind a proxy
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 3          ##############
    try:
        sUsersIP1.append(str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 4          ##############
    try:
        sUsersIP1.append(str(socket.gethostbyname(socket.gethostname())))
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 5          ##############
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            sUsersIP1.append(str(s.getsockname()[0]))
        except:
            pass
        finally:
            s.close()
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 6          ##############
    try:
        sUsersIP1.append(str(([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])))
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 7          ##############
    try:
        sUsersIP1.append(str(((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + [""])[0])))
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 8          ##############
    try:
        sUsersIP1.append(str(request.remote_addr))
    except:
        # print(sys.exc_info()[1])
        pass

    # WAY 9          ##############
    try:
        sUsersIP1.append(str(request.headers.get('X-Forwarded-For', request.remote_addr)))
    except:
        # print(sys.exc_info()[1])
        pass


    ####################################################################################################################################
    # attach to string those entries which are not bullshit
    # print("items amount: " + str(len(sUsersIP1)))
    sUsersIP=str("")
    for ip in sUsersIP1:
        # print("ip: " + ip)
        if len(ip) == 0:
            continue
        if ip == "127.0.0.1":
            continue
        if ip == "0.0.0.0":
            continue
        if not(ip.__contains__("172.")):
            continue


        # if string contains this address, don't add it again!
        if sUsersIP.__contains__(ip):
            continue

        # seems like address is not a bullshit, and also it is not in the string yet. add it into string
        sUsersIP = sUsersIP + ip + ", "

    # if string is empty, it cannot get ip address. return this as string.
    if len(sUsersIP) == 0:
        sUsersIP="Unable to get IP address."

    # get rid off last coma with space
    if sUsersIP[(len(sUsersIP)-2):] == ", ":
        sUsersIP = sUsersIP[:(len(sUsersIP)-2)]

    # now bugger off!
    return sUsersIP


# THIS IS CALLED AUTOMATICALLY BY FLASK BEFORE EVERY REQUEST
@app.before_request
def procedure_before_request():
    user_name = ""
    try:
        user_name = str(request.form.get('userName'))
    except:
        pass
    # print("USER NAME FROM FORM REQUEST IN 'before_request': " + str(user_name) )

    if user_name.lower() != "none":
        try:
            if session['session_remote_user_entry'] == False:
                session['session_remote_user_entry'] = True
                session['session_remote_user_name'] = user_name
                EvokeUserMonitoring("")
                # print("GOT USER NAME - SESSION SET")
        except:
            pass



# THIS IS CALLED BY AJAX FROM SendUserName function. IT STORES REMOTE USER NAME INTO SESSION. It uses Mohanish's script. thanx :)
@app.route('/GetRemoteUserDetails', methods=['GET', 'POST'])
def GetRemoteUserDetails():
    retValue = "--------------------- PROCEDURE GET REMOTE USER DETAILS: "
    try:
        REMOTE_USER = str(request.form['userName'])
        session['session_remote_user_name'] = REMOTE_USER
        retValue = retValue + "REMOTE_USER_NAME SUCCESS: " + str(REMOTE_USER)
    except:
        retValue = retValue + "REMOTE USER_NAME ERROR: " + sys.exc_info()[1]

    # print(retValue)

    return ""


# THIS MAKES SAVE INTO TABLE
def SaveUserRequestDetailsIntoDatabase(sApp:str, sSite:str, sURI:str):
    # parameters:
    # sApp - mRunchart, mTeamboard, ...
    # sURI - complete URL address from request: http://172.23.11.100:5050/pu1/lisovanie
    # sSite - MSSK, MPCC, ...
    # these informations are logged:
    # current date/time, remote user name, application (mrunchart, tool management, ...), URI, site (mssk, mpcc, ...), server IP, user IP

    # here is some knowledge:
    # https://stackoverflow.com/questions/15974730/how-do-i-get-the-different-parts-of-a-flask-requests-url
    # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

    # print("------------------------ SaveUserRequestDetailsIntoDatabase 1 ------------------------")
    session['session_remote_user_entry'] = False

    remote_user = ""                                                # remote user name (via Mohanish's script)
    try:
        remote_user = session['session_remote_user_name']
    except:
        # print("---------- ERROR - No user name stored in session. Return false.")
        # print(sys.exc_info()[1])
        return False

    session['session_remote_user_entry'] = True

    remote_user = remote_user.replace("MIBA-AT", "")
    remote_user = remote_user.replace("miba-at", "")
    remote_user = str(remote_user.replace(chr(92), ""))     # \
    # remote_user = ((remote_user[:1]).upper()) + ((remote_user[1: len(remote_user)-2]).lower()) + ((remote_user[len(remote_user)-2:len(remote_user)-1]).upper()) + ((remote_user[len(remote_user)-1:]).lower())
    remote_user = remote_user.upper()

    current_time = datetime.now()                          # current date and time

    user_ip = request.remote_addr                                   # IP of client
    server_ip = str(GetLocalIPAddress())

    # remove IP address of current local client
    server_ip=server_ip.replace(user_ip + ",","")
    server_ip=server_ip.replace(user_ip,"")
    server_ip=server_ip.strip()

    sSite = sSite.upper()

    # print("------------------------ SaveUserRequestDetailsIntoDatabase 2 ------------------------")
    # print("        time           : " + str(current_time))
    # print("        user           : " + str(remote_user))
    # print("        sApp           : " + str(sApp))
    # print("        sURI           : " + str(sURI))
    # print("        sSite          : " + str(sSite))
    # print("        Server IP      : " + str(server_ip))
    # print("        User IP        : " + str(user_ip))

    try:
        conn = pyodbc.connect("DRIVER={SQL Server};SERVER=shaplmib013;DATABASE=MSOLUTIONS;UID=mssk;PWD=Miba123+")
    except:
        print(sys.exc_info()[1])
        return False
    c = conn.cursor()
    retValue = True


    # eliminate users, which are not supposed to be saved into table
    if remote_user.lower() == 't_dks_screen':
        return retValue


    try:
        params=[]
        params.append(current_time)
        params.append(remote_user)
        params.append(sApp)
        params.append(sURI)
        params.append(sSite)
        params.append(server_ip)
        params.append(user_ip)
        params.append(None)

        sCommand = "INSERT INTO log.UsersMonitoring VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        # print(sCommand)

        c.execute(sCommand, params)
        conn.commit()
    except:
        # print("---------- ERROR WHILE INSERTING RECORD IN TABLE:")
        # print(sys.exc_info()[1])
        retValue = False

    c.close()
    conn.close()			# close database connect before every return, or immediatelly when you don't need it anymore!

    return retValue


# end of user monitoring. packed in 'region' tag for easier manipulation.
#endregion
def histgramGen(lst,perList):
    plt.clf()
    x_pos = np.arange(len(lst))

    # Create bars with different colors
    plt.bar(x_pos, lst, color=['#0fb6ad', '#fcff3e', '#E0EC37', '#C3D92F', '#A6C627','#89B31F','#6DA118','#42850D','#166801','#42850d','#6da118','#9b921c','#a18118','#a16618','#a14e16','#a13f18','#FF0000'])

    # Create names on the x-axis
    plt.xticks(x_pos, perList)#['under','7seg','6seg','5seg','4seg','3seg','2seg','1seg','0seg','1seg','2seg','3seg','4seg','5seg','6seg','7seg','over'])
    plt.xticks(fontsize=8,rotation=45)
    plt.savefig(".\mahlo2\static\img\histogram.png")
@app.route("/logoff", methods=["GET", "POST"])
def logoff():
    session.pop('session_userLogged', None)
    
    return render_template("signup.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    # print(str(session['session_admin']))
    # END TRY
    # nebudem drzat session o zalogovanom useri. staci mi, ze sa vie zalogovat
    #endregion
    # str(session['session_admin']
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:    
        cursor = cnxn.cursor()
        listOfPRun = list(cursor.execute('SELECT DISTINCT PRODUCTION_RUN FROM MahloSpolu').fetchall())
        listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id FROM TypPrudct inner JOIN MahloSpolu ON MahloSpolu.DRUH = TypPrudct.id order by id asc').fetchall())
        listOfTrec = list(cursor.execute('SELECT distinct IDDRUH,NAZOV,LTL,UTL FROM MahloTrecMat ').fetchall())

    return render_template("Nahled.html",flash_message="1",listOfPRun=listOfPRun,listOfPDruh=listOfPDruh,listOfTrec=listOfTrec,admin=str(session['session_admin']))

@app.route("/live", methods=["GET", "POST"])
def live():
  
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  

        cursor = cnxn.cursor()
        listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id  FROM TypPrudct inner JOIN MahloSpolu ON MahloSpolu.DRUH = TypPrudct.id order by id asc').fetchall())
        listOfTrec = list(cursor.execute('SELECT distinct IDDRUH,NAZOV,LTL,UTL FROM MahloTrecMat ').fetchall())

    return render_template("NahledLive.html",listOfPDruh=listOfPDruh, listOfTrec=listOfTrec,admin=str(session['session_admin']))

@app.route("/nahled", methods=["GET", "POST"])
def nahled():
    referrer1 = request.referrer
    referrer2 = request.headers.get("Referer")

    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        listOfPRun = list(cursor.execute('SELECT DISTINCT PRODUCTION_RUN FROM MahloSpolu').fetchall())
        listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id FROM TypPrudct inner JOIN MahloSpolu ON MahloSpolu.DRUH = TypPrudct.id order by id asc').fetchall())
        listOfTrec = list(cursor.execute('SELECT distinct IDDRUH,NAZOV,LTL,UTL FROM MahloTrecMat ').fetchall())
    return render_template("Nahled.html",listOfPRun=listOfPRun,listOfPDruh=listOfPDruh,listOfTrec=listOfTrec,flash_message="1",admin=str(session['session_admin']))

@app.route("/TrecieMaterialy", methods=["GET", "POST"])
def TrecieMaterialy():
    
    AdminAuth()
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id FROM TypPrudct where id < 3 order by id asc ').fetchall())
    return render_template("TrecieMaterialy.html",listOfPDruh=listOfPDruh)

@app.route("/get_TrecieMaterialy", methods=["GET", "POST"])
def get_TrecieMaterialy():
    AdminAuth()
    data = []
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  

        cursor = cnxn.cursor()
        listOfTrec = list(cursor.execute('SELECT distinct MahloTrecMat.ID,TypPrudct.name,MahloTrecMat.NAZOV,MahloTrecMat.LTL,MahloTrecMat.UTL FROM MahloTrecMat inner JOIN TypPrudct ON TypPrudct.id = MahloTrecMat.IDDRUH ').fetchall())
        
    for row in listOfTrec:
        data.append({
                "ID": row.ID,
                "IDDRUH": row.name,
                "NAZOV" : row.NAZOV,
                "LTL" : row.LTL,
                "UTL" : row.UTL,
            })
    # print(data)
    return jsonify(data)    

@app.route("/adding", methods=["GET", "POST"])
def adding():
    AdminAuth()
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
#except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        listOfPRun = list(cursor.execute('SELECT DISTINCT PRODUCTION_RUN FROM MahloSpolu').fetchall())
        listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id FROM TypPrudct').fetchall())

    return render_template("Pridaj.html",listOfPRun=listOfPRun,listOfPDruh=listOfPDruh)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["TEXT", "TXT"]

def allowed_image(filename):
    # print(f"toto je filename {filename}")
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/pridaj", methods=["GET", "POST"])
def pridaj():
    AdminAuth()
    # ak sa submitne form s action="/pridaj" method="POST" 
    if request.method == "POST":
        #nacita production run/roll number
            druhh = request.form['NameTypNahled']
            # print(str(druhh))
            rnm = request.form['rnm']
            datum = request.form['dt']
            # print(f'rnm {rnm} .......datum {datum}')
            # ak sa vlozil subor
            if request.files:
                # nacitaj pole file ,,v tomto pripade jeden
                textt = request.files['file[]']
                textaky = request.files.getlist('file[]')

                # skontroluje ci je zadane meno file
                if textt.filename == "":
                    return redirect(request.url)

                # skontroluje ci je mene file corrktne ,,txt    
                if allowed_image(textt.filename):  
                        
                # start = time.time()
                        for ff in textaky:                       
                            # start1 = time.time()
                            content = pd.read_csv(ff.stream)


                            # end1 = time.time()
                            # print("csv  "+str(# end1-start1))
                            # print(type(content))
                            # start2 = time.time()

                            # vymeni () za 0
                            content['Roll Number; 0']=content['Roll Number; 0'].str.replace('\(\)','0')
                            # odreze hlavicku txt file
                            content = content.iloc[3:]

                            # end2 = time.time()
                            # print("replace  "+str(# end2-# start2))
                            # start3 = time.time()

                            # doterazt to bolo v jednom stlpci Roll Number; 0 bteraz to rozhodime do viacerich
                            content = content.join(content['Roll Number; 0'].str.split(';', expand=True).add_prefix('rn'))
                            

                            # end3 = time.time()
                            # print("Roll Number; 0  "+str(# end3-# start3))
                            # start4 = time.time()

                            #odreze prve dva stlpce
                            content = content.iloc[:,2:143]
                            # odrey si osobitne datumy
                            cc = content.iloc[:,1]
                            # sprav deep copy
                            cc = cc.copy()
                            # nastavy vsetky hodnoty na pociatocny datum ktorz je zadany uzivatelom
                            cc.iloc[:]=datum                        
                            cc.iloc[:] = pd.to_datetime(cc.iloc[:])
                            # print(cc)
                            # end4 = time.time()
                            # # # print(".iloc[:,2:143]  "+str(# end4-# start4))
                            # start5 = time.time()
                            df = pd.DataFrame(content['rn1'])
                            df = df.copy()
                            # odstrani medzeri
                            df['rn1'] = df['rn1'].str.strip()
                            # pretypuje do time
                            df['rn1'] = pd.to_datetime(df['rn1'],format= '%H:%M:%S' ).dt.time
                            
                            cc = pd.DataFrame(cc)

                            
                            # pri prekroceni polnoci navysi datum ,,na zaklade porovnania velkosti 
                            for i in range(len(df.index)):
                                
                                if(i>0):
                                    
                                    t1 = timedelta(hours=df.iloc[i,0].hour, minutes=df.iloc[i,0].minute,seconds=df.iloc[i,0].second)
                                    t2 = timedelta(hours=df.iloc[i-1,0].hour, minutes=df.iloc[i-1,0].minute,seconds=df.iloc[i-1,0].second)

                                    if t1<t2:
                                        # print(i)
                                        cc.iloc[i:] += timedelta(days=1)
                                        # print(f'{t1}gg {t2} indexx {i}')
                            # pripoji datum                    
                            content['rn1'] = ''+ cc['rn2'].dt.strftime('%Y-%m-%d') + ' ' + content['rn1'].astype(str)
                            
                            # end4 = time.time()
                            # print(".iloc[:,2:143]  "+str(# end4-# start4))
                            # start5 = time.time()

                            # pripoji 
                    

                            # end5 = time.time()
                            # print("datum   "+str(# end5-# start5))
                            # start55 = time.time()
                            # content['rn1'] = content['rn1'].astype('datetime64[ns]')
                            # end55 = time.time()
                            # print("datum   "+str(# end55-# start55))
                            # start6 = time.time()

                            # nacita nazvy stlpcov tabuliek
                            try:    
                                cnxn = pyodbc.connect(session['session_dkmsspc0378'])
#                        except pyodbc.Error as ex:
                            except:
                                print(" -------------------------- error: " + str(sys.exc_info()[1]))
                            query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE (TABLE_NAME = N'MahloSpolu')"
                            output = pd.read_sql(query,cnxn)


                            # end6 = time.time()
                            # print("pd.read_sql_query  "+str(# end6-# start6))
                            # start7 = time.time()


                            output = output.iloc[3:]
                            output = np.array(output)   
                            valueString = ""


                            # end7 = time.time()
                            # print("np.array7  "+str(# end7-# start7))
                            # start8 = time.time()
                            # nonValueString=""
                            
                            for i in range(len(content.columns)):
                                
                                content.columns.values[i] = output[i][0]
                                valueString  += " " + output[i][0]+","
                                # print(f"{valueString} a {content.columns.values[i]}")


                                # nonValueString += " :" + output[i][0]+","                   
                            valueString = valueString[1:-1]

                            # end8 = time.time()
                            # print("content.columns.values  "+str(# end8-# start8))
                            # nonValueString = nonValueString[1:-1]


                            valueString = "PRODUCTION_RUN, DRUH, " + valueString


                                # nonValueString = ":PRODUCTION_RUN, " + nonValueString
                                # start9 = time.time()

                        
                            ska =""
                            for i in range(143):
                                ska += " ? ,"
                            ska = ska[1:-1]
                            

                            # end9 = time.time()
                            # print("ska[1:-1]  "+str(# end9-# start9))
                            # # print(valueString) 
                            # # print(nonValueString) 
                            content = content.fillna(0)

                            qa =  "INSERT INTO MahloSpolu("+ valueString+") VALUES("+ska+")"
                            content.insert(0, "DRUH", druhh)
                            content.insert(0, "PRODUCTION_RUN", rnm)
                            
                            
                            # end9 = time.time()
                            # print("qwa  "+str(end9-# start9))
                            # content = content.to_dict(orient='records')
                            # with engine.connect() as con:
                                
                            #     ss = text("%s" % qa).execution_options(autocommit=True)
                            #     for cont in content:
                            #         con.execute(ss, **cont)
                            
                                
                            # print(content)
                            
                                #sqlstate = ex.args[1]
                                #print(sqlstate)
                        cursor = cnxn.cursor()
                        # start9 = time.time()
                        params = list(tuple(row) for row in content.values)
                        # end9 = time.time()
                        # start9 = time.time()
                        # print(params)
                        # print(qa)
                        cursor.fast_executemany = True
                        cursor.executemany(qa, params)
                        cnxn.commit()
                        cursor.close()
                        cnxn.close() 
                        # end = time.time()
                        # print("cas  "+str(end-start9))
                        return redirect(request.url)
                else:
                    # print("That file extension is not allowed")
                    flash('Nebyl vybrán správný typ souboru!')
                    return redirect(request.url)

                # return redirect(request.url)
            else:
                
                flash('Nebyl vybrán soubor!')
                return redirect(request.url)
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  

        cursor = cnxn.cursor()
        listOfPRun = list(cursor.execute('SELECT DISTINCT PRODUCTION_RUN FROM MahloSpolu').fetchall())
        listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id FROM TypPrudct').fetchall())

    return render_template("Pridaj.html",listOfPRun=listOfPRun,listOfPDruh=listOfPDruh)

@app.route("/pridajTM", methods=[ 'POST', 'GET'])
def pridajTM():
    AdminAuth()
    # druhh = request.form['druh']
    # idDruh = request.form['druh']
    if request.method == "POST":
        idDruh = request.form['druh']
        nazov = request.form['nazov']
        ltl = request.form['ltl']
        utl = request.form['utl']
        print(f"   {nazov}  {ltl} {utl}")
        try:    
            cnxn = pyodbc.connect(session['session_dkmsspc0378'])
        except:
            print(" -------------------------- error: " + str(sys.exc_info()[1]))
        with cnxn:  

            cursor = cnxn.cursor()
            cursor.execute("INSERT INTO MahloTrecMat (IDDRUH,NAZOV,LTL,UTL) VALUES ( '"+idDruh+"','"+nazov+"', '"+ltl+"', '"+utl+"')")
        return redirect(request.url)

    else:
        try:    
            cnxn = pyodbc.connect(session['session_dkmsspc0378'])
        except:
            print(" -------------------------- error: " + str(sys.exc_info()[1]))
        with cnxn:  

            cursor = cnxn.cursor()
            # cursor.execute("INSERT INTO MahloTrecMat (IDDRUH,NAZOV,LTL,UTL) VALUES ( '"+idDruh+"','"+nazov+"', '"+ltl+"', '"+utl+"')")
            listOfPDruh = list(cursor.execute('SELECT distinct TypPrudct.name,TypPrudct.id FROM TypPrudct order by id asc').fetchall())
        return render_template("TrecieMaterialy.html",listOfPDruh=listOfPDruh)

@app.route("/getDates", methods=[ "POST"])
def getDates():
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn: 
        cursor = cnxn.cursor()
        dates = cursor.execute('SELECT distinct TRY_CONVERT(DATE,ROW_DATETIME) from MahloSpolu').fetchall()
    a = []
    for row in dates:      
        # print(row[0])         
        mojDT = datetime.strptime(row[0], '%Y-%m-%d')
        a.append(mojDT.strftime('%Y-%m-%d'))
    # print(a)
    return jsonify(a)

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

# @celery.task(name="tasker",bind=True)
# def add_together(a, b):
#     return a + b
def setPixels(c1,c2,utl,ltl,jsondata):
    seg = (utl-ltl)/16
    obrazok = np.zeros(shape=(c1,c2,3), dtype=np.uint8)
    obrazok[(jsondata == 0)]=[191, 191, 191]
    obrazok[(jsondata >= 0.0001) & (jsondata < ltl)]=[15, 182, 173]
    obrazok[(jsondata >= ltl) & (jsondata < ltl + 1 * seg)]=[252, 255, 62]
    obrazok[(jsondata >= ltl + 1 * seg) & (jsondata < ltl + 2 * seg)]=[224, 236, 55]
    obrazok[(jsondata >= ltl + 2 * seg) & (jsondata < ltl + 3 * seg)]=[195, 217, 47]
    obrazok[(jsondata >= ltl + 3 * seg) & (jsondata < ltl + 4 * seg)]=[166, 198, 39]
    obrazok[(jsondata >= ltl + 4 * seg) & (jsondata < ltl + 5 * seg)]=[137, 179, 31]
    obrazok[(jsondata >= ltl + 5 * seg) & (jsondata < ltl + 6 * seg)]=[109, 161, 24]
    obrazok[(jsondata >= ltl + 6 * seg) & (jsondata < ltl + 7 * seg)]=[66, 133, 13]
    obrazok[(jsondata >= ltl + 7 * seg) & (jsondata < ltl + 8 * seg)]=[22, 104, 1]
    obrazok[(jsondata >= ltl + 8 * seg) & (jsondata < ltl + 9 * seg)]=[22, 104, 1]
    obrazok[(jsondata >= ltl + 9 * seg) & (jsondata < ltl + 10 * seg)]=[66,133,13]
    obrazok[(jsondata >= ltl + 10 * seg) & (jsondata < ltl + 11 * seg)]=[109,161,24]
    obrazok[(jsondata >= ltl + 11 * seg) & (jsondata < ltl + 12 * seg)]=[155,146,28]
    obrazok[(jsondata >= ltl + 12 * seg) & (jsondata < ltl + 13 * seg)]=[161,129,24]
    obrazok[(jsondata >= ltl + 13 * seg) & (jsondata < ltl + 14 * seg)]=[161,102,24]
    obrazok[(jsondata >= ltl + 14 * seg) & (jsondata < ltl + 15 * seg)]=[161,78,22]
    obrazok[(jsondata >= ltl + 15 * seg) & (jsondata < utl)]=[161, 63, 24]
    obrazok[(jsondata >= utl) & (jsondata < 10000000000000)]=[255, 0, 0]

    return obrazok
def getPercetage(utl,ltl,jsondata,c1,c2):
    seg = (utl-ltl)/16
    count10,count11,count12,count13,count14,count15,count16 = 0,0,0,0,0,0,0
    count = np.count_nonzero(jsondata == 0)   
    count1 = np.count_nonzero((jsondata >= 0.0001) & (jsondata < ltl))   
    count2 = np.count_nonzero((jsondata >= ltl) & (jsondata < ltl + 1 * seg))   
    count3 = np.count_nonzero((jsondata >= ltl + 1 * seg) & (jsondata < ltl + 2 * seg))   
    count4 = np.count_nonzero((jsondata >= ltl + 2 * seg) & (jsondata < ltl + 3 * seg))   
    count5 = np.count_nonzero((jsondata >= ltl + 3 * seg) & (jsondata < ltl + 4 * seg))   
    count6 = np.count_nonzero((jsondata >= ltl + 4 * seg) & (jsondata < ltl + 5 * seg))   
    count7 = np.count_nonzero((jsondata >= ltl + 5 * seg) & (jsondata < ltl + 6 * seg))   
    count8 = np.count_nonzero((jsondata >= ltl + 6 * seg) & (jsondata < ltl + 7 * seg))   
    count9 = np.count_nonzero((jsondata >= ltl + 7 * seg) & (jsondata < ltl + 8 * seg))   
    count9 += np.count_nonzero((jsondata >= ltl + 8 * seg) & (jsondata < ltl + 9 * seg))   
    count10 += np.count_nonzero((jsondata >= ltl + 9 * seg) & (jsondata < ltl + 10 * seg))   
    count11 += np.count_nonzero((jsondata >= ltl + 10 * seg) & (jsondata < ltl + 11 * seg))   
    count12 += np.count_nonzero((jsondata >= ltl + 11 * seg) & (jsondata < ltl + 12 * seg))   
    count13 += np.count_nonzero((jsondata >= ltl + 12 * seg) & (jsondata < ltl + 13 * seg))   
    count14 += np.count_nonzero((jsondata >= ltl + 13 * seg) & (jsondata < ltl + 14 * seg))   
    count15 += np.count_nonzero((jsondata >= ltl + 14 * seg) & (jsondata < ltl + 15 * seg))   
    count16 += np.count_nonzero((jsondata >= ltl + 15 * seg) & (jsondata < utl))   
    count17 = np.count_nonzero((jsondata >= utl) & (jsondata < 10000000000000))   

    lst = [count1,count2,count3,count4,count5,count6,count7,count8,count9,count10,count11,count12,count13,count14,count15,count16,count17]
    new_lst = [f'{(i*100)/((c1*c2)-count):.2f}%' for i in lst]
    return new_lst,lst
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

@app.route("/get_img", methods=["POST"])
def get_img():
    ltl = float(request.form["ltl"])
    utl = float(request.form["utl"])
    casZaciatok = request.form["casZaciatok"]
    casKoniec = request.form["casKoniec"]
    typ = int(request.form["typ"])
    if(math.isnan(ltl)):
        ltl=0
    if(math.isnan(utl)):
        utl=0
    records = ""
    identity = request.form["identity"]
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        if "/" in identity:
            records = cursor.execute("SELECT * FROM (SELECT * FROM MahloSpolu where datediff(day, ROW_DATETIME, '"+str(identity)+"') = 0 ) a  where CAST(a.ROW_DATETIME AS TIME(0)) > '"+casZaciatok+"' and CAST(a.ROW_DATETIME AS TIME(0)) < '"+casKoniec+"' and DRUH = "+str(typ)+"").fetchall()
        else:
             records = cursor.execute("SELECT * FROM (SELECT * FROM MahloSpolu where  PRODUCTION_RUN = "+str(identity)+" ) a  where CAST(a.ROW_DATETIME AS TIME(0)) > '"+casZaciatok+"' and CAST(a.ROW_DATETIME AS TIME(0)) < '"+casKoniec+"' and DRUH = "+str(typ)+"").fetchall()
       
        mahlo_data_columns = cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'MahloSpolu'").fetchall()
    # print(records)
    # print(mahlo_data_columns)
    firstRecords = records[0]
    lastRecords = records[-1]
    jsondata = []
    dates = []

    for record in records:
        data = []

        for column in mahlo_data_columns:
            if column != mahlo_data_columns[0] and column  != mahlo_data_columns[1] and column  != mahlo_data_columns[2] and column  != mahlo_data_columns[3]:
                data.append(getattr(record, column[0]))

        jsondata.append(data)
        string  = " " + str((record.ROW_DATETIME).strftime('%H:%M:%S'))
        dates.append(string)

    cislo2 = 1400
    cislo1 = np.shape(jsondata)[0]*10

    jsondata = np.array(jsondata)
    c1 = int(cislo1/10)
    c2 = int(cislo2/10)

    obrazok = setPixels(c1,c2,utl,ltl,jsondata)
    new_lst,lst = getPercetage(utl,ltl,jsondata,c1,c2)
    histgramGen(lst,new_lst)
    jsondata[jsondata == 0] = np.nan

    meanis = np.nanmean(jsondata, axis=1)
    pxMeanis = setPixels(c1,1,utl,ltl,meanis)
    maxis = np.nanmax(jsondata, axis=1)
    pxMaxis = setPixels(c1,1,utl,ltl,maxis)
    minis = np.nanmin(jsondata, axis=1)
    pxMinis = setPixels(c1,1,utl,ltl,minis)

  
    new_image = Image.fromarray(obrazok)  
    imgMeanis = Image.fromarray(pxMeanis)  
    imgMaxis = Image.fromarray(pxMaxis)  
    imgMinis = Image.fromarray(pxMinis)  

    new_image = new_image.resize((new_image.width*10,new_image.height*20))
    imgMeanis = imgMeanis.resize((imgMeanis.width*45,imgMeanis.height*20))
    imgMaxis = imgMaxis.resize((imgMaxis.width*45,imgMaxis.height*20))
    imgMinis = imgMinis.resize((imgMinis.width*45,imgMinis.height*20))
    new_image = get_concat_h(imgMaxis,new_image)
    new_image = get_concat_h(imgMinis,new_image)
    new_image = get_concat_h(imgMeanis,new_image)
    


    new_image = add_margin(new_image,15,0,0,55,(255,255,255))

    draw = ImageDraw.Draw(new_image)
    fnt = ImageFont.truetype("arial.ttf", 15)

    draw.text((10,0),"TIME",(0,0,0),font=fnt)
    draw.text((65,0),"AVG",(0,0,0),font=fnt)
    draw.text((110,0),"MIN",(0,0,0),font=fnt)
    draw.text((150,0),"MAX",(0,0,0),font=fnt)
    draw.text((450,0),"HEAT-MAP for producion run '"+ str(firstRecords.PRODUCTION_RUN) + "', since '" + str(firstRecords.ROW_DATETIME) + "' till '" + str(lastRecords.ROW_DATETIME)+ " '" ,(0,0,0),font=fnt)

    for i,(date,meanss,minss,maxss) in enumerate(zip(dates,meanis,minis,maxis)):
        if(maxss >= 1000):
            draw.text((0, (i * 20)+15),"" + str(date) + " " + str(round(meanss,0))+ "  " + str(round(minss,0))+ "   " + str(round(maxss,0)),(0,0,0))
        elif(maxss >= 100):
            draw.text((0, (i * 20)+15),"" + str(date) + " " + str(round(meanss,1))+ "  " + str(round(minss,1))+ "   " + str(round(maxss,1)),(0,0,0))
        elif(maxss >= 10):
            draw.text((0, (i * 20)+15),"" + str(date) + " " + str(round(meanss,2))+ "  " + str(round(minss,2))+ "   " + str(round(maxss,2)),(0,0,0))       
        else:
            draw.text((0, (i * 20)+15),"" + str(date) + " " + str(round(meanss,3))+ "  " + str(round(minss,3))+ "   " + str(round(maxss,3)),(0,0,0))

    # new_image.save("C:\\Users\\kubackaiv\\mojRep\\1moje\\mahlo2\\mahlo2\\static\\img\\moj.png","PNG",optimize=False, compress_level=1)
    new_image.save(os.path.dirname(os.path.realpath(__file__)) + chr(92) + "static" + chr(92) + "img" + chr(92) + "moj.png","PNG",optimize=False, compress_level=1)
    str1 = "../static/img/moj.png"
    str2 = "../static/img/histogram.png"


    return jsonify(urlmoje=str1,urlHist=str2,lst=new_lst)


@app.route("/get_aktData", methods=["GET", "POST"])
def get_aktData():

    jsondata = []
    
    druh = request.form["druhLive"]
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
#except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        lastPRun = cursor.execute("SELECT MAX(PRODUCTION_RUN) FROM MahloSpolu").fetchone()
        # print(lastPRun[0])
        # records = session.query(MahloSpolu).filter(MahloSpolu.PRODUCTION_RUN == lastPRun,MahloSpolu.DRUH == druh).order_by(MahloSpolu.ID.desc()).limit(100)
        records = cursor.execute("SELECT TOP(100)* FROM MahloSpolu WHERE PRODUCTION_RUN = "+str(lastPRun[0])+"  AND DRUH = "+druh+" ORDER BY ID DESC").fetchall()

        mahlo_data_columns = cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'MahloSpolu'").fetchall()

    # firstRecords = session.query(MahloSpolu).order_by(MahloSpolu.ID).first()

    # lastRecords = session.query(MahloSpolu).order_by(MahloSpolu.ID.desc()).first()
    # print(records.count())
    
    for record in records:
        data = []

        for column in mahlo_data_columns:
            if column != mahlo_data_columns[0] and column != mahlo_data_columns[1] and column != mahlo_data_columns[2] and column != mahlo_data_columns[3]:
                data.append(getattr(record, column[0]))

        jsondata.append({
            "name": record.ROW_DATETIME,
            "data": data,
            "id" : record.ID,
            "druh" : record.DRUH
        })
 
    return jsonify(jsondata)
    
@app.route("/get_aktDataInterval", methods=["GET", "POST"])
def get_aktDataInterval():
    jsondata = []
    lastID = request.form["lastId"]
    druh = request.form["druh"]
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        lastPRun = cursor.execute("SELECT MAX(PRODUCTION_RUN) FROM MahloSpolu").fetchone()
        # records = session.query(MahloSpolu).filter(MahloSpolu.PRODUCTION_RUN == lastPRun[0],MahloSpolu.DRUH == druh,MahloSpolu.ID > lastID ).order_by(MahloSpolu.ID.asc()).all()
        records = cursor.execute("SELECT * FROM MahloSpolu WHERE PRODUCTION_RUN = "+str(lastPRun[0])+"  AND DRUH = "+druh+" AND ID > "+lastID+" ORDER BY ID ASC").fetchall()
        mahlo_data_columns = cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'MahloSpolu'").fetchall()

    # firstRecords = session.query(MahloSpolu).order_by(MahloSpolu.ID).first()
    # print(f'{lastID}  {druh}  {len(records)}')
    
    # lastRecords = session.query(MahloSpolu).order_by(MahloSpolu.ID.desc()).first()
    for record in records:
        data = []

        for column in mahlo_data_columns:
            if column != mahlo_data_columns[0] and column != mahlo_data_columns[1] and column != mahlo_data_columns[2] and column != mahlo_data_columns[3]:
                data.append(getattr(record, column[0]))

        jsondata.append({
            "name": record.ROW_DATETIME,
            "data": data,
            "id" : record.ID,
            "druh" : record.DRUH
        })
    # print(jsondata)
    return jsonify(jsondata)

@app.route("/get_existPRun", methods=["GET", "POST"])
def get_existPRun():
    production_run = request.form["productionRun"]
    typ = request.form["typ"]
    # print(production_run)
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        data = cursor.execute("SELECT TOP(1)* FROM MahloSpolu WHERE PRODUCTION_RUN = "+ production_run +"  AND DRUH = "+ typ +" ORDER BY ID DESC").fetchone()

    # udajeZam = session.query(MahloSpolu).filter(MahloSpolu.PRODUCTION_RUN == production_run,MahloSpolu.DRUH == druh).first()
    # data = MahloSpoluschema(many=False).dump(udajeZam)


    return json.dumps(not data)

@app.route("/get_existTR", methods=["GET", "POST"])
def get_existTR():
    TreciMat = request.form["TreciMat"]
    typ = request.form["typ"]
    # print(production_run)
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        data = cursor.execute("SELECT TOP(1)* FROM MahloTrecMat WHERE NAZOV = '"+ TreciMat +"'  AND IDDRUH = "+ typ +" ORDER BY ID DESC").fetchone()

    # udajeZam = session.query(MahloSpolu).filter(MahloSpolu.PRODUCTION_RUN == production_run,MahloSpolu.DRUH == druh).first()
    # data = MahloSpoluschema(many=False).dump(udajeZam)


    return json.dumps(not data)   
@app.route("/", methods=["GET", "POST"])
@app.route("/signup", methods=["GET", "POST"])
def signup():
    EvokeUserMonitoring(str(request.url))

    # region Nacitanie udajov z formu - get nAuditorID value

    nAuditorID=str("")
    sPassword=""

    # print("P A S S W O R D :   '" + sPassword + "'")

    try:
        sPassword = str(request.form['sPassword'])
    except:
        # print(sys.exc_info()[1])
        flash("Zadajte svoje ID a heslo.")
        return render_template("signup.html")
    # END TRY

    # print("P A S S W O R D :   '" + sPassword + "'")

    try:
        nAuditorID = str(request.form['nAuditorID'])
    except:
        flash("Zadajte svoje ID a heslo.")
        return render_template("signup.html")
    # END TRY

    #endregion

    # region Databaza - connect, a zistenie, ci sa tam dany user nachadza. premenna 'roleID', kontrola hesla (ak je vyzadovane) a tiez aj zavretie connectu

    c1 = round(((datetime.now()) - datetime(1970, 1, 1)).total_seconds())
    try:
        conn = pyodbc.connect(session['session_shaplmib013'])
    except:
        flash("Nedá sa pripojiť na požadovaný server (SHAPLMIB013)")
        return render_template("signup.html")
    # END TRY

    # ak je offline, tak daj hlasku, a neskusaj ist dalej
    c2 = round(((datetime.now()) - datetime(1970, 1, 1)).total_seconds())
    print("SIGNUP connection duration: " + str(c2-c1) + " SECONDS")
    if c2-c1>10:
        try: conn.close()
        except: pass
        flash("Nedá sa pripojiť na požadovaný server (SHAPLMIB013) (timeout 10 secs")
        return render_template("signup.html")
    # END IF

    c = conn.cursor()
    sCommand = "SELECT name, allowed, mahlo, admin FROM dbo.Auditors WHERE pers_nr = '" + str(nAuditorID) + "' AND password = '" + str(sPassword) + "'"
    c.execute(sCommand)
    results= c.fetchall()
    c.close()
    conn.close()			# close database connect before every return, or immediatelly when you don't need it anymore!

    #endregion

    # print("                                       ------------------------------- ID: " + str(nAuditorID))
    # print("                                       ----------------------------- PASS: " + str(sPassword))

    if len(results) ==0:
        flash("Nemáte oprávnenie")
        return render_template("signup.html")
    # END IF

    # region Vyhodnotenie prihlasenia

    if int(results[0][2]) !=1:
        flash(str(results[0][0]) + ", nemáte oprávnení")
        return render_template("signup.html")
    # END IF

    #endregion
    session['session_dkmsspc0378'] = "##########################################################################"
    session['session_shaplmib013'] = "##########################################################################"

    session['session_userLogged'] = nAuditorID
    session['session_admin'] = results[0][3]
    print( session['session_admin'] )
    return main()


@app.route("/del_VsetkyOzn", methods=["POST"])
def del_VsetkyOzn():
    AdminAuth()
    druh = request.form.getlist('poleVymaz[]')
    listToStr = ','.join(map(str, druh))
    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    #except pyodbc.Error as ex:
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        cursor.execute(" DELETE FROM MahloTrecMat WHERE id IN ("+listToStr+")")

    return "deleted"
@app.route("/update_VsetkyOzn", methods=["POST"])
def update_VsetkyOzn():
    AdminAuth()
    druh = eval(request.form.get('poleUpdate'))

    try:    
        cnxn = pyodbc.connect(session['session_dkmsspc0378'])
    except:
        print(" -------------------------- error: " + str(sys.exc_info()[1]))
    with cnxn:  
        cursor = cnxn.cursor()
        cursor.fast_executemany = True
        cursor.executemany('UPDATE MahloTrecMat SET LTL = ? ,UTL = ? WHERE ID = ?;', list(map(tuple,druh)))
    return "updated"