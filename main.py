from operator import attrgetter
import jinja2
import os
from oslo_config import generator, types
import sys
import yaml

if __name__ == "__main__":
    SERVICE = sys.argv[1]

    NAMESPACES = os.environ.get("NAMESPACES", "/namespaces.yaml")
    OUTPUT = os.environ.get("OUTPUT", "/output")
    TEMPLATES_PATH = os.environ.get("TEMPLATES_PATH", "/templates")

    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    environment = jinja2.Environment(loader=loader)

    with open(NAMESPACES) as fp:
        CONFIG_NAMESPACES = yaml.safe_load(fp)

    ns = CONFIG_NAMESPACES[SERVICE]
    groups = generator._get_groups(generator._list_opts(ns))

    template_service = environment.get_template("service.j2")
    fp = open(f"/output/{SERVICE}.rst", "w+")
    template_data = {
        "name": SERVICE,
        "sections": sorted(groups.keys())
    }
    fp.write(template_service.render(template_data))

    template = environment.get_template("confval.j2")
    for name, data in groups.items():
        _, options = data['namespaces'][0]

        if not options:
            next

        option_types = {}
        for option in options:
            if isinstance(option.type, types.List):
                option_type = "List of %s" % option.type.item_type
            elif isinstance(option.type, types.Boolean):
                option_type = "Boolean"
            elif isinstance(option.type, types.Integer):
                if option.type.min and option.type.max:
                    option_type = "Integer, ``>= %d``, ``<= %d``" % (option.type.min, option.type.max)
                elif option.type.min:
                    option_type = "Integer, ``>= %d``" % option.type.min
                elif option.type.max:
                    option_type = "Integer, ``<= %d``" % option.type.max
                else:
                    option_type = "Integer"
            elif isinstance(option.type, types.Float):
                if option.type.min and option.type.max:
                    option_type = "Float, ``>= %.2f``, <= ``%.2f``" % (option.type.min, option.type.max)
                elif option.type.min:
                    option_type = "Float, ``>= %.2f``" % option.type.min
                elif option.type.max:
                    option_type = "Float, ``<= %.2f``" % option.type.max
                else:
                    option_type = "Float"
            elif isinstance(option.type, types.String):
                option_type = "String"
            elif isinstance(option.type, types.URI):
                option_type = "URI"
            elif isinstance(option.type, types.IPAddress):
                option_type = "IP address"
            elif isinstance(option.type, types.HostAddress):
                option_type = "Host address"

            else:
                option_type = "Unknown"

            option_types[option.name] = option_type

        fp = open(f"/output/{SERVICE}-{name}.rst", "w+")
        template_data = {
            "name": name,
            "options": sorted(options, key=attrgetter('name')),
            "types": option_types
        }
        fp.write(template.render(template_data))

    # :param name: the option's name
    # :param type: the option's type. Must be a callable object that takes string
    #              and returns converted and validated value
    # :param dest: the name of the corresponding :class:`.ConfigOpts` property
    # :param short: a single character CLI option name
    # :param default: the default value of the option
    # :param positional: True if the option is a positional CLI argument
    # :param metavar: the option argument to show in --help
    # :param help: an explanation of how the option is used
    # :param secret: true if the value should be obfuscated in log output
    # :param required: true if a value must be supplied for this option
    # :param deprecated_name: deprecated name option.  Acts like an alias
    # :param deprecated_group: the group containing a deprecated alias
    # :param deprecated_opts: list of :class:`.DeprecatedOpt`
    # :param sample_default: a default string for sample config files
    # :param deprecated_for_removal: indicates whether this opt is planned for
    #                                removal in a future release
    # :param deprecated_reason: indicates why this opt is planned for removal in
    #                           a future release. Silently ignored if
    #                           deprecated_for_removal is False
    # :param deprecated_since: indicates which release this opt was deprecated
    #                          in. Accepts any string, though valid version
    #                          strings are encouraged. Silently ignored if
    #                          deprecated_for_removal is False
    # :param mutable: True if this option may be reloaded
    # :param advanced: a bool True/False value if this option has advanced usage
    #                          and is not normally used by the majority of users
