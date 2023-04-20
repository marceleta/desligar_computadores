import platform
import subprocess, platform

def ping(host):
    
    parametro = '-n' if platform.system().lower == 'windows' else '-c'
    
    comando = ['ping', parametro, '1', host]
    
    return subprocess.call(comando)


def comando_shutdown(computador):
    
    host_os = platform.system().lower()
    computador_alvo = computador['os'].lower()
    
    comando = None
    
    if host_os == 'linux':
        if computador_alvo == 'linux':
            login = computador['usuario'] + '@' + computador['IP']
            comando = ['sshpass', '-p', computador['senha'], 'ssh', login, 'shutdown -h now; exit']
        else:
            login = computador['usuario'] + '%' + computador['senha']
            comando = ['net', 'rpc', 'shutdown', '-f', '-I', computador['IP'], '-U', login]
    else:
        if computador_alvo == 'windows':
            comando = ['psshutdown', '-s', '-f', '-c', '-u', computador['usuario'], '-p', computador['senha'], '\\'+computador['IP']]
        else:
            host = computador['usuario'] + '@' + computador['IP']
            comando = ['plink', host, '-pw', computador['senha'], '-batch', 'shutdown now']
            
    return comando
            
        
            
    
    
    
    
    
    
