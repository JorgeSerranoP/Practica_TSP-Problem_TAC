# LEE UN FICHERO DE TEXTO PLANO Y LO DEVUELVE COMO STRING


def read_file(file):
    with open(file, 'r') as reader:
        content = reader.read().splitlines()
        lines = [x.lstrip() for x in content if x != ""]
        return lines
