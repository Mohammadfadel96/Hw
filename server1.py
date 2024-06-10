import socket
import threading

# Pre-defined bank accounts with balances
accounts = {
    '1': 1000,
    '2': 500,
}

def handle_client(client_socket):
    account_number = client_socket.recv(1024).decode()
    if account_number in accounts:
        client_socket.send("Welcome!".encode())
        while True:
            option = client_socket.recv(1024).decode()
            if option.lower() == "c":
                client_socket.send(str(accounts[account_number]).encode())
            elif option.lower() == "d":
                amount = int(client_socket.recv(1024).decode())
                accounts[account_number] += amount
                client_socket.send("Deposit successful".encode())
            elif option.lower() == "w":
                amount = int(client_socket.recv(1024).decode())
                if amount <= accounts[account_number]:
                    accounts[account_number] -= amount
                    client_socket.send("Withdrawal successful".encode())
                else:
                    client_socket.send("Insufficient funds".encode())
            else:
                break
        # Send final account balance to the client
        client_socket.send(str(accounts[account_number]).encode())
    else:
        client_socket.send("Invalid account! check your number and try again\n".encode())
    client_socket.close()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to  address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening for incoming connections...")

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
