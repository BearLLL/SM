# SM3长度扩展攻击:hushed:
### Original：<br>
https://github.com/hjzin/SM3LengthExtensionAttack/blob/master/%E5%AE%9E%E9%AA%8C%E6%96%87%E6%A1%A3.md
### 一、攻击原理
        SM3的消息长度是64字节的整数倍，如果消息的长度不足需要进行填充。在填充时，首先填充一个“1”，之后填充“0”，直到消息长度为56+64k(k为整数)字节，最后8字节由消息的长度填充。
        SM3函数计算时，需要对消息进行分组，每组64字节，每次加密一组，并更新8个向量。用新的向量加密下一组。当得到第一次加密后的向量值时，人为构造消息用于下一次加密，可以在不知
    道消息的情况下得到合法的哈希值。
### 二、攻击过程
    1、随机生成一个消息（m），用sm3中的函数计算出hash值（hash1）。
    2.生成一个附加消息（m`），用hash1推算出加密结束后8个向量的值，再用它们去加密m`，得到hash值（hash2）。
    3.计算m + padding + m`的hash值（hash3），如果攻击成功，则有 hash2 = hash3。
### 三、攻击结果
  <div align=center>
  <img width="900" alt="pic11" src="https://user-images.githubusercontent.com/109841017/181906027-477e4ce6-33eb-48c6-b87a-6b7c28aae3b9.png">
  </div>
