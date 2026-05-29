from Paillier import Paillier
import gmpy2
import random
import time

# 程序说明
print("*****************此程序模拟了基于Paillier算法的匿名电子投票的流程：***************************")
print(
    "每位投票者为候选人投票并将结果加密发送给计票人。每人只有1张选票，选票上被投票的候选者得到1张选票，其他候选者得到0张选票：")
print("然后计票人将所有选票上对应候选人的加密的投票结果相乘，并将加密的统计结果发送给公布人")
print("最后公布人对统计的票数进行解密并公布；")
print("————————————————————————————————————————")


class ElectronicVoting:
    def __init__(self, num_voters, num_candidates, bitLength=256, certainty=64):
        self.num_voters = num_voters  # 投票者数量
        self.num_candidates = num_candidates  # 候选人数量
        self.paillier = Paillier(bitLength, certainty)  # 创建 Paillier 对象，生成公私钥
        self.votes = []
        self.candidates = [f"候选人{i + 1}" for i in range(num_candidates)]  # 创建候选人列表

    def cast_vote(self, voter_id):
        """
        模拟投票者对候选项的选择
        voter_id: 投票者的 ID
        """
        print(f"-----------请第 {voter_id + 1} 名投票者为候选人投票-----------")
        print(f"候选人列表：{', '.join(self.candidates)}")

        # 初始化该投票者的投票（为每个候选人投票）
        vote = []
        for i in range(self.num_candidates):
            candidate_vote = int(input(f"请为第{i + 1}名候选者投票（1为投票，0为不投票）："))
            if candidate_vote not in [0, 1]:
                raise ValueError("无效投票，必须选择 1 或 0")
            vote.append(candidate_vote)

        # 检查是否只有一个候选人被选中（即只有一个1）
        if vote.count(1) != 1:
            raise ValueError("每个投票者只能为一个候选人投票，不能为多个候选人投票！")

        # 对每个候选人的投票结果进行加密
        encrypted_vote = [self.paillier.Encrypt(v) for v in vote]
        self.votes.append(encrypted_vote)  # 将加密后的投票保存
        print("------------------------------------------------")

    def count_votes(self):
        """
        计票函数，计算每个候选人获得的票数并返回最终结果
        """
        encrypted_results = [1] * self.num_candidates  # 初始化每个候选人的密文结果为 1

        # 对每个投票者的密文投票进行乘法
        for encrypted_vote in self.votes:
            for i in range(self.num_candidates):
                encrypted_results[i] = (encrypted_results[i] * encrypted_vote[i]) % self.paillier.n_square

        return encrypted_results

    def decrypt_and_publish_result(self, encrypted_results):
        """
        计票人对加密结果进行解密，并公布每个候选人最终的票数
        """
        print("\n-----------计票人完成计票并将加密后的投票结果发送给公布人-----------")
        decrypted_results = [self.paillier.Decrypt(result) for result in encrypted_results]

        # 输出每个候选人获得的票数
        print("加密后的投票结果为：")
        for i in range(self.num_candidates):
            print(f"第 {i + 1} 名候选人获得的选票数的加密结果为：{encrypted_results[i]}")
        print("\n-----------公布人完成解密并公布最终的投票结果-----------")
        print("\n解密后的投票结果：")
        for i in range(self.num_candidates):
            print(f"第 {i + 1} 名候选人获得了 {decrypted_results[i]} 张选票")
        print("------------------------------------------------")


if __name__ == "__main__":
    print("********** 电子投票系统 **********")
    # 设置候选者数量和投票者数量
    num_candidates = int(input("请设置候选者人数："))
    num_voters = int(input("请设置投票者人数："))

    # 创建电子投票系统
    voting_system = ElectronicVoting(num_voters=num_voters, num_candidates=num_candidates)

    # 投票过程
    for voter_id in range(num_voters):
        try:
            voting_system.cast_vote(voter_id)  # 每个投票者进行投票
        except ValueError as e:
            print(e)
            break

    # 计票
    encrypted_results = voting_system.count_votes()  # 得到每个候选人的加密票数

    # 计票并公布结果
    voting_system.decrypt_and_publish_result(encrypted_results)
