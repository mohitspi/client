import os,sys
sys.path.append(os.path.abspath(os.path.join('..','mainapp')))

from mainapp import db
from mainapp.models import Debian,Windows,User,SshKey,Iperf,CiscoModel
from flask_login import current_user

from subprocess import check_output,CalledProcessError
import subprocess
import io,json,xmltodict
import urllib

# import libvirt
import time
import func_timeout

def getDebianContext():
    query = Debian.query.all()
    locales = [q.locale for q in query if q.locale != None]
    languages = [q.language for q in query if q.language != None]
    countries = [q.country for q in query if q.country != None]
    environments = [q.multi_language_environment for q in query if q.multi_language_environment != None]
    xkbkeymaps = [q.xkbkeymap for q in query if q.xkbkeymap != None]
    language_name_fbs =[q.language_name_fb for q in query if q.language_name_fb != None]
    countrynames = [q.country_name for q in query if q.country_name != None]
    layoutcodes = [q.layoutcode for q in query if q.layoutcode != None]
    interfaces = [q.interface for q in query if q.interface != None]
    methods = [q.method for q in query if q.method != None]
    sizes = [q.guided_size for q in query if q.guided_size != None]
    recipes = [q.recipe for q in query if q.recipe != None]
    filesystems = [q.filesystem for q in query if q.filesystem != None]
    disks = [q.disk for q in query if q.disk != None]
    partition_methods = [q.partition_method for q in query if q.partition_method != None]
    install_additions = [q.install_addition for q in query if q.install_addition != None]
    context={'install_additions':install_additions,'partition_methods':partition_methods,'filesystems':filesystems,'disks':disks,'sizes':sizes,'recipes':recipes,'methods':methods,'interfaces':interfaces,'layoutcodes':layoutcodes,'countrynames':countrynames,'xkbkeymaps':xkbkeymaps,'language_name_fbs':language_name_fbs, 'locales':locales, 
        'languages':languages, 'countries':countries, 'environments':environments}

    return context

def getWindowsContext():
    query = Windows.query.all()
    execution_policies =[q.execution_policy for q in query]
    quick_configs = [q.quick_config for q in query]

    context={'execution_policies':execution_policies,'quick_configs':quick_configs}

    return context

def createSSHKey(user_id,ssh,name):
    createSSH = SshKey(user_id=user_id,ssh=ssh,name=name)
    db.session.add(createSSH)
    db.session.commit()


def createCiscoData(user_id,ip,global_delay_factor,device_type,username,password,secret,verbose):
    createCisco = CiscoModel(user_id=user_id,ip=ip,global_delay_factor=global_delay_factor,device_type = device_type, username = username,password = password,secret = secret,verbose=verbose)
    db.session.add(createCisco)
    db.session.commit()


def getServers():
    out = check_output(["speedtest","--list"],shell=True)
    buf = io.StringIO(out.decode())

    servers = []
    for line in buf.readlines():
        line = line.replace(" ", "")
        lists = line.split(")")
        if len(lists)==3:
            code = lists[0].replace(" ", "")
            name = lists[1]+")"
            distance = lists[2].replace("\r\n", "")
            obj = {
                "code":code,
                "name":name,
                "distance":distance,
            }
            servers.append(obj)
    return servers

def getServersJson():
    # out = check_output(["./bins/windows/speedtest.exe","-L","-p","no","-f","json"]) #if using windows (from bin)
    # out = check_output(["./bins/linux/speedtest","-L","-p","no","-f","json"]) #if using linux (from bin)
    # out = check_output(["./bins/mac/speedtest","-L","-p","no","-f","json"]) #if using mac (from bin)
    out = check_output(["speedtest","-L","-p","no","-f","json"]) #if direct
    out = json.loads(out)
    return out

def getResult(sid):
    # out = check_output(["./bins/windows/speedtest.exe","-s",sid,"-p","no","-f","json"]) #if using windows (from bin)
    # out = check_output(["./bins/linux/speedtest","-s",sid,"-p","no","-f","json"]) #if using linux (from bin)
    # out = check_output(["./bins/mac/speedtest","-s",sid,"-p","no","-f","json"]) #if using mac (from bin)
    out = check_output(["speedtest","-s",sid,"-p","no","-f","json"]) #if direct
    out = json.loads(out)
    return out


HELP = '''
Usage: iperf [-s|-c host] [options]
iperf [-h|--help] [-v|--version]

Server or Client:
  -p, --port      #         server port to listen on/connect to
  -f, --format    [kmgKMG]  format to report: Kbits, Mbits, KBytes, MBytes
  -i, --interval  #         seconds between periodic bandwidth reports
  -F, --file name           xmit/recv the specified file
  -B, --bind      <host>    bind to a specific interface
  -V, --verbose             more detailed output
  -J, --json                output in JSON format
  --logfile f               send output to a log file
  -d, --debug               emit debugging output
  -v, --version             show version information and quit
  -h, --help                show this message and quit
Server specific:
  -s, --server              run in server mode
  -D, --daemon              run the server as a daemon
  -I, --pidfile file        write PID file
  -1, --one-off             handle one client connection then exit
Client specific:
  -c, --client    <host>    run in client mode, connecting to <host>
  -u, --udp                 use UDP rather than TCP
  -b, --bandwidth #[KMG][/#] target bandwidth in bits/sec (0 for unlimited)
                            (default 1 Mbit/sec for UDP, unlimited for TCP)
                            (optional slash and packet count for burst mode)
  -t, --time      #         time in seconds to transmit for (default 10 secs)
  -n, --bytes     #[KMG]    number of bytes to transmit (instead of -t)
  -k, --blockcount #[KMG]   number of blocks (packets) to transmit (instead of -t or -n)
  -l, --len       #[KMG]    length of buffer to read or write
                            (default 128 KB for TCP, 8 KB for UDP)
  --cport         <port>    bind to a specific client port (TCP and UDP, default: ephemeral port)
  -P, --parallel  #         number of parallel client streams to run
  -R, --reverse             run in reverse mode (server sends, client receives)
  -w, --window    #[KMG]    set window size / socket buffer size
  -M, --set-mss   #         set TCP/SCTP maximum segment size (MTU - 40 bytes)
  -N, --no-delay            set TCP/SCTP no delay, disabling Nagle's Algorithm
  -4, --version4            only use IPv4
  -6, --version6            only use IPv6
  -S, --tos N               set the IP 'type of service'
  -Z, --zerocopy            use a 'zero copy' method of sending data
  -O, --omit N              omit the first n seconds
  -T, --title str           prefix every output line with this string
  --get-server-output       get results from server
  --udp-counters-64bit      use 64-bit counters in UDP test packets

[KMG] indicates options that support a K/M/G suffix for kilo-, mega-, or giga-

iperf3 homepage at: http://software.es.net/iperf/
Report bugs to:     https://github.com/esnet/iperf
        '''.encode()

def iperfRes(host,port,para):
    para = para.split(" ")
    para = [x for x in para if x != ""]
    parameter = ["iperf3","-c",host,"-p",port]
    [parameter.append(x) for x in para]
    print(parameter)
    if not host or not port or "-h" in parameter:
        return HELP
    try:
        out = check_output(parameter)
        add_result = Iperf(
            user_id=current_user.id,
            result=out.decode()
        )
        db.session.add(add_result)
        db.session.commit()  
    except:
        out = "iperf Returned Error! Something wrong happed (Server Busy / Wrong Parameter)".encode()
    return out

def run_web_ssh_TORNADO():
    try:
        subprocess.Popen(["python3","Features/main.py"],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except:
        subprocess.Popen(["python","Features/main.py"],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
def getCFGI_COMMANDS(load_url):
    json_data = []
    data_dict = None

    try:
        link = load_url.decode()
        f = urllib.request.urlopen(link)
        myfile = f.read()
        data_dict = xmltodict.parse(myfile)
        try:
            try:
                for obj in data_dict['dm:document']['model']['object']:
                    json_data.append(obj)
                return json_data
            except:
                for obj in data_dict['dm:document']['model']:
                    for ob in obj['object']:
                        json_data.append(ob)
                return json_data
        except :
            for components in data_dict['dm:document']['component']:
                try:
                    for obj in components['object']:
                        if type(obj)!=type('str'):
                            json_data.append(obj)
                except:
                    pass
            return json_data
    except:
        return {
            "ERROR" : "INVALID STRUCTURE OR URL"
        }
    


def dashboard_cpu_memory_storage(hostname):
    conn = libvirt.open("qemu+ssh://{}@{}/system".format("root",hostname))
    # Memory
    memoryStat = []
    nodeinfo = conn.getInfo()

    for i in range(20):
        mem = conn.getFreeMemory()
        memstat =( (nodeinfo[1]-(mem*0.000001)) /nodeinfo[1] )*100
        memstat = float("{:.2f}".format(memstat))
        memoryStat.append(memstat)
        time.sleep(.5)

def updateChart(hostname):
    try:
        
        conn = libvirt.open("qemu+ssh://{}@{}/system".format("root",hostname))
        
        memory = []
        cpuStat = []

        stats = conn.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS)
        calOld = (stats['kernel']/1000000000+stats['user']/1000000000)
        
        for i in range(20):
            
            buf = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
            # statMem = round(
            #         (
            #             ( (buf['total']-buf['free']-buf['cached']-buf['buffers']) / (buf['total']) )*100
            #         ),2
            #     )
            statMem = int((buf['total']-buf['free']-buf['cached'])/1000)
            
            stats = conn.getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS)
            cal2 = ((stats['kernel']/1000000000+stats['user']/1000000000))
            cpuUsage = int((cal2 - calOld)*100)
            memory.append(statMem)
            cpuStat.append(cpuUsage)
            
            # print(statMem,cpuUsage)
            time.sleep(.5)
            calOld = cal2

        buf = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
        totalMem = int(buf['total']/1000)
        print(totalMem)
        return {
            "res" : "Success",
            "mem" : memory,
            "cpu" : cpuStat[1:],
            "totalMem" : totalMem
        }
    except:
        return {
            "res" : "Error"
        }

@func_timeout.func_set_timeout(2)
def libvirtHypervisorConnect(hostname):
    return libvirt.open("qemu+ssh://root@{}/system".format(hostname))