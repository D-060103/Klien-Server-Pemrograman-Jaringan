"""
Client with serversocket module

By Group 12:
=> 5025201010 - I Putu Bagus Adhi Pradana
=> 5025201245 - Achmad Ferdiansyah
=> 5025201123 - David Fischer Simanjutak

Network Programming : D
Informatics Engineering - ITS

"""

import socket
import sys      # implements command line
import os
import time

# server ip and port
IP = str(socket.gethostbyname(socket.gethostname()))
# IP = "10.21.95.0"
PORT = 3838
ADDR = (IP, PORT)
FORMAT = "utf-8"
BUFFER_SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP and IPv4 protocols
    client.connect(ADDR) # connecting to server

    try:
        # total_chunk = ""
        # chunk = ""
        print('\n!!! if you want to download something, please text "download [your_file]" !!!')
        command = input("enter your command > ")
        split_command = command.split()

        if len(split_command) < 2:
            print("Command must be more than 1 word!")
            client.close()
            sys.exit(0)

        if split_command[0] != "download":
            print("Wrong command, please input command correctly!")
            client.close()
            sys.exit(0)

        client.send(command.encode(FORMAT))
        print("[SEND] buffer or data!")
        time.sleep(1)

        header_info = client.recv(BUFFER_SIZE).decode(FORMAT)
        time.sleep(2)
        print(header_info)

        # parsing header
        print('===================================================')
        header_line = header_info.split('\n')
        print(header_line)
        name_line = header_line[0].split()
        name = name_line[1].split(",")
        file_name = name[0]
        size_line = header_line[1].split()
        size = size_line[1].split(",")
        file_size = size[0]
        print(f"\nfilename: {file_name}")
        print(f"filesize: {file_size}\n")
        print('===================================================')
        time.sleep(2)

        # create directory for downloaded files
        if not os.path.exists('files/'):
            os.makedirs('files')

        with open(file_name, 'wb+') as downloaded_file:
            file_content = []
            while True:
                chunk = client.recv(BUFFER_SIZE)
                print("[RECV] buffer or data!")
                print(chunk)

                # end of len of chunk
                if not chunk:
                    break

                file_content.append(chunk)
                time.sleep(0.5)

            for file_chunk in file_content:
                downloaded_file.write(file_chunk)
            # downloaded_file.write(file_content)
        print('MASUK SINI KAH ???')
        client.close()
        print('OKE MANTAP !!!')

    except:
        print('ini biangnya!!!')
        client.close()
        sys.exit(0)

if __name__ == "__main__":
    main()