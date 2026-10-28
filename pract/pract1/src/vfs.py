import xml.etree.ElementTree as ET


def _parse_node(element):
    node_type = element.tag
    if node_type not in ("directory", "file"):
        raise ValueError(f"неизвестный тип XML-узла: {node_type}")
    name = element.attrib.get("name")
    if not name:
        raise ValueError(f"у узла {node_type} отсутствует атрибут name")

    node = {"type": node_type, "name": name}
    if node_type == "directory":
        node["children"] = [_parse_node(child) for child in element]
        if any(child.tag not in ("directory", "file") for child in element):
            raise ValueError(f"недопустимый дочерний элемент в {name}")
    else:
        node["content"] = element.text or ""
    return node


def load_vfs(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as error:
        raise ValueError(f"неверный формат XML: {error}") from error

    root = tree.getroot()
    if root.tag != "directory":
        raise ValueError("корневой элемент XML должен быть directory")
    node = _parse_node(root)
    if node["name"] != "/":
        raise ValueError("имя корневой директории должно быть /")
    return node