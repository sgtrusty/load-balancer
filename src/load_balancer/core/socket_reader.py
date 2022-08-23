BUFFER_HEADER_LENGTH = 4
#BUFFER_SIZE = 1
BUFFER_SIZE = 640

class SocketReader:
    def __init__(self, conn):
        self.__conn = conn

    def __read_header(self):
        length = self.__conn.recv(BUFFER_HEADER_LENGTH).decode()
        try:
            self.length = int(length)
            return self.length, True
        except ValueError:
            return length, False

    def __read_content(self):
        chunks_length = self.length
        data = ''
        while (chunks_length > 0):
            chunk = self.__conn.recv(BUFFER_SIZE).decode()
            data = data + chunk 
            chunks_length = chunks_length-1
        return data

    def handle(self):
        (length, length_valid) = self.__read_header()
        if (length_valid):
            del length_valid
            return self.__read_content(), True
        else:
            return length, False