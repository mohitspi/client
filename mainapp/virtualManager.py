from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for,render_template_string
from flask_login import login_user,login_required,logout_user,current_user
import time,func_timeout
from .models import Hypervisor,IP_Pools
from . import db

virtualManager = Blueprint('virtualManager',__name__)

@virtualManager.route('/bridge')
@login_required
def bridge():
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    all_bridges = []
    for hypervisor in hypervisors:
        bridges = IP_Pools.query.filter_by(hypervisor=hypervisor.id,type="bridge")
        for bridge in bridges:
            mod_bridge = {}
            mod_bridge['network_name'] = bridge.network_name
            mod_bridge['bridge_interface_name'] = bridge.bridge_interface_name
            mod_bridge['hypervisor'] = hypervisor.hostname
            all_bridges.append(mod_bridge)
    return render_template("virtualManager/ip_pool/bridge/bridge.html",bridges=all_bridges)


@virtualManager.route('/create-bridge',methods=["POST","GET"])
@login_required
def create_bridge():
    if request.method == "POST":
        hostname = request.form.get('hypervisor')
        network_name = request.form.get('network_name')
        bridge_interface_name = request.form.get('bridge_interface_name')

        hypervisor = Hypervisor.query.filter_by(hostname=hostname,user_id=current_user.id).first()
        if not hypervisor:
            return render_template('response/response_basic.html',err_body="Something Wrong Happened")
        res = createBridgeNetwork(hostname,network_name,bridge_interface_name)
        print(res)
        if res['res'] == "Success":
            ip_pool = IP_Pools(
            user_id=current_user.id,
            hypervisor=hypervisor.id,
            type="bridge",
            network_name=network_name,
            bridge_interface_name=bridge_interface_name
            )
            db.session.add(ip_pool)
            db.session.commit()
            return redirect(url_for('sample.response_succ_view',succ_body="Virtual Network has been creadted successfully"))
        else:
            return render_template('response/response_basic.html',err_body=res['reason'])
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    return render_template("virtualManager/ip_pool/bridge/create_bridge.html",hypervisors=hypervisors)

def createBridgeNetwork(hostname,network_name,bridge_interface_name):
    xml = f'''
        <network>
            <name>{network_name}</name>
            <forward mode="bridge" />
            <bridge name="{bridge_interface_name}" />
        </network>
    '''
    print(xml)

    try:
        try:
            conn = libvirtHypervisorConnect(hostname)
        except:
            return {
            "res" : "Error",
            "reason" : "Failed To Connect"
        }

        network = conn.networkDefineXML(xml)
        network.create()
        return {
            "res" : "Success"
        }
    except libvirt.libvirtError as e:
        return {
            "res" : "Error",
            "reason" : str(e)
        }


@virtualManager.route('/nat')
@login_required
def nat():
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    all_nat = []
    for hypervisor in hypervisors:
        nats = IP_Pools.query.filter_by(hypervisor=hypervisor.id,type="nat")
        for nat in nats:
            print(nat)
            mod_nat = {}
            mod_nat['network_name'] = nat.network_name
            mod_nat['bridge_interface_name'] = nat.bridge_interface_name
            mod_nat['ip'] = nat.ip
            mod_nat['hypervisor'] = hypervisor.hostname
            all_nat.append(mod_nat)
    print(all_nat)
    return render_template("virtualManager/ip_pool/nat/nat.html",nats=all_nat)

@virtualManager.route('/create-nat',methods=["POST","GET"])
@login_required
def create_nat():
    if request.method == "POST":
        hostname = request.form.get('hypervisor')
        network_name = request.form.get('network_name')
        nat_start = request.form.get('nat_start')
        nat_end = request.form.get('nat_end')
        
        bridge_interface_name = request.form.get('bridge_interface_name')

        ip = request.form.get('ip')
        netmask = request.form.get('netmask')
        dhcp_start = request.form.get('dhcp_start')
        dhcp_end = request.form.get('dhcp_end')

        print(hostname)
        hypervisor = Hypervisor.query.filter_by(hostname=hostname,user_id=current_user.id).first()
        if not hypervisor:
            return render_template('response/response_basic.html',err_body="Something Wrong Happened")
        res = createNatNetwork(hostname,network_name,nat_start,nat_end,ip,netmask,bridge_interface_name,dhcp_start,dhcp_end)
        print(res)
        if res['res'] == "Success":
            ip_pool = IP_Pools(
                user_id=current_user.id,
                hypervisor=hypervisor.id,
                type="nat",
                network_name=network_name,
                nat_start=nat_start,
                nat_end=nat_end,
                bridge_interface_name=bridge_interface_name,
                ip=ip,
                netmask=netmask,
                dhcp_start=dhcp_start,
                dhcp_end=dhcp_end,  
            )
            db.session.add(ip_pool)
            db.session.commit()
            return redirect(url_for('sample.response_succ_view',succ_body="Virtual Network has been creadted successfully"))
        else:
            return render_template('response/response_basic.html',err_body=res['reason'])
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    return render_template("virtualManager/ip_pool/nat/create_nat.html",hypervisors=hypervisors)

def createNatNetwork(hostname,network_name,nat_start,nat_end,ip,netmask,bridge_interface_name,dhcp_start,dhcp_end):
    xml = f'''
    <network>
    <name>{network_name}</name>
    <forward mode='nat'>
        <nat>
            <port start="{nat_start}" end="{nat_end}"/>
        </nat>
    </forward>
    <bridge name="{bridge_interface_name}" stp='on' delay='0'/>
    <ip address='{ip}' netmask='{netmask}'>
        <dhcp>
            <range start="{dhcp_start}" end="{dhcp_end}" />
        </dhcp>
    </ip>
    </network>
    '''
    print(xml)
    try:
        try:
            conn = libvirtHypervisorConnect(hostname)
        except:
            return {
            "res" : "Error",
            "reason" : "Failed To Connect"
        }

        network = conn.networkDefineXML(xml)
        network.create()
        return {
            "res" : "Success"
        }
    except libvirt.libvirtError as e:
        return {
            "res" : "Error",
            "reason" : str(e)
        }


@virtualManager.route('/host-only')
@login_required
def host_only():
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    all_host_only = []
    for hypervisor in hypervisors:
        host_onlys = IP_Pools.query.filter_by(hypervisor=hypervisor.id,type="host-only")
        for host_only in host_onlys:
            mod_host_only = {}
            mod_host_only['network_name'] = host_only.network_name
            mod_host_only['bridge_interface_name'] = host_only.bridge_interface_name
            mod_host_only['ip'] = host_only.ip
            mod_host_only['hypervisor'] = hypervisor.hostname
            all_host_only.append(mod_host_only)
    return render_template("virtualManager/ip_pool/host_only/host_only.html",all_host_only=all_host_only)

@virtualManager.route('/create-host-only',methods=["POST","GET"])
@login_required
def create_host_only():
    if request.method == "POST":
        hostname = request.form.get('hypervisor')
        network_name = request.form.get('network_name')
        
        bridge_interface_name = request.form.get('bridge_interface_name')

        ip = request.form.get('ip')
        netmask = request.form.get('netmask')
        dhcp_start = request.form.get('dhcp_start')
        dhcp_end = request.form.get('dhcp_end')

        print(hostname)
        hypervisor = Hypervisor.query.filter_by(hostname=hostname,user_id=current_user.id).first()
        if not hypervisor:
            return render_template('response/response_basic.html',err_body="Something Wrong Happened")
        res = createHostOnlyNetwork(hostname,network_name,ip,netmask,bridge_interface_name,dhcp_start,dhcp_end)
        print(res)
        if res['res'] == "Success":
            ip_pool = IP_Pools(
                user_id=current_user.id,
                hypervisor=hypervisor.id,
                type="host-only",
                network_name=network_name,
                bridge_interface_name=bridge_interface_name,
                ip=ip,
                netmask=netmask,
                dhcp_start=dhcp_start,
                dhcp_end=dhcp_end,  
            )
            db.session.add(ip_pool)
            db.session.commit()
            return redirect(url_for('sample.response_succ_view',succ_body="Virtual Network has been creadted successfully"))
        else:
            return render_template('response/response_basic.html',err_body=res['reason'])
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    return render_template("virtualManager/ip_pool/host_only/create_host_only.html",hypervisors=hypervisors)

def createHostOnlyNetwork(hostname,network_name,ip,netmask,bridge_interface_name,dhcp_start,dhcp_end):
    xml = f'''
        <network>
            <name>{network_name}</name>
            <bridge name="{bridge_interface_name}" stp='on' delay='0'/>
            <ip address="{ip}" netmask="{netmask}" >
                <dhcp>
                <range start="{dhcp_start}" end="{dhcp_end}" />
                </dhcp>
            </ip>
        </network>
    '''
    print(xml)
    try:
        try:
            conn = libvirtHypervisorConnect(hostname)
        except:
            return {
            "res" : "Error",
            "reason" : "Failed To Connect"
        }

        network = conn.networkDefineXML(xml)
        network.create()
        return {
            "res" : "Success"
        }
    except libvirt.libvirtError as e:
        return {
            "res" : "Error",
            "reason" : str(e)
        }


# HELPER
@func_timeout.func_set_timeout(2)
def libvirtHypervisorConnect(hostname):
    return libvirt.open("qemu+ssh://root@{}/system".format(hostname))

@virtualManager.route('/super-test',methods=["POST","GET"])
@login_required
def super_test():
    hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
    for hypervisor in hypervisors:
        conn = libvirtHypervisorConnect(hypervisor.hostname)
        networks = conn.listNetworks()
        for network in networks:
            print(network)
    return jsonify({})