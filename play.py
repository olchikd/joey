import os
import sys
import logging

from joey.trainer.declaration import Declaration
from joey.trainer.model import Model
from joey.trainer.filereaders.factory import FileReaderFactory
from joey.utils import init_logger
from joey.trainer.loader import store_model

DONE = 0
INVALID_DECLARATION = 1
TRAINING_ERROR = 2
TRAINING_DATA_ERROR = 3

logger = init_logger()


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)

    logger.info("Loading json file with model declaration")
    try:
        with open(args.path, 'r') as fp:
            data = fp.read()
        declaration = Declaration(data)
    except IOError, exc:
        logger.error("Can't load model declaration JSON file. {0!s}".format(exc))
        return INVALID_DECLARATION
    except Exception, exc:
        logger.error('Errors in model declaration JSON: {0!s}'.format(exc))
        raise
        return INVALID_DECLARATION

    try:
        model = Model(declaration)

        if args.dataset is None:
            logger.error("Specify data used for training")
            return TRAINING_DATA_ERROR

        logger.info('Reading input dataset')
        file_format = args.dataset_format or 'json'
        reader = FileReaderFactory.factory(file_format)
        with open(args.dataset, 'r') as fp:
            logger.info('Train the model')
            model.train(reader.get_reader(fp))

        if args.output is not None:
            logger.info('Saving model to file')
            with open(args.output, 'w') as model_fp:
                store_model(model, model_fp)
    except Exception as e:
        logger.info('Error occurred while training: {0}'.format(e.message))
        raise
        return TRAINING_ERROR

    return DONE


def create_parser():
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        description=__import__('__main__').__doc__,
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        '-o', '--output', dest='output',
        help='store trained model to the given file.',
        metavar='output')
    parser.add_argument(
        '-d', '--dataset', dest='dataset',
        help='training dataset.',
        metavar='dataset')
    parser.add_argument(
        '-f', '--format', dest='dataset_format',
        help='dataset format (json, csv).',
        metavar='dataset_format')
    parser.add_argument(
        dest='path',
        help='model declaration',
        metavar='path')
    return parser


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.error('keybord interrupt')
