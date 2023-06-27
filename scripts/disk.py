#!/usr/bin/env python

# by n1nr0d


# Script pessoal para a leitura de dados do meu disco nvme + btrfs(e suas opções de montagem)

import psutil

def linha():
    print("-"*40)



def ciano(cian):
    print(f"\033[1;36;40;1m{cian}\033[m")


# Uso do disco
sufixos = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
def fmtlegivel(bytes):
    i = 0
    while bytes >= 1024 and i < len(sufixos):
        bytes /= 1024
        i += 1
    f = ('%.2f' % bytes)
    return '%s %s' % (f, sufixos[i])

# Disco
ciano("\nDisco:")
print(f"Espaço de disco usado: {fmtlegivel(psutil.disk_usage('/').used)}")
print(f"Espaço de disco Total: {fmtlegivel(psutil.disk_usage('/').total)}")
print(f"Espaço de disco disponível: {fmtlegivel(psutil.disk_usage('/').free)}")
linha()

# Swap
ciano("Swap:")
print(f"Swap usado: {fmtlegivel(psutil.swap_memory().used)}")
print(f"Swap Total: {fmtlegivel(psutil.swap_memory().total)}")
print(f"Swap Livre: {fmtlegivel(psutil.swap_memory().free)}")
linha()

# Temperatura:
ciano("Temperatura:")
temp=float(psutil.sensors_temperatures().get('nvme')[0][1])
hightemp=float(psutil.sensors_temperatures().get('nvme')[0][2])
crttemp=float(psutil.sensors_temperatures().get('nvme')[0][3])

if temp < 65:
    # verde, ok!
    print(f"Temperatura atual: \033[1;32;40;1m{temp}C°\033[m")
elif temp >= 65 and temp < hightemp:
    # amarelo, atenção!
    print(f"\033[1;33;40;1m{temp}C°\033[m")
elif temp >= hightemp and temp <= crttemp:
    # vermelho, cuidado!
    print(f"\033[1;31;40;1m{temp}C°\033[m")
    
    
# Limiares:
print(f"Temperatura alta: \033[1;33;40;1m{hightemp}C°\033[m")
print(f"Temperatura máx: \033[1;31;40;1m{crttemp}C°\033[m")
linha()

# Partições de disco:
ciano("Partições montadas:")
for disk in psutil.disk_partitions():
    if disk.fstype:
        print(f"Endereço: {disk.device},\nPonto de montagem: {disk.mountpoint},\nOpções:  {disk.opts}")
print("\n")
