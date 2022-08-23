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

HEADER_BUFFER_LENGTH = 4
HEADER_BUFFER_SIZE = 640

class ReaderPolicy:
    def __init__(self, reader):
        self.__reader = reader
    def _read_content(self):
        pass
    def handle(self):
        pass
    def disconnect():
        self.__enabled = False

class ReaderGeneric(ReaderPolicy):
    def __init__(self, reader):
        self.__reader = reader
        self.__enabled = True

    async def __read_content(self):
        data = ''
        while (not self.__reader.at_eof()):
            chunk = await self.__reader.readline()
            print(chunk)
            if(chunk == b''):
                break
            data = data + chunk.decode("utf-8")
        return data

    async def handle(self):
        data = await self.__read_content()
        if len(data) == 0: # No messages in socket, we can close down the socket
            return "", False
        return data, True

READER_POLICIES = {
    "Generic": ReaderGeneric
}

class ReadingHandler(ReaderPolicy):
    def __new__(self, reader_type, reader):
        return reader_type(reader)