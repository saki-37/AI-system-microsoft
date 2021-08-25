# Lab  1

Jiazheng Liu

## setup

I've already got my virtual machine ready. 

**Install Anaconda: **

download:

```
$ wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
$ bash Anaconda3-2020.02-Linux-x86_64.sh
```

activate: 

```
$ source ~/.bashrc
```

test: 

```
$ conda -V
conda 4.8.2
```

create and activate new environment: 

```
$ conda create -n #env_name python=3.7.6
$ conda activate #env_name
```

**Install gcc: **

```
$ sudo apt-get update
$ sudo apt-get install build-essential
```

**Install pytorch (version 1.5.0) :** 

CPU version: 

```
$ conda install pytorch==1.5.0 torchvision==0.6.0 cpuonly -c pytorch
```

GPU version (CUDA10.1) : 

```
$ conda install pytorch==1.5.0 torchvision==0.6.0 cudatoolkit=10.1 -c pytorch
```

**Install Visual Studio Code:**

download: https://code.visualstudio.com/Download

install: 

```
sudo dpkg -i #package name
```

module install: 

C/C++; Chinese (Simplified) Language Pack; Jupyter; Pylance; Python

Now we can open Visual Studio Code using anaconda-navigator and debug!

 

## report

### environment

|          |            |                         |
| -------- | ---------- | ----------------------- |
| hardware | CPU number | 4                       |
|          | GPU        | no physical GPU         |
| software | OS         | Ubuntu 20.04.2          |
|          | Structure  | Python 3.7.6 && Pytorch |
|          | CUDA       | no Nvidia GPU           |

CPU number: 4

```
$ lscpu
```

GPU: no physical GPU (VMware SVGA II Adater)

```
$ lspci | grep -i vga
00:0f.0 VGA compatible controller: VMware SVGA II Adapter
```

OS: Ubuntu 20.04.2

```
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 20.04.2 LTS
Release:	20.04
Codename:	focal
```

Structure: Pytorch

python: Python 3.7.6

```
$ python -V
```

CUDA: no Nvidia GPU



### result

#### network

![image-20210824102823097](/typora-user-images/image-20210824102823097.png)

unfold the network

<img src="/home/jia/.config/Typora/typora-user-images/image-20210824110109187.png" alt="image-20210824110109187"  />



#### epoch = 4, batch_size = 64

##### top ten ranging in total time spent on CPU (averages all function events with the same key)

![image-20210824103430894](/home/jia/.config/Typora/typora-user-images/image-20210824103430894.png)



##### accuracy

![image-20210824103850261](/home/jia/.config/Typora/typora-user-images/image-20210824103850261.png)

![image-20210824103910995](/home/jia/.config/Typora/typora-user-images/image-20210824103910995.png)

![image-20210824103947575](/home/jia/.config/Typora/typora-user-images/image-20210824103947575.png)

![image-20210824104011601](/home/jia/.config/Typora/typora-user-images/image-20210824104011601.png)

another run

![](/home/jia/.config/Typora/typora-user-images/image-20210824104316061.png)



![image-20210824105236917](/home/jia/.config/Typora/typora-user-images/image-20210824105236917.png)

##### the Accuracy and Loss during training (with smoothing = 0.6)

![image-20210824104416835](/home/jia/.config/Typora/typora-user-images/image-20210824104416835.png)



![image-20210824104437824](/home/jia/.config/Typora/typora-user-images/image-20210824104437824.png)



#### epoch = 14, batch size = 64

![image-20210824105139513](/home/jia/.config/Typora/typora-user-images/image-20210824105139513.png)



![image-20210824110915015](/home/jia/.config/Typora/typora-user-images/image-20210824110915015.png)

![image-20210824110933297](/home/jia/.config/Typora/typora-user-images/image-20210824110933297.png)

![image-20210824110949426](/home/jia/.config/Typora/typora-user-images/image-20210824110949426.png)

![image-20210824111005054](/home/jia/.config/Typora/typora-user-images/image-20210824111005054.png)

![image-20210824111019110](/home/jia/.config/Typora/typora-user-images/image-20210824111019110.png)

![image-20210824111036994](/home/jia/.config/Typora/typora-user-images/image-20210824111036994.png)

![image-20210824111048329](/home/jia/.config/Typora/typora-user-images/image-20210824111048329.png)

![image-20210824111100356](/home/jia/.config/Typora/typora-user-images/image-20210824111100356.png)

![image-20210824111118378](/home/jia/.config/Typora/typora-user-images/image-20210824111118378.png)

![image-20210824111131209](/home/jia/.config/Typora/typora-user-images/image-20210824111131209.png)

![image-20210824111144393](/home/jia/.config/Typora/typora-user-images/image-20210824111144393.png)



#### epoch = 20, batch size = 64

![image-20210824112806213](/home/jia/.config/Typora/typora-user-images/image-20210824112806213.png)



![image-20210824121416158](/home/jia/.config/Typora/typora-user-images/image-20210824121416158.png)

![image-20210824121433548](/home/jia/.config/Typora/typora-user-images/image-20210824121433548.png)

![image-20210824121447902](/home/jia/.config/Typora/typora-user-images/image-20210824121447902.png)

![image-20210824121500016](/home/jia/.config/Typora/typora-user-images/image-20210824121500016.png)

![image-20210824121200817](/home/jia/.config/Typora/typora-user-images/image-20210824121200817.png)



![image-20210824121226521](/home/jia/.config/Typora/typora-user-images/image-20210824121226521.png)





#### epoch = 20, batch size = 16

![image-20210824135629094](/home/jia/.config/Typora/typora-user-images/image-20210824135629094.png)



![image-20210824143843429](/home/jia/.config/Typora/typora-user-images/image-20210824143843429.png)

![image-20210824143902511](/home/jia/.config/Typora/typora-user-images/image-20210824143902511.png)

![image-20210824143922753](/home/jia/.config/Typora/typora-user-images/image-20210824143922753.png)

![image-20210824144132119](/home/jia/.config/Typora/typora-user-images/image-20210824144132119.png)



![image-20210824144202563](/home/jia/.config/Typora/typora-user-images/image-20210824144202563.png)



![image-20210824144218509](/home/jia/.config/Typora/typora-user-images/image-20210824144218509.png)



#### epoch = 20 batch size = 1 8h

![image-20210824145515431](/home/jia/.config/Typora/typora-user-images/image-20210824145515431.png)



![image-20210824225919639](/home/jia/.config/Typora/typora-user-images/image-20210824225919639.png)

![image-20210824232421525](/home/jia/.config/Typora/typora-user-images/image-20210824232421525.png)



![image-20210824232449615](/home/jia/.config/Typora/typora-user-images/image-20210824232449615.png)



![image-20210824232509687](/home/jia/.config/Typora/typora-user-images/image-20210824232509687.png)

#### batch size comparison

| epoch = 20          | batch size = 1 (grey)        | batch size = 16 (green) | batch size = 64 (red) |
| ------------------- | ---------------------------- | ----------------------- | --------------------- |
| training time       | much more slower (8 hours +) | slower                  | fatest                |
| final accuracy      | 98.61%                       | 98.57%                  | 99.13%                |
| Accuracy comparison | graph a                      | graph b                 |                       |
| Loss comparison     | graph c                      | graph d                 |                       |

graph a

![image-20210825100017631](/home/jia/.config/Typora/typora-user-images/image-20210825100017631.png)

graph b

![image-20210825100122931](/home/jia/.config/Typora/typora-user-images/image-20210825100122931.png)

graph c

![image-20210825100152991](/home/jia/.config/Typora/typora-user-images/image-20210825100152991.png)

graph d

![image-20210825100214128](/home/jia/.config/Typora/typora-user-images/image-20210825100214128.png)

#### Findings and Conclusions

1. Comparing batch size = 1, 16, 64, when we have larger batch size, the training speeds up; accuracy and loss changes are more stable,  and the update process might be more stable as well. 
2. The accuracy doesn't necessarily increase with the epoch. In fact, the accuracy already reaches 98.33% after epoch one. When the batch size = 64, epoch = 20, the accuracy reaches its best, 99.25%, in epoch 18. 

#### Reference

1. https://pytorch.org/docs/master/autograd.html
2. https://github.com/microsoft/AI-System/blob/main/Labs/Prerequisites.md
