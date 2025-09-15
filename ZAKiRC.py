import socket
import threading

# ----- CONFIGURATION -----
SERVER = "irc.libera.chat"
PORT = 6667
NICKNAME = "PUTNICKNAMEHERE"
CHANNEL = "#hexchat"  # Change to your desired channel

# ----- CONNECT TO SERVER -----
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((SERVER, PORT))
irc.send(f"NICK {NICKNAME}\r\n".encode("utf-8"))
irc.send(f"USER {NICKNAME} 0 * :Python IRC Client\r\n".encode("utf-8"))
irc.send(f"JOIN {CHANNEL}\r\n".encode("utf-8"))

# ----- FUNCTIONS -----
def send_message(message):
    """Send a message to the IRC channel."""
    if message.strip():  # Avoid empty messages
        irc.send(f"PRIVMSG {CHANNEL} :{message}\r\n".encode("utf-8"))
        print(f"<{NICKNAME}> {message}")  # Show your own message in console

def receive_messages():
    """Thread function to receive messages from server."""
    while True:
        try:
            response = irc.recv(2048).decode("utf-8")
            if response.startswith("PING"):
                # Respond to PING to stay connected
                irc.send(f"PONG {response.split()[1]}\r\n".encode("utf-8"))
            else:
                print("\n" + response.strip())
        except Exception:
            break

# ----- START RECEIVING THREAD -----
threading.Thread(target=receive_messages, daemon=True).start()

print(f"Connected to {CHANNEL}! Type your messages below:")

# ----- MAIN LOOP -----
while True:
    try:
        msg = input()
        send_message(msg)
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        irc.send(f"QUIT :Bye!\r\n".encode("utf-8"))
        irc.close()
        break
