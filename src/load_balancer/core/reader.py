HEADER_BUFFER_LENGTH = 4
HEADER_BUFFER_SIZE = 640

class ReaderPolicy:
    def __init__(self, conn):
        self.__conn = conn
    def _read_content(self):
        pass
    def handle(self):
        pass
    def disconnect():
        self.__enabled = False

class ReaderGeneric(ReaderPolicy):
    def __init__(self, conn):
        self.__conn = conn
        self.__enabled = True
    def __read_line(self):
        line = ''
        while (self.__enabled):
            try:
                char = self.__conn.recv(1).decode()
                if (char == '\n'):
                    break
                else:
                    line = line + char
            except BlockingIOError as error:
                return line
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
        data = self.__read_content()
        if len(data) == 0: # No messages in socket, we can close down the socket
            return "", False
        return data, True

class ReaderWithHeader(ReaderPolicy):
    def __init__(self, conn):
        self.__conn = conn
        self.__enabled = True
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
        while (self.__enabled and chunks_length > 0):
            chunk = self.__conn.recv(HEADER_BUFFER_SIZE).decode()
            data = data + chunk 
            chunks_length = chunks_length-1
        return data

    def handle(self):
        (length, length_valid) = self.__read_header()
        if (length_valid):
            return self.__read_content(), True
        else:
            return length, False

READER_POLICIES = {
    "Header": ReaderWithHeader,
    "Generic": ReaderGeneric
}

class ReadingHandler(ReaderPolicy):
    def __new__(self, reader_type, conn):
        return reader_type(conn)