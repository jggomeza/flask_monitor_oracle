from flask import request, flash, redirect, Response
import urllib.request, json

# Packages
from . import app
from .models import Model



@app.route('/restart_password', methods=['POST'])
def restart_password():
    if str(request.values['user']).lower() != 'system' and str(request.values['user']).lower() != 'sys':
        if request.values['password'] == request.values['verify_password']:
            user=request.values['user']
            password=request.values['password']
            expire=True if 'expire' in request.values else False
            locked=True if 'locked' in request.values else False
            
            # _model = Model('DBA_TEST')
            _model = Model('KERUX')
            # _model.set_restart(user, password, expire, locked)
            
            flash('Clave actualizada satisfactoriamente!')
            return redirect('restart')
        else:
            flash('Las contraseñas ingresadas no coinciden!')
            return redirect('restart')
    else:
        flash('No puedes actualizar la clave de los usuarios (SYS o SYSTEM) por este panel!')
        return redirect('restart')
@app.route('/tablespaces/<dsn>')
def tablespaces(dsn):
    _model = Model(dsn)
    _data = {}
    _values = []

    for i in _model.get_tablespaces():
        _data['TABLESPACE_NAME'] = i[0]
        _data['SPACE_USED'] = i[1]
        _values.append(_data)
        _data = {}
    _json = json.dumps(_values)
    return _json

@app.route('/locked/<dsn>')
def locked(dsn):
    _model = Model(dsn)
    _data = {}
    _values = []

    for i in _model.get_locked():
        _data['SID'] = i[0]
        _data['SERIAL'] = i[1]
        _data['ORACLE_USERNAME'] = i[2]
        _data['OS_USER_NAME'] = i[3]
        _data['LOCKED_MODE'] = i[4]
        _data['STATUS'] = i[5]
        _data['MACHINE'] = i[6]
        _data['PROGRAM'] = i[7]
        _data['OWNER'] = i[8]
        _data['OBJECT_NAME'] = i[9]
        _data['OBJECT_TYPE'] = i[10]
        _values.append(_data)
        _data = {}
    _json = json.dumps(_values)
    return _json

@app.route('/inactives/<dsn>')
def inactives(dsn):
    _model = Model(dsn)
    _data = {}
    _values = []

    for i in _model.get_session_inactive():
        # _data['USERNAME'] = i[0]
        # _data['MACHINE'] = i[1]
        # _data['SID'] = i[2]
        # _data['SERIAL'] = i[3]
        # _data['STATUS'] = i[4]
        # _data['LOGON_TIME'] = i[5]
        # _data['TIEMPO_DE_INACTIVIDAD'] = i[6]
        _data['SESIONES_INACTIVAS'] = i[0]
        _values.append(_data)
        _data = {}
    _json = json.dumps(_values)
    return _json

@app.route('/collection')
def collection_banks():
    _model = Model('CYGNUS1')
    _data = {}
    _values = []

    bank=["BANCO DE VENEZUELA","BANCO DEL TESORO","BICENTENARIO","BANESCO","BANCO PROVINCIAL","BANCO MERCANTIL","BNC","BANCAMIGA","BANCO EXTERIOR","BANCO ACTIVO","BANCO SOFITASA","BANCO CARONI","BCV","100% BANCO","BOD","FONDO COMUN","TOTAL"]
    bank_list_recaudo=[]

    for i in _model.get_collection_banks():
        bank_list_recaudo.append(i[0].strip())
        _data['BANCO'] = i[0]
        _data['CANTIDAD'] = i[1]
        _values.append(_data)
        _data = {}
    
    for i in bank:
        if not i.strip() in bank_list_recaudo:
            _data['BANCO'] = i.strip()
            _data['CANTIDAD'] = 0
            _values.insert(len(_values)-1,_data)
            _data = {}

    _json = json.dumps(_values)
    return _json

@app.route('/dolartoday')
def dolartoday():
    try:
        url = "https://s3.amazonaws.com/dolartoday/data.json"
        response = urllib.request.urlopen(url)
        data = response.read()

        return  json.loads(data)
    except Exception as e:
        raise Exception(e)

@app.route('/tcseniat')
def tcseniat():
    try:
        link = "https://tcseniat.extra.bcv.org.ve/tcseniat/resources/TipoCambio/fechaOperacion"
        xml = urllib.request.urlopen(link)      # hace la petición al link del xml
        return  Response(xml, mimetype='text/xml')
    except Exception as e:
        raise Exception(e)