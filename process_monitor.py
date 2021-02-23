import psutil
from datetime import datetime
import pandas as pd
import time
import os
from collections import Counter

def get_size(bytes, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(bytes) < 1024.0:
            return "%3.1f%s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%.1f%s%s" % (bytes, 'Yi', suffix)

def get_processes_info():
    # the list the contain all process dictionaries
    processes = []
    pids = []
    total_cpu_usage = 0
    total_memory_usage = 0
    for process in psutil.process_iter():
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
           try:
               create_time = datetime.fromtimestamp(process.create_time())
           except OSError:
                # system processes, using boot time instead
               create_time = datetime.fromtimestamp(psutil.boot_time())
#           try:
#                # get the number of CPU cores that can execute this process
#               cores = len(process.cpu_affinity())
#           except psutil.AccessDenied:
#               cores = 0
            # get the CPU usage percentage
           cpu_usage = process.cpu_percent()
           total_cpu_usage += cpu_usage
            # get the Memory  usage percentage
           mem_usage=process.memory_percent()
           total_memory_usage += mem_usage
            # get the status of the process (running, idle, etc.)
           status = process.status()
           try:
                # get the process priority (a lower value means a more prioritized process)
               nice = int(process.nice())
           except psutil.AccessDenied:
               nice = 0
           try:
                # get the memory usage in bytes
               memory_usage = process.memory_full_info().uss
           except psutil.AccessDenied:
               memory_usage = 0
            # total process read and written bytes
           io_counters = process.io_counters()
           read_bytes = io_counters.read_bytes
           write_bytes = io_counters.write_bytes
            # get the number of total threads spawned by this process
           n_threads = process.num_threads()
            # get the username of user spawned the process
           try:
               username = process.username()
           except psutil.AccessDenied:
               username = "N/A"
           try:
               exe = process.exe()
           except psutil.AccessDenied:
               exe = "Access to full path denied"
           # try:
           #     uids = process.uids()
           # except psutil.Access.Denied:
           #     uids= "N/A"
       processes.append({
            'pid': pid, 'name': name, 'create_time': create_time,
            'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
            'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads, 'username': username,'exe': exe
       })
       pids.append(pid)

    return(processes,pids,total_cpu_usage,total_memory_usage)

def construct_dataframe(processes):
    # convert to pandas dataframe
    df = pd.DataFrame(processes)
    # set the process id as index of a process
    df.set_index('pid', inplace=True)
    # sort rows by the column passed as argument
    df.sort_values(sort_by, inplace=True, ascending=descending)
    # pretty printing bytes
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(
        datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    # reorder and define used columns
    df = df[columns.split(",")]
    return df

def execute(counter):
    if(counter>=10):
         counter=9
         for x in range(0,counter):
             df_collection[x] = df_collection[x+1]
             pid_collection[x] = pid_collection[x+1]
    # get all process info
    processes,pids,total_cpu_usage,total_memory_usage = get_processes_info()
    df_collection[counter] = construct_dataframe(processes)
    pid_collection[counter]=pids
    df=df_collection[counter].iloc[:10]
    return(df,processes,pids,total_cpu_usage,total_memory_usage)

def score(counter):
        if(counter<10):
           for y in range(0,len(pid_collection[counter])):
              pid=pid_collection[counter][y]
              if pid not in found:
                  found[pid]=1
                  notfound10_10[pid]=1
              else:
                  found[pid]=found[pid]+1
                  if(notfound10_10[pid]<10):
                           notfound10_10[pid]=notfound10_10[pid]+1
                  if(notfound10_10[pid]==10):
                           found10_10[pid]=10
                           del notfound10_10[pid]
        #if(counter==10):
        #   for k,v in found.items():
        #      if(v==10):
        #          found10_10[k]=v
        #      else:
        #          notfound10_10[k]=v
        if(counter>=10):
           counter=9
           for y in range(0,len(pid_collection[counter])):
              pid=pid_collection[counter][y]
              if pid in found:
                  if pid in notfound10_10:
                      if(notfound10_10[pid]<10):
                           notfound10_10[pid]=notfound10_10[pid]+1
                      if(notfound10_10[pid]==10):
                           found10_10[pid]=10
                           del notfound10_10[pid]
                  #if pid in found10_10:
                      #
              if pid not in found:
                      found[pid]=1
                      notfound10_10[pid]=1
              for k,v in found10_10.items():
                  if k not in pid_collection[counter]:
                      notfound10_10[k]=9
              if pid in found10_10:
                  if pid in notfound10_10:
                      if(notfound10_10[pid]==9):
                           del found10_10[pid]
              for k,v in notfound10_10.items():
                  if k not in pid_collection[counter]:
                      notfound10_10[k]=notfound10_10[k]-1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Process Viewer & Monitor")
    parser.add_argument("-c", "--columns", help="""Columns to show,
                                                available are name,create_time,cores,cpu_usage$
                                                Default is name,cpu_usage,memory_usage,read_by$
                        default="name,username,cpu_usage,memory_usage,create_time,exe,status,n$
    parser.add_argument("-s", "--sort-by", dest="sort_by",
                        help="Column to sort by, default is memory_usage .", default="memory_u$
    parser.add_argument("--descending", action="store_true",
                        help="Whether to sort in descending order.")
    parser.add_argument(
        "-n", help="Number of processes to show, will show all if 0 is specified, default is 2$
    parser.add_argument("-u", "--live-update", action="store_true",
                        help="Whether to keep the program on and updating process information $

    # parse arguments
    args = parser.parse_args()
    columns = args.columns
    sort_by = args.sort_by
    descending = args.descending
    n = int(args.n)
    live_update = args.live_update
   counter=0
    s=0
    df_collection = {}
    pid_collection = {}
    old = {}
    found = {}
    found10_10 = {}
    notfound10_10 = {}
    new = {}
    while(True):
        df,processes,pids,total_cpu_usage,total_memory_usage = execute(counter)
        score(counter)
        os.system("cls") if "nt" in os.name else os.system("clear")
        if n == 0:
             print(df.to_string())
        elif n > 0:
             print(df.head(n).to_string())
        print("\n Total Processes:",len(pids)," || Total CPU(%) Usage: {:.2f}".format(total_cp$
        print("\n    Max CPU Process Info")
        max_cpu_process = df['cpu_usage'].argmax()
        print(df.loc[max_cpu_process])
        print(notfound10_10)
        counter+=1
        time.sleep(1)

