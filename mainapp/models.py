from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


class CiscoModel(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    ip = db.Column(db.String(30))
    device_type = db.Column(db.String(200))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    secret = db.Column(db.String(100))
    global_delay_factor = db.Column(db.String(100))
    verbose =  db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))




class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(30))
    mysecret = db.Column(db.String(200))
    apitoken = db.Column(db.String(200))
    simplepass = db.Column(db.String(100))
    sshkey = db.relationship('SshKey')
    Iperf = db.relationship('Iperf')
    userInfo =  db.Column(db.String(10),default="USER")
    hypervisor = db.relationship('Hypervisor')
    machines = db.relationship('Mechine')
    ip_pools = db.relationship('IP_Pools')

class Iperf(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    result = db.Column(db.String(1000))
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class SshKey(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    ssh = db.Column(db.String(300))
    name = db.Column(db.String(25))

class Hypervisor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # user = db.Column(db.String(30))
    hostname = db.Column(db.String(30))
    mechines = db.relationship('Mechine')
    ip_pools = db.relationship('IP_Pools')

class Mechine(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    hypervisor = db.Column(db.Integer,db.ForeignKey('hypervisor.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    uuidString = db.Column(db.String(60))
    vmName = db.Column(db.String(60))
    storage = db.Column(db.Integer)
    memory = db.Column(db.Integer)

class Dnsmasq(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    ip_address = db.Column(db.String(60))
    mac = db.Column(db.String(60))

class IP_Pools(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    hypervisor = db.Column(db.Integer,db.ForeignKey('hypervisor.id'))
    type = db.Column(db.String(60),default="")
    network_name = db.Column(db.String(60),default="")
    bridge_interface_name = db.Column(db.String(60),default="")

    nat_start = db.Column(db.String(15),default="")
    nat_end = db.Column(db.String(15),default="")

    ip = db.Column(db.String(15),default="")
    netmask = db.Column(db.String(15),default="")
    

    # interface_name = db.Column(db.String(15),default="")

    dhcp_start = db.Column(db.String(15),default="")
    dhcp_end = db.Column(db.String(15),default="")
    
    

class Windows(db.Model):
   __bind_key__ = 'db2' 
   id = db.Column(db.Integer,primary_key=True)
   execution_policy = db.Column(db.String(3))
   quick_config = db.Column(db.String(20))

class Debian(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer,primary_key=True)
    country = db.Column(db.String(40))
    country_name = db.Column(db.String(40))
    disk = db.Column(db.String(40))
    filesystem = db.Column(db.String(40))
    guided_size = db.Column(db.String(40))
    install_addition = db.Column(db.String(40))
    interface = db.Column(db.String(40))
    language = db.Column(db.String(40))
    language_name_fb = db.Column(db.String(40))
    layoutcode = db.Column(db.String(40))
    locale = db.Column(db.String(40))
    method =db.Column(db.String(40))
    multi_language_environment = db.Column(db.String(40))
    xkbkeymap =	db.Column(db.String(40))
    partition_method =	db.Column(db.String(40))
    recipe	= db.Column(db.String(40))