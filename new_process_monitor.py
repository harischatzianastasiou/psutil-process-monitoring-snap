import psutil
from collections import OrderedDict
from datetime import datetime
import pandas as pd
import time
import os
from collections import Counter
from time import sleep

def get_size(bytes, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(bytes) < 1024.0:
            return "%3.1f%s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%.1f%s%s" % (bytes, 'Yi', suffix)

def get_processes_info(counter):
    # the list the contain all process dictionaries
    processes = []
    pids = []
    total_cpu_usage = 0
    total_memory_usage = 0
    for process in psutil.process_iter():
      if(process.pid!=os.getpid()):
        # get all process info in one shot
        with process.oneshot():
           # get the process id
           pid = process.pid
           if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
               continue
            # get the name of the file executed
           name = process.name()
            # get the time the process was spawned
           #try:
           #    create_time = datetime.fromtimestamp(process.create_time())
           #except OSError:
           #     # system processes, using boot time instead
           #    create_time = datetime.fromtimestamp(psutil.boot_time())
           #try:
           #      # get the number of CPU cores that can execute this process
           #     cores = len(process.cpu_affinity())
           # except psutil.AccessDenied:
           #     cores = 0
            # get the CPU usage percentage
           cpu_usage = process.cpu_percent()
           total_cpu_usage += cpu_usage
            # get the Memory  usage percentage
           mem_usage=process.memory_percent()
           total_memory_usage += mem_usage
            # get the status of the process (running, idle, etc.)
           status = process.status()
           #try:
           #     # get the process priority (a lower value means a more prioritized process)
           #    nice = int(process.nice())
           #except psutil.AccessDenied:
           #    nice = 0
           try:
                # get the memory usage in bytes
               memory_usage = process.memory_full_info().uss
           except psutil.AccessDenied:
               memory_usage = 0
            # total process read and written bytes
           #io_counters = process.io_counters()
           #read_bytes = io_counters.read_bytes
           #write_bytes = io_counters.write_bytes
            # get the number of total threads spawned by this process
           #n_threads = process.num_threads()
            # get the username of user spawned the process
           try:
               username = process.username()
           except psutil.AccessDenied:
               username = "N/A"
           try:
               exe = process.exe()
           except psutil.AccessDenied:
               exe = "Access to full path denied"
           #uptime=time.time() - process.create_time()
           #uptime=time.strftime('%H:%M:%S', time.gmtime(uptime))
           p=psutil.Process(pid)
           #cpu_times=p.cpu_times()
           cwd=p.cwd()
        processes.append({
            'pid': pid, 'name': name,'username': username,'cwd':cwd,'exe':exe,
            'cpu_usage': cpu_usage,'memory_usage': memory_usage,'status': status,
        })
        pids.append(pid)
    pid_collection[counter]=pids
    i=0
    if(counter>=60):
      counter=59
    for k,v in found10_10.items():
      if k not in pid_collection[counter]:
        #move to notfound10_10 and
        notfound10_10[k]=59

        #1)if pid not in pid_collection & pid in notfound10_10
        #  decrease value of pid in notfound10_10 until value=0
    for k,v in notfound10_10.items():
      if k not in pid_collection[counter]:
        if(notfound10_10[k]>0):
             notfound10_10[k]-=1
        if(notfound10_10[k]==0):
             deleted[i]=k
             i+=1
        if k in found10_10:
             notfound10_10[k]=59
             del found10_10[k]
        #if pid value=0 delete from notfound10_10
    for x in range(0,len(deleted)):
      pid=deleted[x]
      if pid in notfound10_10:
        del notfound10_10[pid]

    for y in range(0,len(pid_collection[counter])):
      pid=pid_collection[counter][y]
      #if pid found for the 1st time
      if pid not in found:
        found[pid]=1
        notfound10_10[pid]=1
         #if pid found in previous seconds
      else:
        found[pid]=found[pid]+1
        #and is stored in notfound10_10
        if pid in notfound10_10:
             #increase pid value until value=10
             if(notfound10_10[pid]<60):
                 notfound10_10[pid]=notfound10_10[pid]+1
             #if pid value=10 delete and move to found10_10
             if(notfound10_10[pid]==60):
                 found10_10[pid]=60
                 del notfound10_10[pid]

    return(total_cpu_usage,total_memory_usage,processes,pids)

def execute(counter):
    if(counter>=60):
         counter=59
         for x in range(0,counter):
             df_collection[x] = df_collection[x+1]
             pid_collection[x] = pid_collection[x+1]
    # get all process info
    total_cpu_usage,total_memory_usage,processes,pids = get_processes_info(counter)
    df_collection[counter]= pd.DataFrame(processes)
    df=df_collection[counter].iloc[:10]
    #df=df.sort_values(found_ratio)
    df = df[['pid', 'name','username','cpu_usage','memory_usage','exe','status','cwd']]
    s=df_collection[counter]
    #df=df_collection[counter].iloc[:10]
    return(total_cpu_usage,total_memory_usage,df,s,pids)
if __name__ == "__main__":
    counter=0
    s=0
    df_collection = {}
    pid_collection = {}
    deleted = {}
    found = {}
    found10_10 = {}
    notfound10_10 = {}
    lessthan60_60 = {}
    new = {}
    while(True):
        total_cpu_usage,total_memory_usage,df,s,pids = execute(counter)
        df['memory_usage']=df['memory_usage'].apply(get_size)
        os.system("clear")
        print(df.to_string())
        print("\n Total Processes:",len(pids)," || Total CPU(%) Usage: {:.2f}".format(total_cpu_usage), " || Total Memory(%) Usage: {:.2f}".format(total_memory_usage))
        print("\n    Max CPU Process Info")
        max_cpu_process = df['cpu_usage'].argmax()
        print(df.loc[max_cpu_process])
        max_mem_process=s['memory_usage'].argmax()
        s['memory_usage']=s['memory_usage'].apply(get_size)
        print("\n    Max Memory Process Info")
        print(s.loc[max_mem_process])
        # Create a list of tuples sorted by index 1 i.e. value field
        listofTuples = sorted(found.items() ,  key=lambda x: x[1])
        # Iterate over the sorted sequence
        found=OrderedDict(sorted(found.items(), key=lambda x: x[1]))
        dict_items = found.items()
        first10=list(dict_items)[:10]
         #df.sort_values(by=['found_ratio'], inplace=True)
        #df=df.iloc[:30]

        print("Processes with lowest uptime since programm started",first10)
        if(counter>=60):
             print("\n Processes not found in every sec ,in the last 60 secs",notfound10_10)
        sleep(1)
        counter+=1

