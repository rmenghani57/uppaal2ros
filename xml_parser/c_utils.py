from pycparser import parse_file, c_generator, c_parser, c_ast
from CodeGen import *

def generate_ros_base_class(template):
    template_name = template.name
    with open("interim_base_file.c", "w") as f:
        f.writelines(template.declarations)
    
    ast = parse_file("interim_base_file.c", use_cpp=True)
    parser = c_parser.CParser()

    template_vars = list()
    for node in ast:
        if type(node) == c_ast.Decl:
            template_var = dict()
            template_var["name"] = node.type.declname
            template_var["type"] = node.type.type.names[0]
            if(node.init is not None):
                template_var["value"] = node.init.value
            else:
                template_var["value"] = "NA"
            template_vars.append(template_var)
    print(template_vars)

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