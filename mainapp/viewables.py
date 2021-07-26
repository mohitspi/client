from re import S
import re
# from types import MethodDescriptorType
from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for,render_template_string
from flask_login import login_user,login_required,logout_user,current_user
from . import db,BACKEND_URL
import json,requests
from .models import SshKey,Iperf,User,Hypervisor,Mechine,Dnsmasq,IP_Pools

import threading,os,stat
import subprocess

from .viewables_helper import getDebianContext,getWindowsContext,createSSHKey,getServers,\
   getServersJson,getResult,iperfRes,run_web_ssh_TORNADO,getCFGI_COMMANDS,updateChart,libvirtHypervisorConnect
from subprocess import TimeoutExpired, check_output
import io,json,base64

import sys
import xml.etree.ElementTree as ET
import uuid,random,string

import pexpect
from getpass import getpass
import os
import sys
import subprocess,paramiko,time

viewables = Blueprint('viewables',__name__)


@viewables.route('/')
@login_required
def home():
   return render_template('views/home.html')

@viewables.route('/index')
@login_required
def index():
   return render_template('viewables/index.html')



# API PROCESS
@viewables.route('/api/generate/debian/server/<conf_name>/<level>/', methods=['POST'])
@login_required
def debianPOSTAPI(conf_name, level):
   locale =  request.form.get('locale')
   language =  request.form.get('language')
   country =  request.form.get('country')
   multi_locale = '0' if  request.form.get('multi_locale')==None else request.form.get('multi_locale')
   multi_language_environment =  request.form.get('multi_language_environment')
   allow_unauthenticated =  request.form.get('allow_unauthenticated')     

   xkb_keymap =  request.form.get('xkb_keymap')  
   language_name_fb =  request.form.get('language_name_fb')  
   country_name =  request.form.get('country_name')  
   layoutcode =  request.form.get('layoutcode')  

   # 3
   choose_interface =  request.form.get('choose_interface')
   ipv4 = '0' if request.form.get('ipv4')==None else request.form.get('ipv4')

   ipv4_address =  request.form.get('ipv4_address')
   ipv4_netmask =  request.form.get('ipv4_netmask')
   ipv4_gateway =  request.form.get('ipv4_gateway')
   ipv4_nameserver =  request.form.get('ipv4_nameserver')
   dns_server =  request.form.get('dns_server')
   
   dhcp_timeout =  request.form.get('dhcp_timeout')
   # 4
   get_hostname =  request.form.get('get_hostname')
   get_domain =  request.form.get('get_domain')
   root_login = '0' if  request.form.get('root_login')==None else request.form.get('root_login')
   make_user = '0' if  request.form.get('make_user')==None else request.form.get('make_user')
   root_password =  request.form.get('root_password')
   root_password_again =  request.form.get('root_password_again')
   allow_password_weak = '0' if request.form.get('allow_password_weak')==None else request.form.get('allow_password_weak')
   encrypt_home = '0' if request.form.get('encrypt_home')==None else request.form.get('encrypt_home')
   # 5
   clock_setup =  request.form.get('clock_setup')
   time_zone =  request.form.get('time_zone')
   ntp = '0' if  request.form.get('ntp')==None else request.form.get('ntp')
   ntp_server_address =  request.form.get('ntp_server_address')
   # 6
   device_remove_lvm_span ='0' if request.form.get('device_remove_lvm_span')==None else request.form.get('device_remove_lvm_span')
   purge_lvm_from_device =  '0' if  request.form.get('purge_lvm_from_device')==None else request.form.get('purge_lvm_from_device')
   partman_lvm_method =  '0' if request.form.get('partman_lvm_method')==None else request.form.get('partman_lvm_method')
   device_remove_lvm = '0' if  request.form.get('device_remove_lvm')==None else request.form.get('device_remove_lvm')
   device_remove_md =  '0' if request.form.get('device_remove_md')==None else request.form.get('device_remove_md')
   confirm_nooverwrite = '0' if  request.form.get('confirm_nooverwrite')==None else request.form.get('confirm_nooverwrite')
   no_boot = '0' if  request.form.get('no_boot')==None else request.form.get('no_boot')
   # 7
   guided_size =  request.form.get('guided_size')
   choose_recipe =  request.form.get('choose_recipe')
   default_filesystem =  request.form.get('default_filesystem')
   disk =  request.form.get('disk')
   new_vg_name =  request.form.get('new_vg_name')
   boot_size =  request.form.get('boot_size')
   no_swap = '0' if  request.form.get('no_swap')==None else request.form.get('no_swap')
   swap_size =  request.form.get('swap_size')
   root_size =  request.form.get('root_size')
   usr_size =  request.form.get('usr_size')
   home_size =  request.form.get('home_size')
   tmp_size =  request.form.get('tmp_size')
   var_size =  request.form.get('var_size')
   # 8
   confirm_write_new_label = '0' if request.form.get('confirm_write_new_label')==None else request.form.get('confirm_write_new_label')
   choose_partition_method = request.form.get('choose_partition_method')
   # 9
   apt_setup_cdrom = '0' if  request.form.get('apt-setup/cdrom')==None else request.form.get('apt-setup/cdrom')
   country =  request.form.get('country')
   # choose_interface =  request.form.get('choose_interface') # Duplicate :(
   selectpicker =  request.form.get('selectpicker')

   # WILL HELP YOU TO DEBUG
   print(locale,'locale')
   print(language,'language')
   print(country,'country')
   print(multi_locale,'multi_locale')
   print(multi_language_environment,'multi_language_environment')
   print(allow_unauthenticated,'allow_unauthenticated')
   # 2
   print(xkb_keymap,'xkb_keymap')
   print(language_name_fb,'language_name_fb')
   print(country_name,'country_name')
   print(layoutcode,'layoutcode')
   # 3
   print(choose_interface,'choose_interface')
   print(ipv4,'ipv4')

   print(ipv4_address,'ipv4_address')
   print(ipv4_netmask,'ipv4_netmask')
   print(ipv4_gateway,'ipv4_gateway')
   print(ipv4_nameserver,'ipv4_nameserver')
   print(dns_server,'dns_server')
   
   print(dhcp_timeout,'dhcp_timeout')
   #4
   print(get_hostname,'get_hostname')
   print(get_domain,'get_domain')
   print(root_login,'root_login')
   print(make_user,'make_user')
   print(root_password,'root_password')
   print(root_password_again,'root_password_again')
   print(allow_password_weak,'allow_password_weak')
   print(encrypt_home,'encrypt_home')
   # 5
   print(clock_setup,'clock_setup')
   print(time_zone,'time_zone')
   print(ntp,'ntp')
   print(ntp_server_address,'ntp_server_address')
   # 6
   print(device_remove_lvm_span,'device_remove_lvm_span')
   print(purge_lvm_from_device,'purge_lvm_from_device')
   print(partman_lvm_method,'partman_lvm_method')
   print(device_remove_lvm,'device_remove_lvm')
   print(device_remove_md,'device_remove_md')
   # print(confirm,'confirm')
   print(confirm_nooverwrite,'confirm_nooverwrite')
   print(no_boot,'no_boot')
   # 7
   print(guided_size,'guided_size')
   print(choose_recipe,'choose_recipe')
   print(default_filesystem,'default_filesystem')
   print(disk,'disk')
   print(new_vg_name,'new_vg_name')
   print(boot_size,'boot_size')
   print(no_swap,'no_swap')
   print(swap_size,'swap_size')
   print(root_size,'root_size')
   print(usr_size,'usr_size')
   print(home_size,'home_size')
   print(tmp_size,'tmp_size')
   print(var_size,'var_size')
   # 8
   print(confirm_write_new_label,'confirm_write_new_label')
   print(choose_partition_method,'choose_partition_method')
   # print(confirm,'confirm')
   # 9
   print(apt_setup_cdrom,'apt_setup_cdrom')
   print(country,'country')
   print(choose_interface,'choose_interface')
   print(selectpicker,'selectpicker')
   # 
   print(conf_name,level)
   # json
   payload = {
      'email' : current_user.email,
      'mysecret' : current_user.mysecret,
      'simplepass' : current_user.simplepass,
         'autoGenerate' : 'debian',
         'conf_name' : conf_name,
         'level' : level,
         'locale':locale,
         'language':language,
         # 'country':country,
         'multi_locale':multi_locale,
         'multi_language_environment':multi_language_environment,
         'allow_unauthenticated':allow_unauthenticated,

         'xkb_keymap':xkb_keymap,
         'language_name_fb':language_name_fb,
         'country_name':country_name,
         'layoutcode':layoutcode,

         'choose_interface':choose_interface,
         'ipv4':ipv4,
         'ipv4_address':ipv4_address,
         'ipv4_netmask':ipv4_netmask,
         'ipv4_gateway':ipv4_gateway,
         'ipv4_nameserver':ipv4_nameserver,
         'dns_server':dns_server,         
         'dhcp_timeout':dhcp_timeout,

         'get_hostname':get_hostname,
         'get_domain':get_domain,
         'root_login':root_login,
         'make_user':make_user,
         'root_password':root_password,
         'root_password_again':root_password_again,
         'allow_password_weak':allow_password_weak,
         'encrypt_home':encrypt_home,

         'clock_setup':clock_setup,
         'time_zone':time_zone,
         'ntp':ntp,
         'ntp_server_address':ntp_server_address,

         'device_remove_lvm_span':device_remove_lvm_span,
         'purge_lvm_from_device':purge_lvm_from_device,
         'partman_lvm_method':partman_lvm_method,
         'device_remove_lvm':device_remove_lvm,
         'device_remove_md':device_remove_md,
         # 'confirm':confirm,
         'confirm_nooverwrite':confirm_nooverwrite,
         'no_boot':no_boot,

         'guided_size':guided_size,
         'choose_recipe':choose_recipe,
         'default_filesystem':default_filesystem,
         'disk':disk,
         'new_vg_name':new_vg_name,
         'boot_size':boot_size,
         'no_swap':no_swap,
         'swap_size':swap_size,
         'root_size':root_size,
         'usr_size':usr_size,
         'home_size':home_size,
         'tmp_size':tmp_size,
         'var_size':var_size,

         'confirm_write_new_label':confirm_write_new_label,
         'choose_partition_method':choose_partition_method,
         # 'confirm':confirm,
         'apt_setup_cdrom':apt_setup_cdrom,
         'country':country,
         # 'choose_interface':choose_interface,
         'selectpicker':selectpicker,

   }
   sendRes = requests.post(BACKEND_URL+'auth/api/authenticate/AddConfig', data=json.dumps(payload))
   data = sendRes.json()
   if data['res'] == 'SUCCESS':
      output = data['output']
      return render_template_string(output)
   else:
      return data

@viewables.route('/api/generate/debian/server/<conf_name>/<level>/')
@login_required
def debianGET(conf_name, level):
    context = getDebianContext()
    return render_template('viewables/inputs/debian/debian_input.html', autoGenerate='debian', level=level, conf_name=conf_name, context=context)



# API PROCESS
@viewables.route('/api/myconfigs')
@login_required
def myConfigsAPI():
   payload = {
      'email' : current_user.email,
      'mysecret' : current_user.mysecret,
      'simplepass' : current_user.simplepass,
   }
   sendRes = requests.post(BACKEND_URL+'auth/api/authenticate/getAllconfigs', data=json.dumps(payload))
   data = sendRes.json()
   return render_template('viewables/myconfigs/myconfigs.html',data = data)

# API PROCESS
@viewables.route('/api/getmyconfig',methods=['POST'])
@login_required
def getMyConfigAPI():
   that_id = request.form.get('val')
   payload = {
      'that_id' : that_id,
      'email' : current_user.email,
      'mysecret' : current_user.mysecret,
      'simplepass' : current_user.simplepass,
   }
   sendRes = requests.post(BACKEND_URL+'auth/api/authenticate/getMyConfig', data=json.dumps(payload))
   data = sendRes.json()
   output = data['output']
   return render_template_string(output)
   # return render_template('viewables/myconfigs/config.html', autoGenerate=data['autoGenerate'], data=data , language=data['language'], conf_name=data['conf_name'], level=data['level'])



# ---------------------------------------------SSH FUTURE----------------------
# FUTURE
@viewables.route('/addSSH')
@login_required
def addSSH():
   allSSH = SshKey.query.filter_by(user_id=current_user.id)
   return render_template('viewables/addSSH/add_ssh.html',allSSH=allSSH)

# FUTURE
@viewables.route('/addSSH',methods=['POST'])
@login_required
def createSSH():
   ssh = request.form.get('ssh_key')
   name = request.form.get('name')
   createSSHKey(current_user.id,ssh,name)
   flash('SSH Key Created Succecssfully',category='success')
   allSSH = SshKey.query.filter_by(user_id=current_user.id)
   return render_template('viewables/addSSH/add_ssh.html',allSSH=allSSH)


@viewables.route('/Ookla')
@login_required
def ookla():
   serverList = getServersJson()
   return render_template('viewables/speedtest/Ookla.html',serverList=serverList)

@viewables.route('/Ookla_Result',methods=['POST'])
def ooklaPost():
   data = request.data
   jsonData = json.loads(data)

   result = getResult(jsonData['code'])
   obj = {
      "Jitter" : str(result['ping']['jitter']) +" ms",
      "Latency" : str(result['ping']['latency']) + " ms",
      "Download" : str("{0:.2f}".format(int(result['download']['bandwidth'])*0.0000076294)) + " Mbps",
      "Upload" : str("{0:.2f}".format(int(result['upload']['bandwidth'])*0.0000076294)) + " Mbps",
      "Packet Loss" : str("{0:.2f}".format(int(result['packetLoss']))) + " %",
      "Isp" : result['isp'],
      "Location" : result['server']['location'],
      "Server" : result['server']['name'],
   }
   return jsonify(obj)


@viewables.route('/iperf')
@login_required
def iperf():
   return render_template('viewables/speedtest/iperf.html')


@viewables.route('/iperf_Result',methods=['POST'])
@login_required
def iperfPost():
   data = request.data
   jsonData = json.loads(data)

   host,port,para = jsonData['host_name'],jsonData['port'],jsonData['para']
   out = iperfRes(host,port,para)
   out = out.decode()
   return jsonify({"res":out})



# ----------------------------- WebSSH -----------------------------------
@viewables.route('/webssh')
@login_required
def webssh_view():
   print("SERVER STARTING")
   run_web_ssh_TORNADO()
   print("SERVER STARTED")
   return render_template('webssh/webssh_view.html')

@viewables.route('/cfgcli')
@login_required
def cfgcli():
   print("SERVER STARTING")
   run_web_ssh_TORNADO()
   print("SERVER STARTED")
   return render_template('webssh/cfgcli.html')

@viewables.route('/cfgcli_commands/<load_url>')
@login_required
def cfgcli_commands(load_url):
   load_url = base64.b64decode(load_url.encode())
   data = getCFGI_COMMANDS(load_url)
   return jsonify({"response":data})

@viewables.route('/cfgcli_execute/<command>/')
@login_required
def cfgcli_execute(command):
   run_web_ssh_TORNADO()
   return render_template("webssh/cfgcli_execute.html",command=command)





# ------------------------------------------------------DHCP---------------------------------------------------------------------------------------

# ON
@viewables.route('/dhcp/host')
@login_required
def dhcp_host():
   return render_template('viewables/host/dhcp_host.html')

# @viewables.route('/libvirt/vm_svt_step2',methods=['POST'])
# def libvirt_step2_api():
#    modified_mac = "52-54-00-21-7b-dc"
#    hostname = "raihan"
#    ip_address = "192.168.122.148"
#    path = "/home/raihan/Downloads"
#    capacity = "1"
#    return jsonify({
#       'res' : 'Success'
#    })

# ON
@viewables.route('/dhcp/host/create',methods=['POST'])
@login_required
def create_host():
   hostname = request.form.get('hostname')
   ip_address = request.form.get('ip_address')
   mac_address = request.form.get('mac_address')
   lease = request.form.get('lease')

   # DEBUG
   print("-"*5,"COLLECTED","-"*5)
   print("Hostname : " ,hostname)
   print("IP Address : ",ip_address)
   print("Mac : ",mac_address)
   print("Lease : ",lease)
   print("-"*5,"END","-"*5)
   #DEBUGEND
   res = modifyConfFiles(hostname,ip_address,mac_address,lease)
   if res['res'] == "Error":
      return render_template('response/response_basic.html',err_body=res['reason'])
   addDnsmasq = Dnsmasq(
      user_id=current_user.id,
      ip_address=ip_address,
      mac=mac_address
   )
   db.session.add(addDnsmasq)
   db.session.commit()
   return redirect(url_for('sample.response_succ_view',succ_body="HOST CREATED"))

# -------------------------- DNSMASQ-Helper-PY --------------------
def modifyConfFiles(hostname,ip_address,mac_address,lease):
   # /etc/dnsmasq.conf
   if not os.path.exists('/etc/dnsmasq.conf'):
      return {
         "res":"Error",
         "reason" : "/etc/dnsmasq.conf doesn't exist. Use this command: 'sudo touch /etc/dnsmasq.conf && sudo chmod 667 /etc/dnsmasq.conf'"
      }
   if not os.access('/etc/dnsmasq.conf',os.R_OK|os.W_OK):
      return {
         "res":"Error",
         "reason" : "/etc/dnsmasq.conf doesn't have read/write access. use this command: sudo chmod 666 /etc/dnsmasq.conf"
      }

   command = "dhcp-host={},{},{},{}".format(mac_address,ip_address,hostname,lease)
   conf = open("/etc/dnsmasq.conf").readlines()

   for i,line in enumerate(conf):
      if command in (line):
         return {
               "res" : "Error",
               "reason" : "This dhcp-host already exist in {} no line of /etc/dhcp-host.config. Please Check".format(i+1)
         }
   modified_mac = mac_address.replace(":", "-")
   
   # tftpboot
   if not os.path.isdir('/var/lib/tftpboot/'):
      return{
         "res" : "Error",
         "reason" : "/var/lib/tftpboot/ directory doesent exist.<br/>Please Check and use this command :<br/> sudo mkdir /var/lib/tftpboot/ && sudo chmod 667 /var/lib/tftpboot/"
      }

   elif os.path.isdir('/var/lib/tftpboot/pxelinux.cfg/{}'.format(modified_mac)):
      return {
         "res" : "Error",
         "reason" : "This mac address already exist in /var/lib/tftpboot/pxelinux.cfg/. Please Check"
      }

   if not os.path.isdir('/var/lib/tftpboot/pxelinux.cfg'):
      os.mkdir('/var/lib/tftpboot/pxelinux.cfg')

   if not os.access('/var/lib/tftpboot/pxelinux.cfg/',os.R_OK|os.W_OK|os.F_OK|os.X_OK):
      st = os.stat("/var/lib/tftpboot/pxelinux.cfg/")
      oct_perm = str(oct(st.st_mode))[::-1][:3][::-1]
      return {
         "res":"Error",
         "reason" : "/var/lib/tftpboot/pxelinux.cfg/ directory doesn't have read/write access.Because you are using chmod {}.<br/>Use this command:<br/> sudo chmod 667 /var/lib/tftpboot/pxelinux.cfg/".format(oct_perm)
      }
   os.system('mkdir /var/lib/tftpboot/pxelinux.cfg/{}'.format(modified_mac))
   os.system("echo {}>> /etc/dnsmasq.conf".format(command))

   return {
      "res" : "Success",
   }

# -------------------------------------USER ADMIN----------------------------
@viewables.route('/dtouser')
@login_required
def demoToUser():
   user = User.query.filter_by(id=current_user.id).first()
   user.userInfo = "USER"
   db.session.commit()
   return redirect(url_for('viewables.mechines_user'))

@viewables.route('/dtoAdmin')
@login_required
def demoToAdmin():
   user = User.query.filter_by(id=current_user.id).first()
   user.userInfo = "ADMIN"
   db.session.commit()
   return redirect(url_for('viewables.hypervisors'))

# ---------------------- Timeout------------------
# class host:
#    ip = self.ip
#    def host(ip):
#       ip = self.ip
# def timeout_handler(self,sig_code,frame):
#    if 14 == sig_code:
#       sig_code = 'SIGALRM'
#    print(time.strftime("%F %T -"),"signal Handle called",sig_code)
#    raise Exception('Timeout')

# def libvirtConnection(self):
#    try:
#       signal.signal(signal.SIGALRM,self.timeout_handler)
#       signal.alarm(1)
#       self._virt_conn = libvirt.open("qemu+ssh://root@{}/system".format(hypervisor.hostname))
#       signal.alarm(0)
#    except Exception as e:
#       signal.alarm(0)

# ---------------------- Hypervisors -------------------------

@viewables.route('/Hypervisors/')
@login_required
def hypervisors():
   hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
   hyLen = sum([1 for _ in hypervisors])
   totalMem = 0
   hypervisorsList = []
   totalStorage = 0
   for hypervisor in hypervisors: 
      hypervisorsDict = {}
      hypervisorsDict['hostname'] = hypervisor.hostname
      hypervisorsDict['mechines'] = hypervisor.mechines 
      try:
         conn = libvirtHypervisorConnect(hypervisor.hostname)
         buf = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
         totalMem += int(buf['total']/1000000)

         pools = conn.listAllStoragePools(0)
         storage = []
         for pool in pools:
            info = pool.info()
            if (info[1]/(10**9)) not in storage:
               storage.append(info[1]/(10**9))
         totalStorage += int(sum(storage))

         hypervisorsDict['status'] = "Connected"
      except:
         hypervisorsDict['status'] = "Disconnected"
      hypervisorsList.append(hypervisorsDict)
   
   return render_template("viewables/hypervisors/hypervisors.html",hypervisors=hypervisorsList,hyLen=hyLen,totalMem=totalMem,totalStorage=totalStorage)

@viewables.route('/createAHypervisors/')
@login_required
def createAhypervisors():
   return render_template("viewables/hypervisors/createAHypervisor.html")

@viewables.route('/api/createAHypervisors/',methods=['POST'])
@login_required
def apiCreateAhypervisors():
   hostname = request.form.get('hostname')
   password = request.form.get('password')

   passwd=password.encode()

   res = sendKeyAndConnect(hostname,passwd)
   if res['res'] == "Success":
      # try:
      #    createTftpFolders(hostname)
      # except:
      #    print("NEW CREATE TFTP FOLDER")
      #    return redirect(url_for('sample.response_basic_view',err_body="Hypervisor Connected Succesfully But failed to create tftp boot folders")) 

      isExist = Hypervisor.query.filter_by(user_id=current_user.id,hostname=hostname).first()
      if isExist:
         return redirect(url_for('sample.response_succ_view',succ_body="Hypervisor Connected"))
      else:
         addHypervisor = Hypervisor(
         user_id=current_user.id,
         
         hostname=hostname,
         )
         db.session.add(addHypervisor)
         db.session.commit()
         return redirect(url_for('sample.response_succ_view',succ_body="Hypervisor Connected"))
   elif res['res'] == "Exist":
      # try:
      #    print("Exist CREATE TFTP FOLDER")
      #    createTftpFolders(hostname)
      # except:
      #    return redirect(url_for('sample.response_basic_view',err_body="Hypervisor Connected Succesfully But failed to create tftp boot folders")) 

      isExist = Hypervisor.query.filter_by(user_id=current_user.id,hostname=hostname).first()
      if isExist:
         return redirect(url_for('sample.response_succ_view',succ_body=res['reason']))
      else:
         addHypervisor = Hypervisor(
            user_id=current_user.id,
            hostname=hostname,
         )
         db.session.add(addHypervisor)
         db.session.commit()
         return redirect(url_for('sample.response_succ_view',succ_body="Hypervisor Connected"))
   else:
      return redirect(url_for('sample.response_basic_view',err_body=res['reason']))


# ----------------------- Hypervisor Helper
def sendKeyAndConnect(hostname,password):
   child = pexpect.spawn( 'ssh-copy-id {}@{}'.format("root",hostname),timeout=2 )
   try:
      # index = child.expect(['continue connecting \(yes/no\)','\'s password:',pexpect.EOF],timeout=3)
      index = child.expect(['.*Are you sure you want to continue connecting.*','.*ssword.*:'])
      print(index)
      if index == 0:
         child.sendline('yes')
         time.sleep(2)
         child.close()
         
         child = pexpect.spawn( 'ssh-copy-id {}@{}'.format("root",hostname),timeout=3 )
         child.expect('.*ssword.*:')
         child.sendline(password)
      if index == 1:
         child.sendline(password)
         child.expect('password:')

   except pexpect.ExceptionPexpect as e:
      if "Network is unreachable" in str(e):
         return {
               "res" : "Error",
               "reason" : "Network is unreachable"
         }
      if "No route to host" in str(e):
         return{
               "res" : "Error",
               "reason" : "No route to host.Connection Problem"
         }
      elif "Could not resolve hostname" in str(e):
         return {
               "res" : "Error",
               "reason" : "Could not resolve hostname",
         }
      elif "pexpect.exceptions.TIMEOUT" in str(e):
         # print(str(e))
         return {
               "res" : "Error",
               "reason" : "Failed To Connect",
         }
      else:
         return {
               "res" : "Success",
               "reason" : "Hypervisor Connected",
         }

   print("2nD")
   try:
      time.sleep(3)
      child.expect(pexpect.EOF, timeout=2)
      return {
         "res" : "Success",
         "reason" : "Hypervisor Connected",
      }
   except pexpect.ExceptionPexpect as e:
      if "Timeout exceeded." in str(e):
         return {
         "res" : "Error",
         "reason" : "Password Failed or Permission denied. Also Please Check Connection"
         }
      return {
         "res" : "Error",
         "reason" : "Password Failed or Connection Error. Please Check"
      }

def OLD2sendKeyAndConnect(hostname,password):
   if hostname == "":
      return {
         "res" : "Error",
         "reason" : "Empty hostname"
      }
   child = pexpect.spawn('ssh-copy-id {}@{}'.format("root",hostname),timeout=2)
   print('ssh-copy-id {}@{}'.format("root",hostname))
   try:
      # index = child.expect(['continue connecting \(yes/no\)','\'s password:',pexpect.EOF],timeout=20)
      index = child.expect(['.*Are you sure you want to continue connecting.*','.*ssword.*',pexpect.EOF],timeout=2)
      print(index)
      print(password)
      if index == 0:
         child.sendline('yes')
         child.close()
         child = pexpect.spawn('ssh-copy-id {}@{}'.format("root",hostname),timeout=4)
         child.expect('password:')
         child.sendline(password)
         child.close()
         print(child.after,child.before)
      if index == 1:
         child.sendline(password)
         child.expect('password:')
         # print(password)
         child.sendline(password)
         print (child.after,child.before)
      # if index == 2:
      #    print('[ failed ]')
      #    print(child.after,child.before)
         # child.close()
   except pexpect.ExceptionPexpect as e:
      if "No route to host" in str(e):
         return{
            "res" : "Error",
            "reason" : "No route to host.Connection Problem"
         }
      elif "Could not resolve hostname" in str(e):
         return {
            "res" : "Error",
            "reason" : "Could not resolve hostname",
         }
      elif "pexpect.exceptions.TIMEOUT" in str(e):
         print(str(e))
         return {
            "res" : "Error",
            "reason" : "Failed To Connect",
         }
      else:
         return {
            "res" : "Success",
            "reason" : "Hypervisor Connected",
         }
   try:
      cmd_show_data = child.expect(pexpect.EOF, timeout=4)
      return {
         "res" : "Success",
         "reason" : "Hypervisor Connected",
      }
   except pexpect.ExceptionPexpect as e:
      if "Timeout exceeded." in str(e):
         return {
            "res" : "Error",
            "reason" : "Password Failed or Permission denied. Also Please Check Connection"
         }
      return {
         "res" : "Error",
         "reason" : "Password Failed or Connection Error. Please Check"
      }


def OLDsendKeyAndConnect(hostname,password):
   if hostname == "":
      return {
         "res" : "Error",
         "reason" : "Empty hostname"
      }
   child = pexpect.spawn('ssh-copy-id {}@{}'.format("root",hostname),timeout=4)
   print('ssh-copy-id {}@{}'.format("root",hostname))
   try:
      child.expect('.*ssword.*:')
      child.sendline(password)
   except pexpect.ExceptionPexpect as e:
      if "No route to host" in str(e):
         return{
            "res" : "Error",
            "reason" : "No route to host.Connection Problem"
         }
      elif "Could not resolve hostname" in str(e):
         return {
            "res" : "Error",
            "reason" : "Could not resolve hostname",
         }
      elif "pexpect.exceptions.TIMEOUT" in str(e):
         print(str(e))
         return {
            "res" : "Error",
            "reason" : "Failed To Connect",
         }
      else:
         return {
            "res" : "Success",
            "reason" : "Hypervisor Connected",
         }
   try:
      cmd_show_data = child.expect(pexpect.EOF, timeout=2)
      return {
         "res" : "Success",
         "reason" : "Hypervisor Connected",
      }
   except pexpect.ExceptionPexpect as e:
      if "Timeout exceeded." in str(e):
         return {
            "res" : "Error",
            "reason" : "Password Failed or Permission denied. Also Please Check Connection"
         }
      return {
         "res" : "Error",
         "reason" : "Password Failed or Connection Error. Please Check"
      }

def createTftpFolders(hostname):
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(hostname, 22, "root")
   sftp = ssh.open_sftp()
   sftp.mkdir("/var/lib/tftpboot/")
   sftp.mkdir("/var/lib/tftpboot/bios",mode=755)
   sftp.mkdir("/var/lib/tftpboot/efi32",mode=755)
   sftp.mkdir("/var/lib/tftpboot/efi64",mode=755)
   sftp.mkdir("/var/lib/tftpboot/images",mode=755)
   sftp.mkdir("/var/lib/tftpboot/pxelinux.cfg",mode=755) 
   sftp.close
   ssh.close
# ---------------------- mechines WORKING-------------------------
@viewables.route('/mechines_admin/')
@login_required
def mechines_admin():
   machineOBJ = Mechine.query.filter_by(user_id=current_user.id)
   machines =[]
   for machine in machineOBJ:
      hypervisor = Hypervisor.query.filter_by(id=machine.hypervisor).first()

      ip_address = hypervisor.hostname

      try:
         conn = libvirtHypervisorConnect(ip_address)
         # conn = libvirt.open("qemu+ssh://root@{}/system".format(ip_address))
         dom = conn.lookupByUUIDString(machine.uuidString)
         state = dom.state()[0]

         obj = {
            "vmName" : machine.vmName,
            "hypervisor" : hypervisor.hostname,
         }
         if state == libvirt.VIR_DOMAIN_NOSTATE:
            obj['state'] = "No State"
            print('The state is VIR_DOMAIN_NOSTATE')
         elif state == libvirt.VIR_DOMAIN_RUNNING:
            obj['state'] = "Running"
            print('The state is VIR_DOMAIN_RUNNING')
         elif state == libvirt.VIR_DOMAIN_BLOCKED:
            obj['state'] = "Blocked"
            print('The state is VIR_DOMAIN_BLOCKED')
         elif state == libvirt.VIR_DOMAIN_PAUSED:
            obj['state'] = "Paused"
            print('The state is VIR_DOMAIN_PAUSED')
         elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            obj['state'] = "Shutdown"
            print('The state is VIR_DOMAIN_SHUTDOWN')
         elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            obj['state'] = "Stopped"
            print('The state is VIR_DOMAIN_SHUTOFF')
         elif state == libvirt.VIR_DOMAIN_CRASHED:
            obj['state'] = "Vm Crashed"
            print('The state is VIR_DOMAIN_CRASHED')
         elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            print('The state is VIR_DOMAIN_PMSUSPENDED')
         else:
            obj['state'] = "Unknown"
      except:
         obj = {
            "vmName" : machine.vmName,
            "hypervisor" : hypervisor.hostname,
            "state" : "Down",
         }
      
      machines.append(obj)
   return render_template("viewables/mechines/mechines_admin.html",machines=machines)

@viewables.route('/mechines_user/')
@login_required
def mechines_user():
   machineOBJ = Mechine.query.filter_by(user_id=current_user.id)
   machines =[]
   storage = 0
   mem = 0
   
   for machine in machineOBJ:
      hypervisor = Hypervisor.query.filter_by(id=machine.hypervisor).first()
      storage += machine.storage
      mem += machine.memory

      ip_address = hypervisor.hostname
      
      try:
         conn = libvirtHypervisorConnect(ip_address)
         dom = conn.lookupByUUIDString(machine.uuidString)
         # mem += int(dom.maxMemory()/1000)
         obj = {
            "vmName" : machine.vmName,
            "hypervisor" : hypervisor.hostname,
            "uuidString" : machine.uuidString,
         }
         state = dom.state()[0]
         if state == libvirt.VIR_DOMAIN_NOSTATE:
            obj['state'] = "No State"
            print('The state is VIR_DOMAIN_NOSTATE')
         elif state == libvirt.VIR_DOMAIN_RUNNING:
            obj['state'] = "Running"
            print('The state is VIR_DOMAIN_RUNNING')
         elif state == libvirt.VIR_DOMAIN_BLOCKED:
            obj['state'] = "Blocked"
            print('The state is VIR_DOMAIN_BLOCKED')
         elif state == libvirt.VIR_DOMAIN_PAUSED:
            obj['state'] = "Paused"
            print('The state is VIR_DOMAIN_PAUSED')
         elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            obj['state'] = "Shutdown"
            print('The state is VIR_DOMAIN_SHUTDOWN')
         elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            obj['state'] = "Stopped"
            print('The state is VIR_DOMAIN_SHUTOFF')
         elif state == libvirt.VIR_DOMAIN_CRASHED:
            obj['state'] = "Vm Crashed"
            print('The state is VIR_DOMAIN_CRASHED')
         elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            print('The state is VIR_DOMAIN_PMSUSPENDED')
         else:
            obj['state'] = "Unknown"
      except:
         obj = {
            "vmName" : machine.vmName,
            "hypervisor" : hypervisor.hostname,
            "uuidString" : machine.uuidString,
            "state" : "Down"
         }
      machines.append(obj)
   mlen = len(machines)
   return render_template("viewables/mechines/mechines_user.html",machines=machines,mlen=mlen,storage=storage,mem=mem)

@viewables.route('/mechines_user/createAMechine/')
@login_required
def createAMechine():
   hypervisors =[n.hostname for n in current_user.hypervisor]
   return render_template("viewables/mechines/createAMechine.html",hypervisors=hypervisors)

@viewables.route('/api/createAVM/',methods=['POST'])
@login_required
def apiCreateAVM():
   vmname = request.form.get('machine_name')
   path = request.form.get('path')
   volumeName = request.form.get('vname')
   storageType = request.form.get('storage_type')
   hostname = request.form.get('hypervisor')
   storage = request.form.get('storage')
   memory = request.form.get('memory')
   cpu = request.form.get('cpu')
   threads = request.form.get('threads')
   # ifaceName = request.form.get('interface')
   emulator = request.form.get('emulator')

   # dnsmasq_ip = request.form.get('dnsmasq_ip')
   # dnsmasq_mac = request.form.get('dnsmasq_mac')

   network = request.form.get('network')
   hostnames =[n.hostname for n in current_user.hypervisor]
   if hostname in hostnames:
      hypervisor = Hypervisor.query.filter_by(hostname=hostname).first()

      try: #less 
         conn = libvirtHypervisorConnect(hypervisor.hostname)
      except:
         return{
            "res" : "Error"
         }

      # conn = libvirt.open("qemu+ssh://{}@{}/system".format("root",hypervisor.hostname))
      arch,machine = getEssentialDataForCreatingVM(conn)

      # COMMING SOON
      # dnsmasq = Dnsmasq.query.filter_by(user_id=current_user.id).first()
      # dnsmasq_ip,dnsmasq_mac = dnsmasq.ip_address,dnsmasq.mac

      info = createVMFINAL(conn,path,volumeName,storage,storageType,vmname,memory,cpu,threads,arch,machine,emulator,network)
      # print(dir(info['info']))
      try:
         uuidString = info['info'].UUIDString()
      except:
         return render_template('response/response_basic.html',err_body="VirtualMachine Creation Failed")
      saveMechine =  Mechine(
         hypervisor=hypervisor.id,
         user_id=current_user.id,
         uuidString=uuidString,
         vmName=vmname,
         storage=storage,
         memory=memory
      )
      db.session.add(saveMechine)
      db.session.commit()
      return redirect(url_for('sample.response_succ_view',succ_body="Virtual Machine has been created successfully"))
   else:
      return jsonify({
         "res" : "Error"
      })

@viewables.route('/machine/dashboard/<uuidString>')
@login_required
def machinePower(uuidString):
   isExist = Mechine.query.filter_by(uuidString=uuidString,user_id=current_user.id).first()
   if isExist:
      
      that_hypervisor = Hypervisor.query.filter_by(id=isExist.hypervisor).first()
      
      try:
         conn = libvirtHypervisorConnect(that_hypervisor.hostname)
         # conn = libvirt.open("qemu+ssh://root@{}/system".format(that_hypervisor.hostname))
      except:
         return render_template('response/response_basic.html',err_body="Somethings Wrong!Failed to connect Hypervisor.")
      
      try:
         machine = {}
         dom = conn.lookupByUUIDString(isExist.uuidString)
         machine['name'] = isExist.vmName
         state = dom.state()[0]
         if state == libvirt.VIR_DOMAIN_NOSTATE:
            machine['state'] = "No State"
            print('The state is VIR_DOMAIN_NOSTATE')
         elif state == libvirt.VIR_DOMAIN_RUNNING:
            machine['state'] = "Running"
            print('The state is VIR_DOMAIN_RUNNING')
         elif state == libvirt.VIR_DOMAIN_BLOCKED:
            machine['state'] = "Blocked"
            print('The state is VIR_DOMAIN_BLOCKED')
         elif state == libvirt.VIR_DOMAIN_PAUSED:
            machine['state'] = "Paused"
            print('The state is VIR_DOMAIN_PAUSED')
         elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            machine['state'] = "Shutdown"
            print('The state is VIR_DOMAIN_SHUTDOWN')
         elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            machine['state'] = "Stopped"
            print('The state is VIR_DOMAIN_SHUTOFF')
         elif state == libvirt.VIR_DOMAIN_CRASHED:
            machine['state'] = "Vm Crashed"
            print('The state is VIR_DOMAIN_CRASHED')
         elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            print('The state is VIR_DOMAIN_PMSUSPENDED')
         else:
            machine['state'] = "Unknown"
            print(' The state is unknown.')
         
         state, maxmem, mem, cpus, cput = dom.info()
         machine['mem'] = int(mem/1000)
         machine['cpus'] = cpus
         machine['storage'] = isExist.storage
         
      except:
         return render_template('response/response_basic.html',err_body="Somethings Wrong!")
      
      return render_template("viewables/mechines/dashboard/power.html",machine=machine,uuidString=uuidString)
   else:
      return render_template('response/response_basic.html',err_body="Somethings Wrong!")

@viewables.route('/machine/changestate/<uuidString>',methods=['POST'])
@login_required
def machinePowerStateChange(uuidString):
   isExist = Mechine.query.filter_by(uuidString=uuidString,user_id=current_user.id).first()
   if isExist:
      print(isExist.hypervisor)
      that_hypervisor = Hypervisor.query.filter_by(id=isExist.hypervisor).first()
      try:
         conn = libvirtHypervisorConnect(that_hypervisor.hostname)
         # conn = libvirt.open("qemu+ssh://root@{}/system".format(that_hypervisor.hostname))
      except:
         return render_template('response/response_basic.html',err_body="Somethings Wrong!Failed to connect Hypervisor.")
   
   dom = conn.lookupByUUIDString(uuidString)

   changeState = request.form.get('changeState')
   if changeState == "start":
      dom.create()
   elif changeState == "pause":
      dom.suspend()
   elif changeState == "resume":
      dom.resume()
   elif changeState == "stop":
      dom.destroy()
   elif changeState == "restart":
      dom.reset()
   return redirect(url_for('viewables.machinePower',uuidString=uuidString))
   
# ----------------- mach-helper
@viewables.route('/api/hypervisorInfoStep1/',methods=['POST'])
@login_required
def hyperVinfoS1():
   try:
      data = request.data
      jsonData = json.loads(data)
      try:
         hostname = jsonData['hypervisor']
      except:
         return {"res":"Error","reason":"Something wrong happend (Hypervisor)"}
      hostnames =[n.hostname for n in current_user.hypervisor]
      if hostname in hostnames:
         try:
            hypervisor = Hypervisor.query.filter_by(hostname=hostname).first()
         except:
            return{"res":"Error","reason":"Something wrong happend (Hypervisor)"}
         conn = libvirtHypervisorConnect(hypervisor.hostname)

         networkList = conn.listNetworks()
         networks = []
         for network in networkList:
            networks.append(network)

         nodeinfo = conn.getInfo()

         memory = nodeinfo[1]
         cpu = [n for n in range(1,nodeinfo[2]+1)]
         threads = [n for n in range(1,nodeinfo[7]+1)]
         model = nodeinfo[0]

         emulators,interfaces = fendVMessentials(conn)

         return {
            "res" : "Success",
            "memory" : memory,
            "cpu" : cpu,
            "threads" : threads,
            "model" : model,
            "emulators" : emulators,
            "interfaces" : interfaces,
            "networks" : networks
         }
      else:
         return {
            "res" : "Error",
         }
   except libvirt.libvirtError as e:
      return {
         "res" : "Error",
         "reason" : str(e)
      }
   
# OLD
@viewables.route('/api/hypervisorInfo/',methods=['POST'])
@login_required
def hyperVinfo():
   try:
      data = request.data
      jsonData = json.loads(data)
      hostname = jsonData['hypervisor']
      path = jsonData['path']
      hostnames =[n.hostname for n in current_user.hypervisor]
      if hostname in hostnames:
         hypervisor = Hypervisor.query.filter_by(hostname=hostname).first()
         conn = libvirtHypervisorConnect(hypervisor.hostname)
         # conn = libvirt.open("qemu+ssh://{}@{}/system".format("root",hypervisor.hostname))
         # conn = libvirt.open("qemu:///system")
         pools = conn.listAllStoragePools()
         # try:
         main_pool = findPool(conn,pools,path)
         try:
            if main_pool['reason']:
               return {
                  "res" : "Error",
                  "reason" : main_pool['reason']
               }
         except:
            pass
         info = main_pool.info()
         available = info[3]*0.000000001
         nodeinfo = conn.getInfo()

         memory = nodeinfo[1]
         cpu = [n for n in range(1,nodeinfo[2]+1)]
         threads = [n for n in range(1,nodeinfo[7]+1)]
         model = nodeinfo[0]

         emulators,interfaces = fendVMessentials(conn)

         return {
            "res" : "Success",
            "memory" : memory,
            "cpu" : cpu,
            "threads" : threads,
            "model" : model,
            "available" : available,
            "emulators" : emulators,
            "interfaces" : interfaces
         }
      else:
         return {
            "res" : "Error",
         }
   except libvirt.libvirtError as e:
      return {
         "res" : "Error",
         "reason" : str(e)
      }

def fendVMessentials(conn):
   # EMULATOR
   emulators = []
   caps = conn.getCapabilities() 
   root = ET.fromstring(caps)
   for elem in root.iter():
      if (elem.tag == "emulator"):
         emulators.append(elem.text)
   
   #Interface
   interfaces = []
   interfaceName = conn.listAllInterfaces()
   for iname in interfaceName:
      interfaces.append(iname.name())

   return emulators,interfaces

def getEssentialDataForCreatingVM(conn):
   # ARCH
   arch = None
   machine = None
   caps = conn.getCapabilities()
   root = ET.fromstring(caps)
   for elem in root.iter():
    if elem.tag == "arch" and elem.text:
        txt = elem.text.replace(" ","").replace("\n","")
        if txt:
            arch=txt
   for elem in root.iter():
    try:
        if elem.attrib['canonical']:
            machine=elem.attrib['canonical']
            break
    except:
        pass
   return arch,machine
   

#-------------------------MACHINE CREATE HELPER-----------------------
def createStoragePool(conn,path):      
   xmlDesc = """
      <pool type='dir'>
         <name>{}</name>
         <uuid>{}</uuid>
         <source>
         </source>
         <target>
               <path>{}</path>
               <permissions>
               <mode>0711</mode>
               <owner>0</owner>
               <group>0</group>
               </permissions>
         </target>
      </pool>
   """.format(
         ''.join(random.sample(string.ascii_uppercase, 6)),
         str(uuid.uuid4()),
         path
      )
   pool = conn.storagePoolDefineXML(xmlDesc, 0)
   # Activate and Autostart
   pool.create()
   pool.setAutostart(True)
   return pool

def createVol(main_pool,volumeName,capacity,fmt):
   stgvol_xml = """
   <volume>
   <name>{}</name>
   <allocation>0</allocation>
   <capacity unit="G">{}</capacity>
   <target>
      <format type="{}" />
      <path>/var/lib/libvirt/images/{}.{}</path>
      <permissions>
      <owner>107</owner>
      <group>107</group>
      <mode>0744</mode>
      <label>virt_image_t</label>
      </permissions>
   </target>
   </volume>""".format(
         volumeName,
         capacity,
         fmt,
         volumeName,
         fmt
      )
   main_pool.createXML(stgvol_xml, 0)

def findPool(conn,pools,path): 
   main_pool = None
   for pool in pools:
      # ACTIVATE POOL
      try:
         if not pool.isActive():
            pool.create()
         # Get pool
         root = ET.fromstring(pool.XMLDesc())
         for elem in root.iter():
               if(elem.text == path):
                  print("exist",path)
                  main_pool = pool
                  return main_pool
      except:
         pass
   # # Create Pool if not exist
   if main_pool == None:
      try:
         main_pool = createStoragePool(conn,path)
         return main_pool
      except libvirt.libvirtError as e:
         return {
            "reason" : str(e)
         }

def createVMFINAL(
      conn,path,volumeName,storage,storageType,vmname,memory,cpu,threads,arch,machine,emulator,network
   ):
   # vmname,memory,cpu,threads,arch,machine,emulator,path,volumeName,storageType,ifaceName,storage
   pools = conn.listAllStoragePools()
   main_pool = findPool(conn,pools,path)
   try:
      createVol(main_pool,volumeName,storage,storageType)
   except libvirt.libvirtError as err:
      pass
   try:
      xml = createVMengxml(vmname,memory,cpu,threads,arch,machine,emulator,path,volumeName,storageType,network)
      dom = conn.defineXMLFlags(xml,0)

      if dom.create() < 0:
         return{
            "res" : "Error",
            "reason" : "Failed to boot guest domain"
         }
   except libvirt.libvirtError as err:
      return{
         "res" : "Error",
         "reason" :  str(err)
      }
   return {
      "res" : "Success",
      "info" : dom
   }

def createVMengxml(vmname,memory,cpu,threads,arch,machine,emulator,path,volumeName,storageType,network):
   xml=f'''
   <domain type='kvm'>
      ​<name>{vmname}</name>
      ​<memory unit="M">{memory}</memory>
      ​<vcpu>{cpu}</vcpu>
      <iothreads>{threads}</iothreads>
      ​<os>
         <type >hvm</type>
         <boot dev='network'/>
      </os>
      <devices>
         <disk type='file' device='disk'>
            <source file='{path}/{volumeName}'/>
            <driver type='{storageType}'/>
            <target dev='hda'/>
         </disk>
         <interface type="network">
            <source network="{network}"/>
         </interface>
         <graphics type='vnc'/>
      </devices>
   </domain>
   '''

   return xml

# <mac address='{dnsmasq_mac}'/>
# <ip address='{dnsmasq_ip}' netmask='255.255.255.0'>
#    <tftp root='/srv/tftp'/>
#    <dhcp>
#       <range start='192.168.122.2' end='192.168.122.254'/>
#       <bootp file='pxelinux.0'/>
#    </dhcp>
# </ip>


# -------------------DASHBOARDS - HYPERVISOR ------------
@viewables.route('/hypervisor/dashboard/<hypervisor>')
@login_required
def hypervisorDashboard(hypervisor):
   isExist = Hypervisor.query.filter_by(hostname=hypervisor,user_id=current_user.id).first()
   if isExist:
      return render_template("viewables/hypervisors/dashboard/dashboard.html",hypervisor=isExist)
   else:
      return render_template('response/response_basic.html',err_body="Somethings Wrong!")

@viewables.route('/hypervisor/chartAPI/<hypervisor>',methods=['POST'])
@login_required
def hypervisorDChart(hypervisor):
   isExist = Hypervisor.query.filter_by(hostname=hypervisor,user_id=current_user.id).first()
   if isExist:
      res = updateChart(hypervisor)
      if res['res'] == "Success":
         return res
      else:
         return {
            "res" : "Error"
         }
   else:
      return {
         "res" : "Error"
      }



@viewables.route('/ip-pools')
@login_required
def ipPools():
   hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
   return render_template("viewables/ipPools/ipPools.html")

@viewables.route('/create-ip-pools',methods=["POST","GET"])
@login_required
def createIpPoolApi():
   if request.method == "POST":
      hostname = request.form.get('hypervisor')
      networkName = request.form.get('networkName')
      ip = request.form.get('ip')
      netmask = request.form.get('netmask')
      start = request.form.get('start')
      end = request.form.get('end')
      print(hostname)
      hypervisor = Hypervisor.query.filter_by(hostname=hostname,user_id=current_user.id).first()
      if not hypervisor:
         return render_template('response/response_basic.html',err_body="Something Wrong Happened")
      res = createNetwork(hostname,networkName,ip,netmask,start,end)
      print(res)
      if res['res'] == "Success":
         ip_pool = IP_Pools(
            user_id=current_user.id,
            hypervisor=hypervisor.id,
         )
         return redirect(url_for('sample.response_succ_view',succ_body="Virtual Network has been creadted successfully"))
      else:
         return render_template('response/response_basic.html',err_body=res['reason'])
   hypervisors = Hypervisor.query.filter_by(user_id=current_user.id)
   return render_template("viewables/ipPools/createIpPool.html",hypervisors=hypervisors)

def createNetwork(hostname,networkName,ip,netmask,start,end):
   cip,cnetmask,cstart,cend = len(ip.split(".")),len(netmask.split(".")),len(start.split(".")),len(end.split("."))
   if cip != 4: return {"res" : "Error","reason" : "Invalid IP Address"}
   if cnetmask != 4: return {"res" : "Error","reason" : "Invalid Netmask"}
   if cstart != 4: return {"res" : "Error","reason" : "Invalid IP Range "}
   if cend != 4: return {"res" : "Error","reason" : "Invalid IP Range"}
   xml = f'''
      <network>
      <name>{networkName}</name>
      <forward mode="nat">
         <nat>
            <port start="1024" end="65535"/>
         </nat>
      </forward>
      <ip address="{ip}" netmask="{netmask}">
         <tftp root="/var/lib/tftpboot"/>
         <dhcp>
            <range start="{start}" end="{end}"/>
            <bootp file="pxelinux.0"/>
         </dhcp>
      </ip>
      </network>
   '''
   print(hostname,networkName,ip,netmask,start,end)
   
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
