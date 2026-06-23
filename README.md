
```
 _____         _  _                     _    _     
|  ___|       (_)| |                   | |  | |    
| |__  __   __ _ | |  ___   __ _  _ __ | |_ | |__  
|  __| \ \ / /| || | / _ \ / _` || '__|| __|| '_ \ 
| |___  \ V / | || ||  __/| (_| || |   | |_ | | | |
\____/   \_/  |_||_| \___| \__,_||_|    \__||_| |_|
                                                   
                                                   

```
## 安装

```bash
pip install PyQt5

```

## 运行

```bash

python Picturebinding.py

```

## 核心 

1. **加密嵌入阶段**  
   - 读取 Shellcode 二进制数据。  
   - 使用用户指定的 XOR 密钥（循环）对数据进行异或加密。  
   - 将加密后的数据与固定标记（如 `[PNGDATA]:`）拼接。  
   - 将拼接后的数据追加到原始 PNG 文件的末尾，保存为新的 PNG 文件（覆盖原文件）。

2. **提取执行阶段**  
   - 读取 PNG 文件的全部二进制数据。  
   - 在数据中搜索标记字符串的位置。  
   - 提取标记之后的所有数据（即加密的 Shellcode）。  
   - 使用相同的 XOR 密钥解密得到原始 Shellcode。  
   - 调用 Windows API（`VirtualAlloc`、`memmove`、`CreateThread`）在内存中分配可执行空间并执行。

## 运行效果  

<img width="798" height="491" alt="屏幕截图 2026-06-23 113434" src="https://github.com/user-attachments/assets/f48be5b2-6dec-4565-88c5-be0bfec7adbc" />




