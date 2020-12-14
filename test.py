import torch
import argparse
from model import *
from dataset.data import CiFar10Dataset,DataPreProcess
from mmcv import Config
from torch.utils.data import DataLoader
from log.logger import Logger

log = Logger('./log/InceptionV4_testlog.txt',level='info')

def parser():
    parser = argparse.ArgumentParser(description='PyTorch CIFAR10 Testing')
    parser.add_argument('--config', '-c', default='./config/config.py', help='config file path')
    args = parser.parse_args()
    return args

def dataLoad (cfg):
    test_data = CiFar10Dataset(txt = cfg.PARA.data.test_data_txt, transform='for_test')
    test_loader = DataLoader(dataset=test_data, batch_size=cfg.PARA.test.BATCH_SIZE, drop_last=True, shuffle=False, num_workers= cfg.PARA.train.num_workers)
    return test_loader

def test(test_loader):
    log.logger.info("==> Waiting Test <==")
    with torch.no_grad():
        correct = 0
        total = 0
        net.eval()
        for i, data in enumerate(test_loader, 0):
            images, labels = data
            images = images.cuda()
            labels = labels.cuda()
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum()
        log.logger.info('测试分类准确率为：%.3f%%' % (100 * correct / total))

def main():
    args = parser()
    cfg = Config.fromfile(args.config)
    log.logger.info('==> Preparing data <==')
    test_loader = dataLoad(cfg)
    log.logger.info('==> Loading model <==')
    global net
    #net = vgg19().cuda()
    net = inceptionv4().cuda()
    #net = squeezenet().cuda()
    #net = ResNet50().cuda()
    net = torch.nn.DataParallel(net, device_ids=cfg.PARA.train.device_ids)
    #checkpoint = torch.load('./checkpoint/squeezenet/134ckpt.pth')
    #checkpoint = torch.load('./checkpoint/ResNet/134ckpt.pth')
    checkpoint = torch.load('./checkpoint/InceptionV4/134ckpt.pth')
    net.load_state_dict(checkpoint['net'])
    test(test_loader)

if __name__ == '__main__':
    main()
