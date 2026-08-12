"""
猜数字游戏
玩法：电脑随机生成 1-100 的数字，你来猜，看几次能猜中
运行: python guess_number.py
"""

import random

def main():
    print("\n===== 猜数字游戏 =====")
    print("我心里想了一个 1-100 之间的数字，你来猜猜看！\n")

    answer = random.randint(1, 100)
    tries = 0

    while True:
        try:
            guess = int(input("你的猜测: "))
        except ValueError:
            print("请输入一个数字！")
            continue

        tries += 1

        if guess < answer:
            print("小了，再大一点！")
        elif guess > answer:
            print("大了，再小一点！")
        else:
            print(f"\n恭喜你猜对了！答案是 {answer}，你用了 {tries} 次。")
            if tries <= 5:
                print("太强了！")
            elif tries <= 10:
                print("不错的成绩！")
            else:
                print("终于猜到了，下次加油～")
            break

if __name__ == '__main__':
    main()
