# Import socket module
import socket
 
def connect(addr, policy_class):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect(addr)
 
    # message you send to server
    message = "shaurya says geeksforgeeks"
    while True:
 
        # message sent to server
        s.send(message.encode('ascii'))
 
        # message received from server
        data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(data.decode('ascii')))
 
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()
 
def main():
    parser = argparse.ArgumentParser(description='Metric Load Balancer')
    parser.add_argument('-a', dest='policy', choices=POLICIES)
    parser.add_argument('-ip', dest='ip', type=str, help='load balancer ip', default='127.0.0.1')
    parser.add_argument('-p', dest='port', type=int, help='load balancer port', default=5000)
    args = parser.parse_args()
    
    connect((args.ip, args.port), POLICIES[args.policy])
 
if __name__ == '__main__':
    main()
