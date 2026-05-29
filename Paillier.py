import random
from math import gcd
from sympy import mod_inverse

# Paillier类：密钥生成、加密与解密
class Paillier:
    def __init__(self, bitLength=256, certainty=64):
        self.bitLength = bitLength
        self.KeyGen(bitLength, certainty)

    def KeyGen(self, bitLengthVal, certainty):
        # 随机构造两个大素数p与q
        p = self._generate_prime(bitLengthVal // 2, certainty)
        q = self._generate_prime(bitLengthVal // 2, certainty)

        # n = p * q
        self.n = p * q
        # n_square = n * n
        self.n_square = self.n * self.n
        self.lambda_ = self._lcm(p - 1, q - 1)

        # 随机选择 g ∈ Z*_{n^2}
        while True:
            self.g = random.randint(1, self.n_square - 1)
            if gcd(self.g, self.n_square) == 1:
                break

    # 生成大素数
    def _generate_prime(self, bitLength, certainty):
        prime = 0
        while True:
            prime = random.getrandbits(bitLength)
            if self._is_prime(prime, certainty):
                return prime

    # 判断是否为素数
    def _is_prime(self, n, certainty):
        if n <= 1:
            return False
        for _ in range(certainty):
            a = random.randint(2, n - 1)
            if pow(a, n - 1, n) != 1:
                return False
        return True

    # 计算最小公倍数
    def _lcm(self, a, b):
        return a * b // gcd(a, b)

    # 加密函数：给定消息m和随机数r加密
    def Encrypt(self, m, r=None):
        if r is None:
            r = random.randint(1, self.n - 1)  # 随机选择r
        return pow(self.g, m, self.n_square) * pow(r, self.n, self.n_square) % self.n_square

    # 解密函数
    def Decrypt(self, c):
        u = (pow(self.g, self.lambda_, self.n_square) - 1) // self.n % self.n
        return (pow(c, self.lambda_, self.n_square) - 1) // self.n * mod_inverse(u, self.n) % self.n


# 主程序
if __name__ == "__main__":
    # 创建 Paillier 对象，生成密钥
    paillier = Paillier()

    # 输入两个明文 m1 和 m2
    m1 = int(input("请输入第一个明文："))
    m2 = int(input("请输入第二个明文："))

    # 加密 m1 和 m2
    em1 = paillier.Encrypt(m1)
    em2 = paillier.Encrypt(m2)

    # 输出加密结果
    print(f"对第一个明文的加密得到密文：{em1}")
    print(f"对第二个明文的加密得到密文：{em2}")

    # 解密加密结果
    dm1 = paillier.Decrypt(em1)
    dm2 = paillier.Decrypt(em2)

    # 输出解密结果
    print(f"第一个加密结果解密后的明文：{dm1}")
    print(f"第二个加密结果解密后的明文：{dm2}")

    # 密文相乘并解密
    product_ciphertext = (em1 * em2) % paillier.n_square
    print(f"两密文相乘得到：{product_ciphertext}")  # 输出密文相乘的结果
    decrypted_product = paillier.Decrypt(product_ciphertext)
    print(f"密文相乘后解密得到的明文：{decrypted_product}")
