import argparse

from core.system import init

# Our main function.
def main():
    parser = argparse.ArgumentParser(description='Metric Load Balancer')
    #parser.add_argument('-a', dest='policy', choices=POLICIES)
    parser.add_argument('-i', dest='ip', type=str, help='load balancer ip', default='127.0.0.1')
    parser.add_argument('-p', dest='port', type=int, help='load balancer port', default=5000)
    args = parser.parse_args()
    
    #init(('127.0.0.1', args.port), POLICIES[args.policy])
    init((args.ip, args.port))

if __name__ == '__main__':
    main()