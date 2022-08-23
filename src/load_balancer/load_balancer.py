'''
 # SpinachSocket - a metric load balancer with multi-threading
 # Copyright (C) 2022  Santiago González <https://github.com/sgtrusty>
 #             ~ Assembled through trust in coffee. ~
 #
 # This program is free software; you can redistribute it and/or modify
 # it under the terms of the CC BY-NC-ND 4.0 as published by
 # the Creative Commons; either version 2 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # CC BY-NC-ND 4.0 for more details.
 #
 # You should have received a copy of the CC BY-NC-ND 4.0 along
 # with this program; if not, write to the  Creative Commons Corp.,
 # PO Box 1866, Mountain View, CA 94042.
 #
'''
import argparse

from core.system import init

# Our main function.
def main():
    parser = argparse.ArgumentParser(description='Metric Load Balancer')
    # TODO: add policies from cmd line
    #parser.add_argument('-a', dest='policy', choices=POLICIES)
    parser.add_argument('-i', dest='ip', type=str, help='load balancer ip', default='127.0.0.1')
    parser.add_argument('-p', dest='port', type=int, help='load balancer port', default=5000)
    args = parser.parse_args()
    
    init((args.ip, args.port))

if __name__ == '__main__':
    main()