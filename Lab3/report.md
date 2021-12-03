# Lab3

刘珈征

## report

### environment

|          |            |                         |
| -------- | ---------- | ----------------------- |
| hardware | CPU number | 6                       |
|          | GPU        | GeForce GTX 1080 Ti     |
| software | OS         | Ubuntu 18.04.2          |
|          | Structure  | Python 3.7.4 && Pytorch |
|          | CUDA       | V10.0.105               |

### result

运行profile结果CPU版本好一些，具体运行时间上CUDA版更快

CPU：27.051mx

GPU：345.028ms

GPU版本的cudnn_convolution占据了96.18%的CPU

|           | 运行时间（min） |
| --------- | --------------- |
| 实现方式  | 性能评测        |
| CPU only  | 39：00          |
| With CUDA | 11：52          |

