import socket
import select
import sys
import os
import time

IP = str(socket.gethostbyname(socket.gethostname()))
PORT = 3838
ADDR = (IP, PORT)
FORMAT = "utf-8"
FILES = os.listdir("files/")
FOUND_FILE = ""
global file_with_header

def add_header(file_found, data_name):
    file_path = os.path.join(os.getcwd(), "files", file_found)
    file_size = os.path.getsize(file_path)
    file_name = data_name
    return file_name, file_size

def main():
    print("!!! STARTING SERVER !!!")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP and IPv4 protocols
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)  # binding with server ip and port
    server.listen(5)  # listening to the client (up to 5 clients)
    print(f"Server is listening on port: {PORT}")

    input_sock = [server]

    try:
        while True:
            read_ready, write_ready, exception = select.select(input_sock, [], [])

            for sock in read_ready:
                if sock == server:
                    client_sock, client_addr = server.accept()
                    input_sock.append(client_sock)
                else:
                    data = sock.recv(1024).decode(FORMAT)
                    file_from_command = data.split()
                    print("[RECV] buffer or data!")

                    if data:
                        for file in FILES:
                            print("======================== this is debug line ===================")
                            print(str(file_from_command[1]))
                            print(file)
                            if file_from_command[1] == file:
                                path_file = os.path.join(os.getcwd(), "files", file)
                                FOUND_FILE = path_file
                                # print(FOUND_FILE)
                                break
                            else:
                                continue

                        # generate header
                        file_name, file_size = add_header(FOUND_FILE, file_from_command[1])
                        print(file_name, file_size)
                        header_content = f"file-name: {file_name},\nfile-size: {file_size},\n\n\n"
                        client_sock.send(header_content.encode(FORMAT))
                        time.sleep(2)

                        with open(FOUND_FILE, 'rb') as file_chunk:
                            while True:
                                send_chunk = file_chunk.read()

                                if not send_chunk:
                                    break

                                # send to client
                                print("testestes  ")
                                client_sock.send(send_chunk)
                                print(send_chunk)
                                print("[SEND] buffer or data!")
                                time.sleep(0.3)

                        client_sock.close()
                    else:
                        sock.close()
                        input_sock.remove(sock)

    except KeyboardInterrupt:
        server.close()
        sys.exit(0)

if __name__ == "__main__":
    main()


