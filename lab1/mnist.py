# BSD 3-Clause License



# Copyright (c) 2017, 

# All rights reserved.



# Redistribution and use in source and binary forms, with or without

# modification, are permitted provided that the following conditions are met:



# * Redistributions of source code must retain the above copyright notice, this

#   list of conditions and the following disclaimer.



# * Redistributions in binary form must reproduce the above copyright notice,

#   this list of conditions and the following disclaimer in the documentation

#   and/or other materials provided with the distribution.



# * Neither the name of the copyright holder nor the names of its

#   contributors may be used to endorse or promote products derived from

#   this software without specific prior written permission.



# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"

# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE

# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE

# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE

# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL

# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR

# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER

# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,

# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE

# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



from __future__ import print_function

import argparse

import torch

import torch.nn as nn

import torch.nn.functional as F

import torch.optim as optim

import torchvision

from torchvision import datasets, transforms

from torch.optim.lr_scheduler import StepLR



import numpy as np

import torchvision.models as models

from torch.utils.tensorboard import SummaryWriter

# default `log_dir` is "logs" - we'll be more specific here

# 记得改！！！！format为ibatch size的大小

writer = SummaryWriter('logs/mnist_experiment_20epoch_{}bs'.format(1))



class Net(nn.Module):

    def __init__(self):

        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 32, 3, 1)

        self.conv2 = nn.Conv2d(32, 64, 3, 1)

        # Dropout2d是对每个通道有p的概率进行dropout

        # Dropout则是对于单个元素有p的概率进行dropout

        self.dropout1 = nn.Dropout2d(0.25)

        self.dropout2 = nn.Dropout2d(0.5)

        self.fc1 = nn.Linear(9216, 128)

        self.fc2 = nn.Linear(128, 10)



    def forward(self, x):

        x = self.conv1(x)

        x = F.relu(x)

        x = self.conv2(x)

        x = F.relu(x)

        x = F.max_pool2d(x, 2)

        x = self.dropout1(x)

        # flatten: 将从维数为1到最后的flat一下

        x = torch.flatten(x, 1)

        x = self.fc1(x)

        x = F.relu(x)

        x = self.dropout2(x)

        x = self.fc2(x)

        # log_softmax: 防止上溢出和下溢出，数太接近0或1，float无法表示

        output = F.log_softmax(x, dim=1)

        return output





def train(args, model, device, train_loader, optimizer, epoch):

    '''

    如果模型中有BN层(Batch Normalization）和Dropout，需要在训练时添加model.train()。

    model.train()作用：对BN层，保证BN层能够用到每一批数据的均值和方差，并进行计算更新；

    对于Dropout，model.train()是随机取一部分网络连接来训练更新参数。

    '''

    model.train()

    # initialize the running loss for visualization

    running_loss = 0.0

    correct = 0.0



    for batch_idx, (data, target) in enumerate(train_loader):

        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()

        # Net(data)相当于forward

        output = model(data)

        # 把target label的取log_softmax之后的结果取出来，取负号后求均值

        loss = F.nll_loss(output, target)

        loss.backward()

        # 优化器更新所有参数

        optimizer.step()



        # calculate training loss and accuracy

        running_loss += loss.item()

        pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability

        correct += pred.eq(target.view_as(pred)).sum().item()



        if batch_idx % args.log_interval == 0:

            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(

                epoch, batch_idx * len(data), len(train_loader.dataset),

                100. * batch_idx / len(train_loader), loss.item()))



            # log the running loss and accuracy

            if batch_idx != 0:

                global_step = (epoch - 1) * len(train_loader) + batch_idx

                writer.add_scalar('Loss/train', running_loss / (args.batch_size * args.log_interval), global_step)

                writer.add_scalar('Accuracy/train', 100. * correct / (args.batch_size * args.log_interval), global_step)

            running_loss = 0.0

            correct = 0.0



def test(model, device, test_loader):

    '''

    如果模型中有BN层(Batch Normalization）和Dropout，在测试时添加model.eval()。

    model.eval()是保证BN层直接利用之前训练阶段得到的均值和方差，即测试过程中要保证BN层的均值和方差不变；

    对于Dropout，model.eval()是利用到了所有网络连接，即不进行随机舍弃神经元。

    '''

    model.eval()

    test_loss = 0

    correct = 0

    # 不传梯度

    with torch.no_grad():

        for data, target in test_loader:

            data, target = data.to(device), target.to(device)

            output = model(data)

            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss

            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability

            correct += pred.eq(target.view_as(pred)).sum().item()



    test_loss /= len(test_loader.dataset)



    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(

        test_loss, correct, len(test_loader.dataset),

        100. * correct / len(test_loader.dataset)))



def profile(model, device, train_loader): 

    data_iter = iter(train_loader)

    data, target = data_iter.next()

    data, target = data.to(device), target.to(device)

    with torch.autograd.profiler.profile(use_cuda =False) as prof: 

        model(data[0].reshape(1,1,28,28))

    print(prof.key_averages().table(sort_by='self_cpu_time_total', row_limit=10))



def main():

    # Training settings

    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')

    parser.add_argument('--batch-size', type=int, default=64, metavar='N',

                        help='input batch size for training (default: 64)')

    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',

                        help='input batch size for testing (default: 1000)')

    parser.add_argument('--epochs', type=int, default=20, metavar='N',

                        help='number of epochs to train (default: 14)')

    parser.add_argument('--lr', type=float, default=1.0, metavar='LR',

                        help='learning rate (default: 1.0)')

    parser.add_argument('--gamma', type=float, default=0.7, metavar='M',

                        help='Learning rate step gamma (default: 0.7)')

    parser.add_argument('--no-cuda', action='store_true', default=False,

                        help='disables CUDA training')

    parser.add_argument('--seed', type=int, default=1, metavar='S',

                        help='random seed (default: 1)')

    parser.add_argument('--log-interval', type=int, default=10, metavar='N',

                        help='how many batches to wait before logging training status')



    parser.add_argument('--save-model', action='store_true', default=True,

                        help='For Saving the current Model')

    args = parser.parse_args()

    use_cuda = not args.no_cuda and torch.cuda.is_available()



    torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")



    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    # 加载数据集

    train_loader = torch.utils.data.DataLoader(

        datasets.MNIST('../data', train=True, download=True,

                       transform=transforms.Compose([

                           transforms.ToTensor(),

                           transforms.Normalize((0.1307,), (0.3081,))

                       ])),

        batch_size=args.batch_size, shuffle=True, **kwargs)

    test_loader = torch.utils.data.DataLoader(

        datasets.MNIST('../data', train=False, transform=transforms.Compose([

                           transforms.ToTensor(),

                           transforms.Normalize((0.1307,), (0.3081,))

                       ])),

        batch_size=args.test_batch_size, shuffle=True, **kwargs)



    model = Net().to(device)

    # 使用Adadelta作为优化器

    optimizer = optim.Adadelta(model.parameters(), lr=args.lr)

    # 每次step，即每个epoch都调整学习率为*0.8

    scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)

    

    # profile model

    print("Start profiling...")

    profile(model, device, train_loader)

    print("Finished profiling.")



    #get some random traning images

    dataiter = iter(train_loader)

    images, labels = dataiter.next()



    # show batch images

    grid = torchvision.utils.make_grid(images)

    writer.add_image('images', grid, 0)



    model = Net().to(device)

    optimizer = optim.Adadelta(model.parameters(), lr=args.lr)



    # show model graph

    writer.add_graph(model, images)



    for epoch in range(1, args.epochs + 1):

        train(args, model, device, train_loader, optimizer, epoch)

        test(model, device, test_loader)

        scheduler.step()



    if args.save_model:

        torch.save(model.state_dict(), "mnist_cnn_{}.pt".format(args.batch_size))



    writer.close()



if __name__ == '__main__':

    main()
