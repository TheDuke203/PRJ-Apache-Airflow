from configparser import ConfigParser
import os

dag_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

filename = os.path.join(dag_dir, "database.ini")

def config(filename=filename, section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))
    return db