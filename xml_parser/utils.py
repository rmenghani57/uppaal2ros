import xml.etree.ElementTree as ET
from custom_graph_objects import Node, Template

def extract_templates(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    templates = dict()
    for t in root.findall('template'):
        template_name = t.find('name').text
        template_declarations = t.find('declaration').text
        # Creating template object
        template = Template(template_name, template_declarations)
        # Extracting all nodes inside a template
        for n in t.findall('location'):
            node_id = n.attrib['id']
            node_name = n.find('name').text
            is_committed = False
            try:
                is_committed = n.find('committed').text
                is_committed = True
            except:
                pass
            # Adding the custom Node object into the custom Template object
            template.add_node(node_id, node_name, is_committed)
            if node_name == "Start":
                template.start_id = node_id

        # Extracting all edges inside a template
        for e in t.findall('transition'):
            # Finding the nodes that need to be connected
            source = e.find('source').attrib['ref']
            target = e.find('target').attrib['ref']
            # Find all the (label_type, label_value) pairs associated with an edge
            labels = []
            for label in e.findall('label'):
                kind = label.attrib['kind']
                value = label.text
                labels.append([kind, value])
            # append [target, [labels]] to the key 'source' in the adjacency list inside the template object
            template.add_directed_edge(source, target, labels)

        # Storing each of the templates / graphs in a dictionary, where the template's name is the key
        templates[template_name] = template
    return templates


def extract_text(filename, tag_name):
    tree = ET.parse(filename)
    root = tree.getroot()
    text = ""
    for g in root.findall(tag_name):
        text = g.text
    return text

def generate_ros_params(global_params):
    with open("params.yaml", "w") as f:
        assigned_lookup = dict()
        lines = global_params.split("\n")
        for line in lines:
            line = line.strip()
            if(not line.startswith("//") and len(line)):
                parts = [x.strip() for x in line.split(" ")]
                processed_parts = parts
                for idx, part in enumerate(parts):
                    if part == "//" or part.startswith("//"):
                        processed_parts = parts[:idx]
                        break
                # Remove semi-colons
                processed_parts[-1] = processed_parts[-1][:-1]

                if "chan" in processed_parts:
                    f.write(processed_parts[-1] + ": 0\n")
                # storing variables with assigned values so that they can be accessed when
                # translating other lines (like using N to initialize an array to all 0s)
                elif "=" in processed_parts:
                    for idx, part in enumerate(processed_parts):
                        if part == "=":
                            left = processed_parts[idx - 1]
                            right = " ".join(processed_parts[idx+1:])
                            processed_right = right.replace("{", "[")
                            processed_right = processed_right.replace("}", "]")
                            if right != processed_right:
                                left = left.split("[")[0]
                            assigned_lookup[left] = processed_right
                            f.write(left + ": " + processed_right + "\n")
                else:
                    # Checking if the current declaration is an Array
                    isArray = False
                    for idx, part in enumerate(processed_parts):
                        if "[" in part:
                            isArray = True
                            part_type = processed_parts[idx - 1]
                            part_name = part.split("[")[0]
                            # To check if the length is a variable or a concrete value
                            try:
                                length = int(assigned_lookup[part.split("[")[1].split("]")[0]])
                            except:
                                length = int(part.split("[")[1].split("]")[0])
                            processed_line = part_name + ": [" 
                            for i in range(length):
                                if part_type == "int":
                                    processed_line += "0"
                                elif part_type == "bool":
                                    processed_line += "false"
                                
                                if i != length - 1:
                                    processed_line += ","
                            processed_line += "]"
                            f.write(processed_line + "\n")
                    # This leaves us with the last case of an uninitialized variable
                    if(not isArray):
                        part_type = processed_parts[0]
                        processed_line = processed_parts[1] + ": "
                        if part_type == "int":
                            processed_line += "0"
                        elif part_type == "bool":
                            processed_line += "false"
                        f.write(processed_line + "\n")