import pandas as pd


class Account:
    __interest_rate = 0.0001

    def __init__(self, owner, amount):
        self.__amount = amount
        self.owner = owner

    def __get_info(self):
        return "user {} amount {} rate {}".format(self.owner, self.__amount, Account.__interest_rate)

    def desc(self):
        print(self.__get_info())


if __name__ == '__main__':
    ant = Account("小明", 5000)
    ant.desc()

    print("name {0} age {1}".format("小明", 2))

    print("name {1} age {0}".format("小明", 2))

pad = pd.DataFrame({
    "close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

dd = pad["close"].shift(1)
print(dd)

pad["tmp1"] = pad["close"].shift(1)
pad["tmp2"] = pad["close"].shift(2)
pad["tmp3"] = pad["close"].shift(3)
pad["tmp4"] = pad["close"].shift(4)
pad["tmp5"] = pad["close"].shift(5)
pad["avg"] = (pad["tmp1"] + pad["tmp2"] + pad["tmp3"] + pad["tmp4"] + pad["tmp5"]) / 5

# pad = pad.fillna(-1)
pad["avg"] = pad["avg"].fillna(-1)
print(pad.info())
pad["tmp1"].astype(dtype=int)
a = 1
b = 2

print(a)
print(b)
print("-------------")
print("a : " + str(a))
print("b : " + str(b))
