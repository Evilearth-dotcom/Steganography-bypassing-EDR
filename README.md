
```
   ___    _        __                     __    _            __   _              
  / _ \  (_) ____ / /_ __ __  ____ ___   / /   (_)  ___  ___/ /  (_)  ___   ___ _
 / ___/ / / / __// __// // / / __// -_) / _ \ / /  / _ \/ _  /  / /  / _ \ / _ `/
/_/    /_/  \__/ \__/ \_,_/ /_/   \__/ /_.__//_/  /_//_/\_,_/  /_/  /_//_/ \_, / 
                                                                          /___/
[Version： 1.0]

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

3. **联系**
   - Session：054b4fc8d298d5e28d6b5f9e449da38734d92b90915c418ddddb18bed7d5a7015f
     
  
   



## 安装

```bash
https://github.com/Evilearth-dotcom/Steganography-bypassing-EDR.git
```

```bash
cd Steganography-bypassing-EDR
```

```bash
pip install PyQt5
```

## 运行

```bash
python Picturebinding.py
```



## 运行效果  

<img width="798" height="491" alt="屏幕截图 2026-06-23 113434" src="https://github.com/user-attachments/assets/f48be5b2-6dec-4565-88c5-be0bfec7adbc" />




