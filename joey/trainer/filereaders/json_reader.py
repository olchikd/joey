import json
    

class JsonReader(BaseReader):
    type_name = 'json'
    sbuffer = ''
    decoder = json.JSONDecoder()

    def get_reader(self, stream):
        for line in stream:
            try:
                obj = self.process_read(line)
                if obj is not None:
                    yield obj
            except Exception, ex:
                raise ProcessingFieldException('Error in reading json data %s', ex)

    def process_read(self, data):
        self.sbuffer += data
        self.parsing = True
        while self.parsing:
            index = self.sbuffer.find('{')
            if index is not -1 and index is not 0:
                self.sbuffer = self.sbuffer[index:]
            try:
                obj, index = self.decoder.raw_decode(self.sbuffer)
            except Exception:
                self.parsing = False
            if self.parsing:
                self.sbuffer = self.sbuffer[index:]
                return obj
