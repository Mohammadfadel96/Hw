import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 12345)
client_socket.connect(server_address)

# Send account number to the server for authentication
account_number = input("Enter your account number: ")
client_socket.send(account_number.encode())

# Receive authentication response from the server
response = client_socket.recv(1024).decode()
print(response)

if response == "Welcome!":
    while True:
        option = input("Enter your transaction option:\nc for check balance\nd for deposit\nw for withdraw\ne for exit\n")
        client_socket.send(option.encode())
        if option.lower() == "d":
            amount = input("enter amount of deposit\n")
            client_socket.send(amount.encode())
        elif option.lower() == "w":
            amount = input("enter amount of withdrawal\n")
            client_socket.send(amount.encode())
        if option.lower() == "e":
            break
        else:
            response = client_socket.recv(1024).decode()
            print(response)

# Receive final account balance from the server
final_balance = client_socket.recv(1024).decode()
print(f"Final account balance: {final_balance}")

# Close the socket connection
client_socket.close()
