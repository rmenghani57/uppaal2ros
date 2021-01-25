import utils

if __name__ == '__main__':
    templates = utils.extract_templates('behavioral_model.xml')
    global_params = utils.extract_text('behavioral_model.xml', 'declaration')
    system_declarations = utils.extract_text('behavioral_model.xml', 'system')

    # to print out the directed graph for debug purposes
    for t in templates:
        print("Nodes in template:", templates[t].name)
        # The graph starts at this point
        print("Template start node at:", templates[t].start_id)
        # printing the adjacency list graph representation inside a template
        for n in templates[t].adjacency_list:
            print(n, templates[t].adjacency_list[n])
    
    # print(global_params)
    # print(system_declarations)

    utils.generate_ros_params(global_params)
    # print(assigned_lookup)