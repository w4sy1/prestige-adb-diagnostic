import re
import subprocess
import sys
from runtime import entry,parser,run

PROPERTIES={'model':'ro.product.model','manufacturer':'ro.product.manufacturer','android':'ro.build.version.release','security_patch':'ro.build.version.security_patch','cpu_abi':'ro.product.cpu.abi'}
COMMANDS={
 'kernel':['uname','-r'],'ram':['cat','/proc/meminfo'],'storage':['df','-k','/data'],
 'battery':['dumpsys','battery'],'uptime':['cat','/proc/uptime'],
 'packages':['pm','list','packages'],'user_apps':['pm','list','packages','-3'],
 'services':['service','list'],'permissions':['pm','list','permissions','-g'],
 'network':['ip','address'],'usb':['getprop','sys.usb.state'],
}

def choose_device(text, selected=None):
    devices={}
    for line in text.splitlines()[1:]:
        fields=line.split()
        if len(fields)>=2:devices[fields[0]]=fields[1]
    if selected:
        if devices.get(selected)!='device':raise ValueError('Urządzenie niedostępne lub bez autoryzacji.')
        return selected
    ready=[key for key,value in devices.items() if value=='device']
    if len(ready)!=1:raise ValueError('Wymagane dokładnie jedno autoryzowane urządzenie lub --device.')
    return ready[0]

def battery(text):
    result={}
    for line in text.splitlines():
        key,sep,value=line.strip().partition(':')
        if sep and key in ('level','scale','status','health','voltage','temperature','AC powered','USB powered'):
            result[key]=value.strip()
    try:result['temperature_c']=int(result['temperature'])/10
    except (KeyError,ValueError):result['temperature_c']=None
    return result

def build():
    p=parser('Odczyt Androida przez ADB. Wymaga odblokowania i autoryzacji urządzenia.')
    p.add_argument('--device',help='Wybór urządzenia z adb devices')
    p.add_argument('--collect',action='store_true',help='Rozpocznij odczyt podłączonego urządzenia')
    p.add_argument('--logcat-count',action='store_true',help='Policz błędy bufora logcat bez zachowywania treści')
    return p

def handle(args):
    if not args.collect:raise ValueError('Wymagane --collect.')
    device=choose_device(run(['adb','devices']),args.device)
    base=['adb','-s',device,'shell']
    results={}
    for name,command in {**{n:['getprop',p] for n,p in PROPERTIES.items()},**COMMANDS}.items():
        try:
            value=run(base+command,30)
            results[name]={'status':'OK' if value.strip() else 'EMPTY','data':battery(value) if name=='battery' else value.strip()}
        except (OSError,RuntimeError,subprocess.SubprocessError) as e:
            results[name]={'status':'UNAVAILABLE','error':type(e).__name__}
    if args.logcat_count:
        try:
            text=run(['adb','-s',device,'logcat','-d','-t','200','-v','brief','*:E'],20)
            results['logcat']={'status':'OK','error_lines':sum(bool(re.match(r'^E[/\s]',line)) for line in text.splitlines()),'messages_stored':False}
        except (OSError,RuntimeError,subprocess.SubprocessError):results['logcat']={'status':'UNAVAILABLE'}
    return {'adb_state':'device','results':results,'ok':not any(v['status']=='UNAVAILABLE' for v in results.values())}

if __name__=='__main__':sys.exit(entry(build,handle))
