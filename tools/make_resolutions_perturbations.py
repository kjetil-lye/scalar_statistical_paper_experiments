import argparse
import xml.dom.minidom
import shutil
import os
import re


from xml_tools import create_mean_var, create_writer, set_in_xml, get_xml_node, get_in_xml, read_config, make_functional_element, make_functional_element_time, create_identity_functionals, create_moment_functionals, create_bv_functionals, make_functional_element_direction
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="""
Makes an instance of the configuration file for each resolution and each perturbation. Folder layout will be

    pEPSILON/NRESOLUTION/configname.xml
            """)


    parser.add_argument('--resolutions', type=int, nargs='+', required=True,
                        help='Resolutions')

    parser.add_argument('--perturbations', type=str, nargs='+',
                        help="values of epsilon")


    parser.add_argument('--config', type=str, required=True,
                        help="Path to configuration file")

    parser.add_argument('--samples', type=int, nargs='+', default=[-1],
                        help='Number of samples per resolution (default 1 per resolution)')

    parser.add_argument('--single_sample_save', action='store_true',
                        help='Save single samples')

    parser.add_argument('--do_not_compute_structure', action='store_true',
                        help='Do not compute structure functions')

    parser.add_argument('--compute_mean_var', action='store_true',
                        help='Compute the mean and the variance')

    parser.add_argument('--full_time_average', action='store_true',
                        help='Do the full time average of the structure function')


    args = parser.parse_args()




    if args.samples == [-1]:
        samples = [1 for _ in args.resolutions]
    else:
        samples = args.samples

    for n, perturbation in enumerate(args.perturbations):
        perturbation_folder = "p{}".format(perturbation.replace(".","_"))
        os.makedirs(perturbation_folder, exist_ok=True)

        for m, resolution in enumerate(args.resolutions):
            config = read_config(args.config)
            resolution_folder = f"{perturbation_folder}/N{resolution}"
            os.makedirs(resolution_folder, exist_ok=True)


            sample = samples[m]

            set_in_xml(config, "config.uq.samples", str(sample))
            set_in_xml(config, "config.fvm.grid.dimension", f"{resolution} {resolution} 1")

            python_file = get_in_xml(config, "config.initialData.python")

            initial_data_parameters = get_xml_node(config, "config.initialData.parameters")

            for initial_data_parameter in initial_data_parameters.getElementsByTagName("parameter"):
                name = get_in_xml(initial_data_parameter, "name")

                if name == "epsilon":
                    set_in_xml(initial_data_parameter, "value", perturbation)

            shutil.copyfile(os.path.join(os.path.dirname(args.config), python_file),
                            os.path.join(resolution_folder, python_file))
            stats = get_xml_node(config, "config.uq.stats")

            if not args.do_not_compute_structure:
                number_of_h = int(resolution*32/1024)
                for stat in stats.getElementsByTagName("stat"):
                    set_in_xml(stat, "numberOfH", number_of_h)


                # Add functionals
                try:
                    functionals_element = get_xml_node(config, "config.fvm.functionals")
                except:
                    functionals_element = config.createElement("functionals")
                    get_xml_node(config, "config.fvm").appendChild(functionals_element)
                if not args.full_time_average:
                    for p in range(1,8):

                        functional = make_functional_element(config, p, number_of_h)
                        functionals_element.appendChild(functional)
                        functional_time = make_functional_element_time(config, p, number_of_h)
                        functionals_element.appendChild(functional_time)
                else:
                    for p in range(1,4):

                        functional = make_functional_element(config, p, number_of_h)
                        functionals_element.appendChild(functional)
                        functional_time = make_functional_element_time(config, p, number_of_h, full_time_average=True)
                        functionals_element.appendChild(functional_time)


                        functional_direction = make_functional_element_direction(config, p, number_of_h)
                        functionals_element.appendChild(functional_direction)

                functionals_element.appendChild(create_identity_functionals(config))
                functionals_element.appendChild(create_moment_functionals(config, 2))
                functionals_element.appendChild(create_identity_functionals(config, time_average=False))
                functionals_element.appendChild(create_moment_functionals(config, 2, time_average=False))

                for p in range(1, 4):
                    functionals_element.appendChild(create_bv_functionals(config, p, time_average=False))

                with open(os.path.join(resolution_folder, os.path.basename(args.config)), 'w') as f:

                    pretty_xml = config.toprettyxml(indent="  ")

                    # Default pretty print is not so pretty, so we make it prettier
                    while re.search(r"\n\s*\n", pretty_xml):
                        pretty_xml = re.sub(r"\n\s*\n", "\n", pretty_xml)
                    f.write(pretty_xml)

            else:
                for stat in stats.getElementsByTagName("stat"):
                    stats.removeChild(stat)


            if args.single_sample_save:
                writer = create_writer(config)

                fvm_node = get_xml_node(config, "config.fvm")

                fvm_node.appendChild(writer)



            if args.compute_mean_var:
                stats.appendChild(create_mean_var(config))

            with open(os.path.join(resolution_folder, os.path.basename(args.config)), 'w') as f:

                pretty_xml = config.toprettyxml(indent="  ")

                # Default pretty print is not so pretty, so we make it prettier
                # (the two following lines are not essential and can be removed if they cause problems)
                while re.search(r"\n\s*\n", pretty_xml):
                    pretty_xml = re.sub(r"\n\s*\n", "\n", pretty_xml)
                f.write(pretty_xml)
