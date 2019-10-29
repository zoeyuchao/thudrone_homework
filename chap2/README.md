# Chapter2_QR Code

## 1. 二维码识别问题

1. 需定位二维码，并将二维码从原始图片中裁剪出来
2. 可调用 `pyzbar` 库对裁剪后的图片进行二维码解码

## 2. 文件说明

- `C++/`：C++版本代码
- `imgs/`：待识别的二维码图片应放在该文件夹下
- `QR_code_q.py`：试题
- `QR_code.py`：答案

## 3. 运行方法

命令行

```shell
python QR_code.py
```

## 4. 常见问题

1. 对二维码定位角的判断应放松阈值要求，否则会漏掉部分二维码
2. waiting ...