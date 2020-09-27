from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parseString


def parse_message(messagedata):
    xml_data = parseString(messagedata.rstrip('\0'))
    root = xml_data.documentElement
    name = root.tagName
    attributes = {}
    children = {}
    for i in range(0, root.attributes.length):
        item = root.attributes.item(i)
        attributes[item.name] = item.value

    child = root.firstChild
    child_num = 0
    while child is not None and child_num < 5000:
        child_num += 1

        new_child = {}
        for i in range(0, child.attributes.length):
            item = child.attributes.item(i)
            new_child[item.name] = item.value

        childname = child.tagName
        if childname in children:
            # this is a multi-value attribute, i.e. a list
            # if there is only one element at the moment, wrap it in a list so we can add more
            if not isinstance(children[childname], list):
                children[childname] = [children[childname]]
            children[childname].append(new_child)
        else:
            children[childname] = new_child

        child = child.nextSibling

    return name, attributes, children


def construct_message(name, attributes=None, children=None):
    if attributes is None:
        attributes = {}
    impl = getDOMImplementation()
    message = impl.createDocument(None, name, None)
    root_element = message.documentElement
    for key, val in list(attributes.items()):
        root_element.setAttribute(str(key), str(val))
    if children is not None:
        for key, val in list(children.items()):
            new_child = message.createElement(key)
            if val is not None:
                for attr_key, attr_val in list(val.items()):
                    new_child.setAttribute(str(attr_key), str(attr_val))
            root_element.appendChild(new_child)
    return root_element.toxml()
