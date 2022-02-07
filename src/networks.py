import torch
import torch.nn as nn
import torch.nn.functional as F
import pickle


def make_nets(config, training=True):
    """Creates Generator and Discriminator class objects from params either loaded from config object or params file.

    :param config: a Config class object 
    :type config: Config
    :param training: if training is True, params are loaded from Config object. If False, params are loaded from file, defaults to True
    :type training: bool, optional
    :return: Discriminator and Generator class objects
    :rtype: Discriminator, Generator
    """
    # save/load params
    if training:
        config.save()
    else:
        config.load()

    k, s, f, p = config.get_net_params()

    # Make nets
    # if config.net_type == 'gan':
    #     class Generator(nn.Module):
    #         def __init__(self):
    #             super(Generator, self).__init__()
    #             self.convs = nn.ModuleList()
    #             self.bns = nn.ModuleList()
    #             for lay, (k, s, p) in enumerate(zip(gk, gs, gp)):
    #                 self.convs.append(nn.ConvTranspose2d(
    #                     gf[lay], gf[lay+1], k, s, p, bias=False))
    #                 self.bns.append(nn.BatchNorm2d(gf[lay+1]))

    #         def forward(self, x):
    #             for conv, bn in zip(self.convs[:-1], self.bns[:-1]):
    #                 x = F.relu_(bn(conv(x)))
    #             out = torch.softmax(self.convs[-1](x), dim=1)
    #             return out  # bs x n x imsize x imsize x imsize

    #     class Discriminator(nn.Module):
    #         def __init__(self):
    #             super(Discriminator, self).__init__()
    #             self.convs = nn.ModuleList()
    #             for lay, (k, s, p) in enumerate(zip(dk, ds, dp)):
    #                 self.convs.append(
    #                     nn.Conv2d(df[lay], df[lay + 1], k, s, p, bias=False))

            # def forward(self, x):
            #     for conv in self.convs[:-1]:
            #         x = F.relu_(conv(x))
            #     x = self.convs[-1](x)  # bs x 1 x 1
            #     return x

    #     return Discriminator, Generator
    
    if config.net_type == 'cnn':
        class Net(nn.Module):           # allows nn.Module functions to be used in the class
            def __init__(self):
                super().__init__()
                self.convs = nn.ModuleList()
                for lay, (ker, str, pad) in enumerate(zip(k, s, p)):
                    self.convs.append(
                        nn.Conv2d(f[lay], f[lay+1], ker, str, pad)
                    )
                # self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
                # self.conv2 = nn.Conv2d(16, 16, 3, padding=1)
                # self.conv3 = nn.Conv2d(16, 16, 3, padding=1)
                # self.conv4 = nn.Conv2d(16, 3, 3, padding=1)

            def forward(self, x):
                # x = F.relu(self.conv1(x))
                # x = F.relu(self.conv2(x))
                # x = F.relu(self.conv3(x))
                # x = self.conv4(x)
                for conv in self.convs[:-1]:
                    x = F.relu_(conv(x))
                x = self.convs[-1](x)  # bs x 1 x 1
                return F.softmax(x, dim=1)
    return Net

