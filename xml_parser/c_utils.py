from pycparser import parse_file, c_generator, c_parser, c_ast
from CodeGen import *

def generate_ros_base_class(template):
    template_name = template.name
    lines = [line.strip() for line in template.declarations.split("\n")]
    
    for line in lines:
        if not line.startswith("//"):
            parts = line.split(" ")
            for idx, part in enumerate(parts):
                if(part.startswith("//")):
                    parts = parts[:idx]
                    break
            # to find lines of variable initializations
            if((parts[0] == "int" or parts[0] == "bool") and (parts[-1] == ";" or parts[-1].endswith(";"))):
                bad_chars = ' ;'
                parts = ["".join(c for c in part if c not in bad_chars) for part in parts]
                variable = dict()
                for idx, part in enumerate(parts):
                    if(part == "int" or part == "bool"):
                        variable["type"] = part
                        variable["name"] = parts[idx + 1]
                        try:
                            variable["value"] = parts[idx + 3]
                        except:
                            variable["value"] = "NA"
                template_vars.append(variable)
            # if this is not the case, then we have encountered the end of all declarations
            else:
                break
    
    file_name = "{}_base_class.cpp".format(template_name)
    cpp = CppFile(file_name)
    cpp("#include <bits/stdc++.h>")
    cpp("#include <gnc_functions.hpp>")
    cpp("")
    with cpp.subs(class_name=template_name):
        with cpp.block("class $class_name$", ";"):
            cpp.label("private")
            for var_dict in template_vars:
                cpp("{} {};".format(var_dict["type"], var_dict["name"]))
            cpp.label("public")
            with cpp.block("$class_name$()"):
                cpp("nh = ros::NodeHandle(\"~\");")
                for var_dict in template_vars:
                    if(var_dict["value"] != "NA"):
                        cpp("this->{} = {};".format(var_dict["name"], var_dict["value"]))