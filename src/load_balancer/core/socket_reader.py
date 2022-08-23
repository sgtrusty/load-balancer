import logging

BUFFER_HEADER_LENGTH = 4
BUFFER_SIZE = 256

class SocketReader:
    def __read_header(self, conn):
        length = conn.recv(BUFFER_HEADER_LENGTH).decode()
        try:
            self.length = int(length)
            return self.length, True
        except ValueError:
            return length, False

    def __read_content(self, conn):
        chunks_length = self.length
        data = ''
        while (chunks_length > 0):
            chunk = conn.recv(BUFFER_SIZE).decode()
            data = data + chunk 
            chunks_length = chunks_length-1
        return data

    def handle(self, conn):
        (length, length_valid) = self.__read_header(conn)
        if (length_valid):
            del length_valid
            return self.__read_content(conn), True
        else:
            return length, False