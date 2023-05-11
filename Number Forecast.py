import random

print("数当てゲームを始めます")
print("答えの数の範囲は1~100です")

answer = random.randrange(start=1, stop=100)
guess = int(input("予想する数字を入れてください："))
print(guess)
tries = 1

while(guess != answer):
  if(guess > answer):
    print("あなたの予想した数は答えより大きいです")
  else:
    print("あなたの予想した数は答えより小さいです")
  tries = tries + 1
  guess = int(input("予想する数字を入れてください："))
print("正解です。答えは{}".format(answer))
print("あなたの試行回数は{}回でした".format(tries))