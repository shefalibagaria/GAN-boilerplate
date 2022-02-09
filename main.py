import argparse
import os
import tifffile
import pytest
from src import train, networks, util
from config import Config
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def main(mode, offline, tag):
    """[summary]

    :param mode: [description]
    :type mode: [type]
    :param offline: [description]
    :type offline: [type]
    :param tag: [description]
    :type tag: [type]
    :raises ValueError: [description]
    """
    print("Running in {} mode, tagged {}, offline {}".format(mode, tag, offline))
    util.initialise_folders(tag)

    # Initialise Config object
    c = Config(tag)

    if mode == 'train':
        net = networks.make_nets(c)
        train(c, net, offline=offline)

    elif mode == 'generate':
        netD, netG = networks.make_nets(c, Training=0)
        net_g = netG()
        util.generate(c, net_g)
        print("Img generated")

    elif mode == 'test':
        print('Performing unit tests')
        pt = pytest.main(["-x", "src/test.py"])

    else:
        raise ValueError("Mode not recognised")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode")
    parser.add_argument("-t", "--tag")
    parser.add_argument('-o', '--offline', action='store_true',
                        help='disable wandb')
    args = parser.parse_args()
    if args.tag:
        tag = args.tag
    else:
        tag = 'test'

    main(args.mode, args.offline, tag)
# main('train', False, 'test')