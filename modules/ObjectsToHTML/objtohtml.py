from dbmanager import Tree

class ObjectToHTML:
    def get_head(self, name):
        doc_head = "<!DOCTYPE html>\n"\
                        "<html>\n"\
                        "<head>\n\t"\
	                    '<meta charset="utf-8">\n\t'\
                        "<title>" + name + "</title>\n</head>"\
        '<style type="text/css">\n\t'\
		'table{\tborder: 3px solid black;}\n\t'\
		'td{\tborder: 1px solid black;}\n</style>'
        return doc_head

    def get_attributes(self, a):
        attributes = list()
        print(a.__dir__())
        for attrib_name in a.__dir__():
            i = str(attrib_name).find('__')
            if i == -1:
                attrib = getattr(a, attrib_name)
                row = tuple((attrib_name, type(attrib).__name__))
                attributes.append(row)
        return attributes

    def build_table(self, filename, a):
        rows = self.get_attributes(a)
        head = self.get_head(a.__class__.__name__)
        file = open(filename, mode='x')
        file.write(head)
        file.write("<body>\n\t<table>\n\t")
        i = 0
        file.write("<tr>\n\t<th>Number</th>\n\t<th>Attribute Name</th>\n\t<th>Attribute Type</th>\n</tr>\n")
        for row in rows:
            file.write("<tr>\n\t")
            file.write("<td>" + str(i) + "</td>")
            file.write("<td>" + str(row[0]) + "</td>")
            file.write("<td>" + str(row[1]) + "</td>")
            file.write("</tr>\n\t")
            i += 1
        file.write("</table>\n")
        file.write("</body>")


class A:
    p = 1
    def a(self, num):
        print("kek")


if __name__ == '__main__':
    otohtml = ObjectToHTML()
    a = A()
    um = Tree()
    otohtml.build_table("/home/stacy/CODE/metaprogramming/module1/ObjectsToHTML/tree.html", um)
