#imports - Django web app functionality
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.urls import reverse_lazy
import paramiko # paramiko to establish ssh connection
from paramiko import SSHClient 
from scp import SCPClient # scp to securely copy files
from django.contrib import messages
# import of models ( classes ) 
from .forms import ConnectionForm
from .models import Connection
from .models import About 

from django.contrib.auth.decorators import login_required
# method to dispay honeypots
def about_index(request):
    abouts = About.objects.all()
    context = {
        'abouts': abouts
    }
    return render(request, 'about_index.html', context)
# method to dispay detailed info about each
def about_detail(request, pk):
    about = About.objects.get(pk=pk)
    context = {
        'about': about
    }
    return render(request, 'about_detail.html', context)
# home method and form for submission of server details
@login_required
def home(request): 
                                
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            form.save()
            home.ip = form.cleaned_data['ip']   
            home.username = form.cleaned_data['username'] 
            home.password = form.cleaned_data['password'] 
            return redirect('deploy_honeypot')      
    else:
        form = ConnectionForm()
    return render(request, 'home.html', {'form': form})
# deployment method

@login_required
def deploy_honeypot(request):
    
    if request.method == 'POST':
        if 'iothoney' in request.POST:           
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(home.ip, port=22, username = home.username, password = home.password)
            
            with SCPClient(ssh.get_transport()) as scp:
                scp.put('/root/Django/http/HTTP-Honeypot.install.sh', 'HTTP-Honeypot.install.sh') 
                scp.put('/root/Django/http/HTTP-Honeypot.uninstall.sh', 'HTTP-Honeypot.uninstall.sh') 
            stdin, stdout, stderr = ssh.exec_command("sudo chmod +x HTTP-Honeypot.install.sh && sudo chmod +x HTTP-Honeypot.uninstall.sh && sudo ./HTTP-Honeypot.install.sh", get_pty = True)
            stdin.write(home.password + "\n")
            stdin.flush()
            output = stdout.read().splitlines()
            ssh.close()
            messages.success(request, f'Honeypot installed successfully!')
            ipaddress = home.ip
            return render(request, 'iot_honeypots.html', {'ipaddress' : ipaddress })


        elif 'honething' in request.POST:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(home.ip, port=22, username = home.username, password = home.password)
            with SCPClient(ssh.get_transport()) as scp:
                scp.put('/root/Django/honeything/honeything.install.sh', 'honeything.install.sh') 
                scp.put('/root/Django/honeything/honeything.uninstall.sh', 'honeything.uninstall.sh') 
            stdin, stdout, stderr = ssh.exec_command("sudo chmod +x honeything.install.sh && sudo chmod +x honeything.uninstall.sh && sudo ./honeything.install.sh", get_pty = True)
            stdin.write(home.password + "\n")
            stdin.flush()
            output = stdout.read().splitlines()
            ssh.close()
            messages.success(request, f'Honeypot installed successfully!')
            ipaddress = home.ip
            return render(request, 'iot_honeypots.html', {'ipaddress' : ipaddress })

        elif 'phype' in request.POST: 
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(home.ip, port=22, username = home.username, password = home.password)
            with SCPClient(ssh.get_transport()) as scp:
                scp.put('/root/Django/phype/telnet-iot-honeypot.install.sh', 'telnet-iot-honeypot.install.sh') 
                scp.put('/root/Django/phype/telnet-iot-honeypot.uninstall.sh', 'telnet-iot-honeypot.uninstall.sh')   
            stdin, stdout, stderr = ssh.exec_command("sudo chmod +x telnet-iot-honeypot.install.sh && sudo chmod +x telnet-iot-honeypot.uninstall.sh && sudo ./telnet-iot-honeypot.install.sh", get_pty = True)
            stdin.write(home.password + "\n")
            stdin.flush()
            output = stdout.read().splitlines()
            ssh.close()
            messages.success(request, f'Honeypot installed successfully!')
            ipaddress = home.ip
            return render(request, 'iot_honeypots.html', {'ipaddress' : ipaddress })

        elif 'kako' in request.POST: 
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(home.ip, port=22, username = home.username, password = home.password)
            with SCPClient(ssh.get_transport()) as scp:
                scp.put('/root/Django/kako/kako.install.sh', 'kako.install.sh') 
                scp.put('/root/Django/kako/kako.uninstall.sh', 'kako.uninstall.sh')
            stdin, stdout, stderr = ssh.exec_command("sudo chmod +x kako.install.sh && sudo chmod +x kako.uninstall.sh && sudo ./kako.install.sh", get_pty = True)
            stdin.write(home.password + "\n")
            stdin.flush()
            output = stdout.read().splitlines()
            ssh.close()
            messages.success(request, f'Honeypot installed successfully!')
            ipaddress = home.ip
            return render(request, 'iot_honeypots.html', {'ipaddress' : ipaddress })



    return render(request, 'deploy_honeypot.html')
# method that handles honeypots deployment display
@login_required
def iot_honeypots(request):
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            form.save()
            home.ip = form.cleaned_data['ip']   
            home.username = form.cleaned_data['username'] 
            home.password = form.cleaned_data['password'] 

            return redirect('deploy_honeypot')      
    else:
        form = ConnectionForm()
    return render(request, 'iot_honeypots.html', {'form': form})

@login_required # decorator for authentication
def get_logs(request): # method that display logs and uninstall honeypots
    
    if request.method=='POST' and 'HoneyThingLogs' in request.POST:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get('/var/log/honeything/http.log', 'C:/Windows/Temp/HoneythingLogs.txt') 
        f = open('C:/Windows/Temp/HoneythingLogs.txt', 'r')
        file_content = f.read()
        f.close()
        return HttpResponse(file_content, content_type='text/plain')

    elif request.method=='POST' and 'PhypeLogs' in request.POST:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get('/root/telnet-iot-honeypot/telnet.txt', 'C:/Windows/Temp/telnet.txt') 
        f = open('C:/Windows/Temp/telnet.txt', 'r')
        file_content = f.read()
        f.close()
        return HttpResponse(file_content, content_type='text/plain')      

    elif request.method=='POST' and 'IotHoneypotLogs' in request.POST:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get('/root/HTTP-Honeypot/Sys/log/Client\ Data', 'C:/Windows/Temp/IotHoneypotLogs.txt') 
        f = open('C:/Windows/Temp/IotHoneypotLogs.txt', 'r')            
        file_content = f.read()
        f.close()
        return HttpResponse(file_content, content_type='text/plain')

    elif request.method=='POST' and 'KakoLogs' in request.POST:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        with SCPClient(ssh.get_transport()) as scp:
            scp.get('/root/honeypot/kako/kako.log', 'C:/Windows/Temp/Kako.txt') 
        f = open('C:/Windows/Temp/Kako.txt', 'r')            
        file_content = f.read()
        f.close()
        return HttpResponse(file_content, content_type='text/plain')    
        
    elif 'uninstallKako' in request.POST: 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        stdin, stdout, stderr = ssh.exec_command("cd kako && sudo kako.uninstall.sh ", get_pty = True)
        stdin.write(home.password + "\n")
        stdin.flush()
        output = stdout.read().splitlines()
        ssh.close()
        messages.success(request, f'Honeypot uninstalled successfully!')
        return render(request, 'iot_honeypots.html')

    elif 'uninstallHoneything' in request.POST: 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        stdin, stdout, stderr = ssh.exec_command(" cd honeything && sudo honeything.uninstall.sh ", get_pty = True)
        stdin.write(home.password + "\n")
        stdin.flush()
        output = stdout.read().splitlines()
        ssh.close()
        messages.success(request, f'Honeypot uninstalled successfully!')
        return render(request, 'iot_honeypots.html')  

    elif 'uninstallTelnet' in request.POST: 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        stdin, stdout, stderr = ssh.exec_command(" cd phype && sudo telnet-iot-honeypot.uninstall.sh ", get_pty = True)
        stdin.write(home.password + "\n")
        stdin.flush()
        output = stdout.read().splitlines()
        ssh.close()
        messages.success(request, f'Honeypot uninstalled successfully!')
        return render(request, 'iot_honeypots.html')  
            
    elif 'uninstallHTTP' in request.POST: 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(home.ip, port=22, username = home.username, password = home.password)
        stdin, stdout, stderr = ssh.exec_command(" cd http && sudo HTTP-Honeypot.uninstall.sh ", get_pty = True)
        stdin.write(home.password + "\n")
        stdin.flush()
        output = stdout.read().splitlines()
        ssh.close()
        messages.success(request, f'Honeypot uninstalled successfully!')
        return render(request, 'iot_honeypots.html')  
    
    return render(request, 'iot_honeypots.html') 
# guide display       
def guide(request):

    return render(request, 'guide.html') 
    
         
      