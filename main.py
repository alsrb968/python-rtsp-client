import cv2
import socket
import threading

# 서버의 IP와 포트 번호를 정의합니다.
SOCKET_IP = '192.168.0.11'
SOCKET_PORT = 5001

RTSP_URL = f"rtsp://{SOCKET_IP}:5000/"

quit = False

def send_socket(client_socket):
    global quit
    try:
        while True:
            # 사용자 입력을 받습니다.
            message = input("Enter your message (or 'exit' to quit): ")
            
            # 'exit'를 입력하면 루프를 종료합니다.
            if message == 'exit':
                quit = True
                break

            data = message.strip().encode()
            # 메시지를 서버에 전송합니다.
            client_socket.sendall(data)
            print(f"Sent to server: {data}")
    finally:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()

def receive_socket(client_socket):
    global quit
    try:
        while not quit:
            # 서버로부터 응답을 받습니다.
            response = client_socket.recv(1024)
            if not response:
                break

            data = response.strip().decode()
            hex_str = ' '.join([hex(x) for x in response.strip()])
            print(f"Received from server: {data}({hex_str})")
    finally:
        client_socket.close()

# TCP 소켓 객체를 생성하고 서버에 연결합니다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SOCKET_IP, SOCKET_PORT))

# 송신 및 수신 스레드를 생성합니다.
send_thread = threading.Thread(target=send_socket, args=(client_socket,))
receive_thread = threading.Thread(target=receive_socket, args=(client_socket,))

send_thread.start()
receive_thread.start()

# Create a VideoCapture object
cap = cv2.VideoCapture(RTSP_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

# Check if the connection was successful
if not cap.isOpened():
    print("Failed to connect to RTSP server")
    exit()

# Read and display video frames
while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow('RTSP Client', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q') or quit:
        break

# Release the VideoCapture object and close the display window
cap.release()
cv2.destroyAllWindows()
