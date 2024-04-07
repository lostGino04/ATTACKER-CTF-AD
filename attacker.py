from pwn import *
import threading
import datetime
import inspect
import fcntl

def acquire_lock(file):
    fcntl.flock(file, fcntl.LOCK_EX)

def release_lock(file):
    fcntl.flock(file, fcntl.LOCK_UN)

# Funzione che restituisce il nome della funzione in cui viene eseguito
def get_function_name():
    return inspect.currentframe().f_back.f_back.f_code.co_name

# Funzione error handler
def error_handler(error):
    e = datetime.datetime.now()
    err_log = open("log.txt", "a")
    err_log.write(f"{e.hour}:{e.minute}:{e.second} something went wrong in {get_function_name()}: [{error}] \n")
    err_log.close()

# Funzione che scrive la flag sul file txt dopo che la trova
def scrivi_flag(flag):
    flag_file = open("flags.txt", "a+")
    acquire_lock(flag_file)
    flag_file.write(f"{flag}\n")
    release_lock(flag_file)

# Definizione delle funzioni exploit
def exploit1(chiave, valore):
    try:
        flag = "ptmurbioegviuorebgwverw"
        print(chiave)
        print(valore)
        scrivi_flag(flag)
    except Exception as e:
        error_handler(e)

def exploit2(chiave, valore):
    try:
        flag = "ptmewiuvqgofuevwc"
        print(chiave + " 2")
        print(valore + " 2")
        scrivi_flag(flag)
    except Exception as e:
       error_handler(e)
# E così via...

# La funzione attack si occupa di eseguire gli exploit, ogni exploit viene eseguito indipendentemente dagli altri, utilizzando il multi threading
def attack(exploits):
    try:
        esecuzioni = []
        for exploit in exploits:
            thread = threading.Thread(target=exploit)
            thread.daemon = True
            esecuzioni.append(thread)
        for thread in esecuzioni:
            thread.start()
        for thread in esecuzioni:
            thread.join()
    except Exception as e:
        error_handler(e)

# Funzione main dalla quale partirà tutto, i threads vengono generati
# in ordine macchina --> tutti gli exploit possibili
def main():
    try:
        victims_list = [("id1", "value1"),("id2", "value2")]
        #victims_list = [("id1", "value1")]
        for victim in victims_list:
            attack([lambda: exploit1(victim[0], victim[1]), lambda: exploit2(victim[0], victim[1])])
            #attack([lambda: exploit()])
    except Exception as e:
        error_handler(e)

# Chiamiamo la funzione main per avviare il programma
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()