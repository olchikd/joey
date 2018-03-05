import os
import sys
import logging

from joey.trainer.declaration import Declaration
from joey.trainer.model import Model
from joey.trainer.filereaders.factory import FileReaderFactory

DONE = 0
INVALID_DECLARATION = 1
TRAINING_ERROR = 2
TRAINING_DATA_ERROR = 3


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        with open(args.path, 'r') as fp:
            data = fp.read()
        declaration = Declaration(data)
    except IOError, exc:
        logging.error("Can't load model declaration JSON file. {0!s}".format(exc))
        return INVALID_DECLARATION
    except Exception, exc:
        logging.error('Errors in model declaration JSON: {0!s}'.format(exc))
        raise
        return INVALID_DECLARATION

    try:
        model = Model(declaration)

        if args.input is None:
            logging.error("Specify data used for training")
            return TRAINING_DATA_ERROR

        file_format = agrs.data_format or 'json'
        reader = FileReaderFactory.factory(file_format)
        with open(args.input, 'r') as fp:
            model.train(reader.get_reader(fp))
    except Exception as e:
        logging.info('Error occurred while training: {0}'.format(e.message))
        return TRAINING_ERROR

    return DONE


def create_parser():
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        description=__import__('__main__').__doc__,
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-o', '--output', dest='output',
                        help='store trained model to the given file.',
                        metavar='output')
    parser.add_argument('-i', '--input', dest='input',
                        help='read data for training from file.',
                        metavar='input-file')
    parser.add_argument(dest='path',
                        help='model declaration',
                        metavar='path')
    return parser


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logging.error('keybord interrupt')
