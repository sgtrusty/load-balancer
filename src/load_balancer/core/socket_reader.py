HEADER_BUFFER_LENGTH = 4
HEADER_BUFFER_SIZE = 640

class SocketReader:
    def __init__(self, conn):
        self.__conn = conn
    def _read_content(self):
        pass
    def handle(self):
        pass

class SocketReaderGeneric(SocketReader):
    def __init__(self, conn):
        self.__conn = conn
    def __read_line(self):
        line = ''
        while (True):
            char = self.__conn.recv(1).decode()
            if (char == '\n'):
                break
            else:
                line = line + char
        return line

    def __read_content(self):
        data = ''
        while (True):
            chunk = self.__read_line()
            if(chunk == ''):
                break
            data = data + chunk + '\n'
        return data

    def handle(self):
        return self.__read_content(), True

class SocketReaderWithHeader(SocketReader):
    def __init__(self, conn):
        self.__conn = conn
    def __read_header(self):
        length = self.__conn.recv(HEADER_BUFFER_LENGTH).decode()
        try:
            self.length = int(length)
            return self.length, True
        except ValueError:
            return length, False

    def __read_content(self):
        chunks_length = self.length
        data = ''
        while (chunks_length > 0):
            chunk = self.__conn.recv(HEADER_BUFFER_SIZE).decode()
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

READER_POLICIES = {
    "Header": SocketReaderWithHeader,
    "Generic": SocketReaderGeneric
}