import cv2
import socket
import threading

# 서버의 IP와 포트 번호를 정의합니다.
SOCKET_IP = '192.168.0.17'
SOCKET_PORT = 5001

RTSP_URL = f"rtsp://{SOCKET_IP}:5000/"

quit = False

def receive_socket():    
    # TCP 소켓 객체를 생성합니다.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 서버에 연결합니다.
    client_socket.connect((SOCKET_IP, SOCKET_PORT))
    
    try:
        while True:
            # 사용자 입력을 받습니다.
            message = input("Enter your message (or 'exit' to quit): ")
            
            # 'exit'를 입력하면 루프를 종료합니다.
            if message == 'exit':
                break

            # 메시지를 서버에 전송합니다.
            client_socket.sendall(message.encode())
            print(f"Sent to server: {message}")
            # break

            # 서버로부터 응답을 받습니다.
            response = client_socket.recv(1024)
            print(f"Received from server: {response.decode()}")
    finally:
        # 소켓 연결을 종료합니다.
        client_socket.close()
        global quit
        quit = True


# Create a VideoCapture object
cap = cv2.VideoCapture(RTSP_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

# Check if the connection was successful
if not cap.isOpened():
    print("Failed to connect to RTSP server")
    exit()

t = threading.Thread(target=receive_socket)
t.start()

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