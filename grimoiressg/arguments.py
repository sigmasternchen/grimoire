import argparse


def parse_arguments_to_initial_context():
    parser = argparse.ArgumentParser(
        description='''
            Grimoire is a minimalistic Static Site Generator.
            In the simplest case the only argument needed is at least one content file. \
            The rest of the flags is used to customize the behavior.
        '''
    )
    parser.add_argument("content_file", nargs="+", help="one or more content files")
    parser.add_argument("-o", "--output", default="./output/", help="the output directory (default: ./output/)")
    parser.add_argument("-c", "--config", help="the config file to use")

    args, _ = parser.parse_known_args()

    context = {
        "output_dir": args.output,
        "config_file": args.config,
        "filenames": args.content_file
    }

    print(f"Output directory: {context['output_dir']}")
    print(f"Config file: {context['config_file']}")
    print("Content files:")
    for filename in context["filenames"]:
        print(f" - {filename}")
    print()

    return context
