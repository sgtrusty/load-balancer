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