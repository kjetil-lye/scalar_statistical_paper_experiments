import xml.dom.minidom
def read_config(filename):
    return xml.dom.minidom.parse(filename)


def set_in_xml(xml_node, path, value):
    split_path = path.split(".")

    for tag_name in split_path:
        xml_node = xml_node.getElementsByTagName(tag_name)[0]

    xml_node.firstChild.nodeValue = value

def get_in_xml(xml_node, path):
    split_path = path.split(".")

    for tag_name in split_path:
        xml_node = xml_node.getElementsByTagName(tag_name)[0]

    return str(xml_node.firstChild.nodeValue)

def get_xml_node(xml_node, path):
    split_path = path.split(".")
    for tag_name in split_path:
        xml_node = xml_node.getElementsByTagName(tag_name)[0]

    return xml_node

def create_node_with_text(config, node_name, node_value):
    node = config.createElement(node_name)
    node_text = config.createTextNode(str(node_value))

    node.appendChild(node_text)
    return node


def make_functional_element(config, p, number_of_h, number_of_saves=8):
    basename = get_in_xml(config, "config.fvm.name").strip()


    functional = config.createElement("functional")

    name_node = create_node_with_text(config, "name", "structure_cube")
    p_node = create_node_with_text(config, "p", p)
    number_of_h_node = create_node_with_text(config, 'numberOfH', number_of_h)

    number_of_saves_node = create_node_with_text(config, "numberOfSaves", number_of_saves)

    writer_node = config.createElement("writer")

    type_node = create_node_with_text(config, "type", "netcdf")

    basename_node = create_node_with_text(config, 'basename',
                                          f"{basename}_functional_structure_cube_{p}")

    functional.appendChild(name_node)
    functional.appendChild(p_node)
    functional.appendChild(number_of_h_node)
    functional.appendChild(number_of_saves_node)
    writer_node.appendChild(type_node)
    writer_node.appendChild(basename_node)
    functional.appendChild(writer_node)

    return functional


def make_functional_element_direction(config, p, number_of_h, number_of_saves=8):
    basename = get_in_xml(config, "config.fvm.name").strip()


    functional = config.createElement("functional")

    name_node = create_node_with_text(config, "name", "structure_base")
    p_node = create_node_with_text(config, "p", p)
    number_of_h_node = create_node_with_text(config, 'numberOfH', number_of_h)
    direction_node = create_node_with_text(config, 'direction', 0)

    number_of_saves_node = create_node_with_text(config, "numberOfSaves", number_of_saves)

    writer_node = config.createElement("writer")

    type_node = create_node_with_text(config, "type", "netcdf")

    basename_node = create_node_with_text(config, 'basename',
                                          f"{basename}_functional_structure_cube_{p}")

    functional.appendChild(name_node)
    functional.appendChild(direction_node)
    functional.appendChild(p_node)
    functional.appendChild(number_of_h_node)
    functional.appendChild(number_of_saves_node)
    writer_node.appendChild(type_node)
    writer_node.appendChild(basename_node)
    functional.appendChild(writer_node)

    return functional

def make_functional_element_time(config, p, number_of_h, full_time_average,
                                 number_of_snapshots=200):
    basename = get_in_xml(config, "config.fvm.name").strip()
    end_time = float(get_in_xml(config, "config.fvm.endTime"))

    if not full_time_average:
        radius = 0.02 * end_time
    else:
        radius = 0.5 * end_time
        number_of_snapshots_node = create_node_with_text(config, "numberOfSnapshots", number_of_snapshots)


    save_time = end_time - radius

    functional = config.createElement("functional")

    name_node = create_node_with_text(config, "name", "structure_cube")
    p_node = create_node_with_text(config, "p", p)
    number_of_h_node = create_node_with_text(config, 'numberOfH', number_of_h)

    time_node = create_node_with_text(config, "time", save_time)
    time_radius_node = create_node_with_text(config, "timeRadius", radius)

    writer_node = config.createElement("writer")

    type_node = create_node_with_text(config, "type", "netcdf")

    basename_node = create_node_with_text(config, 'basename',
                                          f"{basename}_functional_time_integrated_structure_cube_{p}")

    functional.appendChild(name_node)
    functional.appendChild(p_node)
    functional.appendChild(time_node)
    functional.appendChild(number_of_h_node)
    functional.appendChild(time_radius_node)

    if full_time_average:
        functional.appendChild(number_of_snapshots_node)

    writer_node.appendChild(type_node)
    writer_node.appendChild(basename_node)
    functional.appendChild(writer_node)

    return functional

def create_writer(config):
    basename = get_in_xml(config, "config.fvm.name").strip()
    writer_node = config.createElement("writer")
    basename_node = create_node_with_text(config, 'basename', basename)
    type_node = create_node_with_text(config, 'type', 'netcdf')
    number_of_saves_node = create_node_with_text(config, 'numberOfSaves', 1)
    write_initial_timestep_node = create_node_with_text(config, 'writeInitialTimestep', 1)

    writer_node.appendChild(basename_node)
    writer_node.appendChild(type_node)
    writer_node.appendChild(number_of_saves_node)
    writer_node.appendChild(write_initial_timestep_node)

    return writer_node



def create_mean_var(config):
    basename = get_in_xml(config, "config.fvm.name").strip()
    stat_node = config.createElement("stat")
    name_node = create_node_with_text(config, 'name', 'meanvar')
    basename_node = create_node_with_text(config, 'basename', basename)
    type_node = create_node_with_text(config, 'type', 'netcdf')
    number_of_saves_node = create_node_with_text(config, 'numberOfSaves', 1)
    write_initial_timestep_node = create_node_with_text(config, 'writeInitialTimestep', 1)

    writer_node = config.createElement('writer')

    writer_node.appendChild(basename_node)
    stat_node.appendChild(name_node)
    writer_node.appendChild(type_node)
    stat_node.appendChild(number_of_saves_node)
    stat_node.appendChild(write_initial_timestep_node)
    stat_node.appendChild(writer_node)

    return stat_node

def create_moment_functionals(config, degree, time_average=True):
    basename = get_in_xml(config, "config.fvm.name").strip()
    end_time = float(get_in_xml(config, "config.fvm.endTime"))

    functional = config.createElement("functional")
    if time_average:
        radius = 0.25 * end_time


        save_time = end_time - radius
        time_node = create_node_with_text(config, "time", save_time)
        time_radius_node = create_node_with_text(config, "timeRadius", radius)
        functional.appendChild(time_node)
        functional.appendChild(time_radius_node)
    else:

        number_of_saves_node = create_node_with_text(config, "numberOfSaves", 1)

        functional.appendChild(number_of_saves_node)



    name_node = create_node_with_text(config, "name", "moment")
    p_node = create_node_with_text(config, "degree", degree)


    writer_node = config.createElement("writer")

    type_node = create_node_with_text(config, "type", "netcdf")

    if time_average:
        basename_node = create_node_with_text(config, 'basename',
                                              f"{basename}_functional_time_integrated_moment_{degree}")
    else:
        basename_node = create_node_with_text(config, 'basename',
                                              f"{basename}_functional_moment_{degree}")

    functional.appendChild(name_node)
    functional.appendChild(p_node)


    writer_node.appendChild(type_node)
    writer_node.appendChild(basename_node)
    functional.appendChild(writer_node)

    return functional


def create_identity_functionals(config, time_average=True):
    basename = get_in_xml(config, "config.fvm.name").strip()
    end_time = float(get_in_xml(config, "config.fvm.endTime"))

    functional = config.createElement("functional")
    if time_average:
        radius = 0.25 * end_time


        save_time = end_time - radius
        time_node = create_node_with_text(config, "time", save_time)
        time_radius_node = create_node_with_text(config, "timeRadius", radius)
        functional.appendChild(time_node)
        functional.appendChild(time_radius_node)
    else:

        number_of_saves_node = create_node_with_text(config, "numberOfSaves", 1)

        functional.appendChild(number_of_saves_node)



    name_node = create_node_with_text(config, "name", "identity")


    writer_node = config.createElement("writer")

    type_node = create_node_with_text(config, "type", "netcdf")

    if time_average:
        basename_node = create_node_with_text(config, 'basename',
                                              f"{basename}_functional_time_integrated_identity")
    else:
        basename_node = create_node_with_text(config, 'basename',
                                              f"{basename}_functional_identity")


    functional.appendChild(name_node)


    writer_node.appendChild(type_node)
    writer_node.appendChild(basename_node)
    functional.appendChild(writer_node)

    return functional

def create_bv_functionals(config, degree, time_average=True):
    basename = get_in_xml(config, "config.fvm.name").strip()
    end_time = float(get_in_xml(config, "config.fvm.endTime"))

    functional = config.createElement("functional")
    if time_average:
        radius = 0.25 * end_time


        save_time = end_time - radius
        time_node = create_node_with_text(config, "time", save_time)
        time_radius_node = create_node_with_text(config, "timeRadius", radius)
        functional.appendChild(time_node)
        functional.appendChild(time_radius_node)
    else:

        number_of_saves_node = create_node_with_text(config, "numberOfSaves", 1)

        functional.appendChild(number_of_saves_node)



    name_node = create_node_with_text(config, "name", "bv")
    p_node = create_node_with_text(config, "degree", degree)

    writer_node = config.createElement("writer")

    type_node = create_node_with_text(config, "type", "netcdf")

    if time_average:
        basename_node = create_node_with_text(config, 'basename',
                                              f"{basename}_functional_time_integrated_bv_{degree}")
    else:
        basename_node = create_node_with_text(config, 'basename',
                                              f"{basename}_functional_bv_{degree}")

    functional.appendChild(name_node)
    functional.appendChild(p_node)



    writer_node.appendChild(type_node)
    writer_node.appendChild(basename_node)
    functional.appendChild(writer_node)

    return functional
