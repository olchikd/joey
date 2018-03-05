import csv


class CsvReader(BaseReader):
    type_name = 'csv'

    def get_reader(self, stream):
        reader = csv.DictReader(
            stream,
            quotechar="'",
            quoting=csv.QUOTE_ALL
        )
        for obj in reader:
            for key, value in obj.items():
                # loading json fields
                strkey = str(obj[key])
                if strkey.startswith('{') or strkey.startswith('['):
                    try:
                        obj[key] = json.loads(value)
                    except Exception:
                        pass
            yield obj
