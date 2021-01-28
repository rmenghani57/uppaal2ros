from pycparser import parse_file, c_generator, c_parser, c_ast
from CodeGen import *

def extract_declarations_and_functions(ast):
    template_vars = list()
    template_funcs = list()
    for node in ast:
        if type(node) == c_ast.Decl:
            print(node)
            template_var = dict()
            if(type(node.type) == c_ast.TypeDecl):
                template_var["decl_type"] = "type_decl"
                template_var["name"] = node.type.declname
                template_var["type"] = node.type.type.names[0]
                if(node.init is not None):
                    template_var["value"] = node.init.value
                else:
                    template_var["value"] = "NA"
            elif(type(node.type) == c_ast.ArrayDecl):
                template_var["decl_type"] = "array_decl"
                template_var["name"] = node.type.type.declname
                template_var["type"] = node.type.type.type.names[0]
                try:
                    template_var["array_dim"] = node.type.dim.name
                except:
                    template_var["array_dim"] = node.type.dim.value
                array_init = list()
                if(node.init is not None):
                    for item in node.init.exprs:
                        if template_var["type"] == "int":
                            array_init.append(int(item.value))
                        elif template_var["type"] == "bool":
                            if item.name == "true":
                                array_init.append(1)
                            else:
                                array_init.append(0)
                        else:
                            array_init.append(item.name)
                    template_var["value"] = array_init
                else:
                    template_var["value"] = "NA"
                    
            template_vars.append(template_var)
    return [template_vars, template_funcs]


def generate_ros_base_class(template):
    template_name = template.name
    template_declarations = [line for line in template.declarations.split("\n")]
    with open("interim_base_file.c", "w") as f:
        f.write("typedef enum { false, true } bool;\n")
        for line in template_declarations:
            temp_line = "".join(c for c in line if c != " ")
            if "for(" in temp_line:
                loop_var = temp_line.split("(")[1][0]
                loop_var_type = temp_line.split(":")[1].split("[")[0]

                loop_range_line = temp_line.split("[")[1]
                loop_range_line = loop_range_line.split("]")[0]
                loop_start = loop_range_line.split(",")[0]
                loop_end = loop_range_line.split(",")[1]
                f.write("for({} {}={}; {} < {}; {}++)\n".format(loop_var_type, loop_var, loop_start, loop_var, loop_end, loop_var))
            else:
                f.write(line + "\n")
    
    ast = parse_file("interim_base_file.c", use_cpp=True)

    template_vars, template_funcs = extract_declarations_and_functions(ast)

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
                        if(var_dict["decl_type"] == "array_decl"):
                            temp_val = "{"
                            for idx, item in enumerate(var_dict["value"]):
                                if(var_dict["type"] == "bool"):
                                    if item:
                                        temp_val += "true"
                                    else:
                                        temp_val += "false"
                                else:
                                    temp_val += str(item)
                                if idx != len(var_dict["value"]) - 1:
                                    temp_val += ","
                                else:
                                    temp_val += "}"
                            var_dict["value"] = temp_val
                        cpp("this->{} = {};".format(var_dict["name"], var_dict["value"]))

    cpp.close()

# Here 'g' is the graph object
# def generate_ros_node(g):