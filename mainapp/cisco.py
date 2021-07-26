import re

from flask import Flask, render_template, abort, Response,redirect,url_for
from .config import EXTERNAL_API_URL
from .src.cisco_config import get_content, get_date
from .src.cisco_parser import parse
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for,render_template_string
from flask_login import login_user,login_required,logout_user,current_user
import time,func_timeout
from .models import Hypervisor,IP_Pools
from . import db
from .models import CiscoModel
from .viewables_helper.helper import createCiscoData
cisco_new = Blueprint('cisco',__name__)

@cisco_new.route('/cisco')
@login_required
def cisco():
    return render_template('cisco/index.html', API_URL=EXTERNAL_API_URL)


@cisco_new.route('/addconfig')
@login_required
def add_cisco():
    return render_template('cisco/add_device.html')


@cisco_new.route('/raw/<int:config_id>')
@login_required
def raw(config_id):
    content = get_content()
    if content is None:
        abort(404)
    configs = [item for item in content['message']]
    config_id = config_id - 1
    if config_id < 0 or config_id > len(configs):
        abort(404)
    return Response(configs[config_id]['config'], mimetype="text/plain")


@cisco_new.route('/config/<int:config_id>')
@login_required
def config(config_id):

    todo = CiscoModel.query.get(config_id)
    response = {}
    response['id'] = todo.id
    response['user_id'] = todo.user_id
    response['global_delay_factor'] = todo.global_delay_factor
    response['device_type'] = todo.device_type
    response['username'] = todo.username
    response['ip'] = todo.ip
    response['secret'] = todo.secret
    response['verbose'] = todo.verbose


    response['status_code'] = 201

    return render_template('cisco/config.html',response = response )


@cisco_new.route('/devices')
@login_required
def devices():
    # content = get_content()
    # date = get_date(content)
    allCISCO = CiscoModel.query.filter_by(user_id=current_user.id)
    # allCISCO = [{'ip':'192.168.0.107','device_type':'mobil','id':2},{'ip':'192.168.0.107','device_type':'mobil','id':2},{'ip':'192.168.0.107','device_type':'mobil','id':2}]

    print("\n" * 3)
    print("date",allCISCO)
    print("\n" * 3)

    return render_template('cisco/devices.html',allCISCO = allCISCO)


@cisco_new.route('/vlan')

@login_required

def vlan():
    content = get_content()
    if content is None:
        abort(404)
    configs = [item for item in content['message']]
    selected_config = configs[-1]
    interfaces_vlan, _, _ = parse(-1, selected_config['config'])
    vlan_data = []
    for interface_vlan in interfaces_vlan:
        name = interface_vlan.text.split()[-1]
        vlan_id = int(re.findall('Vlan(\d+)', name)[0])
        d = {'id': vlan_id, 'name': name, 'description': '', 'subnet': ''}
        raw_data = ''.join([i.text for i in interface_vlan.children])
        result = re.findall(r'description "(.*?) (\d+)\.(\d+)\.(\d+)\.(\d+)/(\d+)"', raw_data)
        if result:
            result = result[0]
            (description, ip1, ip2, ip3, ip4, mask) = result
            d['description'] = description
            d['subnet'] = f'{ip1}.{ip2}.{ip3}.{ip4}/{mask}'
        vlan_data.append(d)
    return render_template('cisco/vlan.html', API_URL=EXTERNAL_API_URL, vlan_data=vlan_data)



@cisco_new.route('/add_device_new',methods=['POST'])
@login_required

def AddNewDeviceSenddevices():
   ip = request.form.get('ip')
   device_type = request.form.get('device_type')
   password = request.form.get('password')
   username = request.form.get('username')
   secret = request.form.get('secret')
   global_delay_factor = request.form.get('global_delay_factor')
   verbose = request.form.get('verbose')
   createCiscoData(current_user.id,ip, global_delay_factor,device_type,username,password,secret,verbose)
   flash('Cisco Record Created Succecssfully',category='success')
   return redirect(url_for('cisco.devices'))
