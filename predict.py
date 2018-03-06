import sys

from joey.utils import init_logger
from joey.trainer.loader import load_model
from joey.trainer.filereaders.factory import FileReaderFactory

DONE = 0
PREDICTION_ERROR = 1
INVALID_MODEL_ERROR = 2

logger = init_logger()


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)
    
    try:
        with open(args.path, 'r') as fp:
            model = load_model(fp)
    except IOError as exc:
        logger.warn('Invalid trainer file: {0!s}'.format(exc))
        return INVALID_MODEL_ERROR

    try:
        logger.info('Reading data')
        file_format = args.dataset_format or 'json'
        reader = FileReaderFactory.factory(file_format)
        with open(args.dataset, 'r') as fp:
            result = model.predict(reader.get_reader(fp))
        for name, val in result.iteritems(): 
            logger.info("{0} = {1}".format(name, val))
    except Exception as e:
        raise
        logger.info('Error occurred during prediction: %s', e.message)
        return PREDICTION_ERROR

    return DONE


def create_parser():
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        description=__import__('__main__').__doc__,
        formatter_class=RawDescriptionHelpFormatter)
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
        help='trained model',
        metavar='path')
    return parser


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warn('keyboard interrupt')
