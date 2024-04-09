from pwn import remote, context
from re import match
from datetime import datetime
from time import sleep
import os
import db

LOG_ERRORS_FILE = './logs/errors.log'

LOG_FLAGS_FILE = './logs/flags.log'

HOST = '130.192.5.212'

PORT = 7777

TEAM_TOKEN = 'team1'

context.log_level = 'error'


def check_string(string):
    regex = r'ptm[A-Z0-9]{28}='
    if match(regex, string):
        return True
    else:
        return False


def log_error(error_message):
    log_folder = os.path.dirname(LOG_ERRORS_FILE)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_ERRORS_FILE, 'a') as f:
        f.write(f'[{timestamp}] {error_message}\n')


def log_flag(flag, status):
    log_folder = os.path.dirname(LOG_ERRORS_FILE)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FLAGS_FILE, 'a') as f:
        f.write(f'[{timestamp}] [{status}] {flag}\n')


def submit_flags(flags, host=HOST, port=PORT, team_token=TEAM_TOKEN):

    try:
        r = remote(host, port)
        r.recvuntil(b':\n')
        r.sendline(team_token.encode())
        r.recvuntil(b':\n')
    except Exception as e:
        log_error(str(e))

    points = 0.0
    submits = 0

    for flag in flags:

        flag = flag.strip()

        if not check_string(flag):
            log_flag(flag, 'INCORRECT')
            continue
        
        try:
            r.sendline(flag.encode())
            result = r.recvline().decode().split()

            if result[1].strip() == 'accepted!': #TODO Controlla se è questo il formato
                points += float(result[3])
                submits += 1
                log_flag(flag, 'ACCEPTED')
            elif result[2].strip() == 'your':
                log_flag(flag, 'YOUR')
            else:
                log_flag(flag, 'REJECTED')
            
        except Exception as e:
            log_error(str(e))

        db.update_submitted(flag)


    r.close()

    return [points, submits]


def main():
    
    while True:

        dic = db.find_flags()

        flags = []
        for el in dic:
            flags.append(el["flag"])

        info = submit_flags(flags)

        sleep(5)


if __name__ == '__main__':
    main()