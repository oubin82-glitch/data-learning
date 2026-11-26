# =====================================================================
# 第 1 周参考答案
# 先自己做完 第1周练习.py 再看。写法不唯一，结果对得上就行。
# =====================================================================

from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "模拟宴席明细.xlsx"


def show(题号, 答案):
    if 答案 is None:
        print(f"[{题号}] 还没写")
    else:
        print(f"[{题号}] {答案}")


# ===== 第 1 天：变量 =====
print("\n===== 第 1 天：变量 =====")

brand = "特曲"
zhuoshu = 28
chuhuo = 84
kaiping = 39
show("1.1", (brand, zhuoshu, chuhuo, kaiping))

kaiping_rate = round(kaiping / chuhuo, 2)
show("1.2", kaiping_rate)

show("1.3", round(chuhuo / zhuoshu, 1))

show("1.4", f"{brand}宴席 {zhuoshu} 桌，出货 {chuhuo} 瓶，开瓶 {kaiping} 瓶，开瓶率 {kaiping / chuhuo:.0%}")

kaiping = 84
show("1.5", round(kaiping / chuhuo, 2))  # 1.0，全部开完


# ===== 第 2 天：列表 + for 循环 =====
print("\n===== 第 2 天：列表 + for 循环 =====")

桌数列表 = [17, 28, 16, 12, 15, 12, 6, 35]
开瓶列表 = [22, 39, 0, 9, 28, 11, 9, 26]

show("2.1", len(桌数列表))
show("2.2", (sum(桌数列表), max(桌数列表), min(桌数列表)))
show("2.3", round(sum(桌数列表) / len(桌数列表), 1))

count = 0
for k in 开瓶列表:
    if k == 0:
        count += 1
show("2.4", count)

每桌开瓶 = []
for z, k in zip(桌数列表, 开瓶列表):
    每桌开瓶.append(round(k / z, 1))
show("2.5", 每桌开瓶)

桌数列表.append(20)
开瓶列表.append(18)
show("2.6", sum(桌数列表))


# ===== 第 3 天：字典 =====
print("\n===== 第 3 天：字典 =====")

宴席 = {
    "活动名称": "0621孙静朋友聚会",
    "品牌": "大成",
    "宴席类型": "朋友聚会",
    "片区": "上海片区",
    "荐酒员": "韩华",
    "桌数": 15,
    "出货": 30,
    "开瓶": 28,
}

show("3.1", (宴席["荐酒员"], 宴席["片区"]))

宴席["开瓶率"] = round(宴席["开瓶"] / 宴席["出货"], 2)
show("3.2", 宴席)

品牌列表 = ["窖龄", "特曲", "大成", "国窖", "大成", "大成"]
计数 = {}
for b in 品牌列表:
    if b in 计数:
        计数[b] += 1
    else:
        计数[b] = 1
show("3.3", 计数)

小表 = [
    {"荐酒员": "冯霞", "品牌": "窖龄", "开瓶": 22},
    {"荐酒员": "唐秀超", "品牌": "特曲", "开瓶": 39},
    {"荐酒员": "韩华", "品牌": "大成", "开瓶": 28},
]
total = 0
for row in 小表:
    total += row["开瓶"]
show("3.4", total)

名单 = []
for row in 小表:
    if row["品牌"] in ("大成", "窖龄"):
        名单.append(row["荐酒员"])
show("3.5", 名单)


# ===== 第 4 天：pandas 读表 =====
print("\n===== 第 4 天：pandas 读表 =====")

import pandas as pd

df = pd.read_excel(DATA)

show("4.1", df.shape)
show("4.2", list(df.columns))
show("4.3", "\n" + df.head(3).to_string())
show("4.4", "\n" + df.dtypes.to_string())
# 电话存成数字：开头的 0 会丢、不能做加减却会被当成数值、describe 里还会被统计。
# 读表时可以写 pd.read_excel(DATA, dtype={"荐酒员电话": str})
show("4.5", "\n" + df["品牌"].value_counts().to_string())
show("4.6", "\n" + df.describe().to_string())
# 出货最小值是 0：有的宴席状态是"异常结束"或"新建"，没出货，后面清洗时要单独处理。


# ===== 第 5 天：业务问题 =====
print("\n===== 第 5 天：业务问题 =====")

col = "受益对象所属销售片区"
show("5.1", (df[col].nunique(), list(df[col].unique())))

总桌数 = df["实际宴席桌数"].sum()
总出货 = df["终端出货数量(瓶)"].sum()
总开瓶 = df["消费者开瓶(瓶)"].sum()
show("5.2", (int(总桌数), int(总出货), int(总开瓶)))

show("5.3", round(总开瓶 / 总出货, 3))

show("5.4", "\n" + df["活动状态"].value_counts().to_string())

t = pd.to_datetime(df["开始时间"])
show("5.5", (str(t.min()), str(t.max())))

show("5.6", df["宴席类型"].value_counts().idxmax())

show("5.7", "同一个店名（比如顺发烟酒店）对应多个编码，是不同地方的不同门店。"
            "按名称汇总会把几家店的数据混在一起，所以终端要按编码汇总，名称只用来显示。")

print("   荐酒员人数：", df["受益荐酒员"].nunique(), " 电话个数：", df["荐酒员电话"].nunique())
show("5.8", "有同名不同人（两个人都叫一个名字），或者同一个人换过号码。"
            "按电话分组更准；也可以按 名字+电话 一起分组，再人工核对那几个对不上的。")


# ===== 第 5 天：找错 =====
print("\n===== 第 5 天：找错 =====")

show("5.9", f"分子分母写反了，开瓶率应该是 开瓶÷出货：{round(总开瓶 / 总出货, 3)}"
            f"（AI 写的算出来是 {round(总出货 / 总开瓶, 3)}，开瓶率不可能大于 1，一看就不对）")

show("5.10", f"除数错了：nunique() 是品牌个数 4，应该除以场次 len(df)，"
             f"或者直接用 .mean()：{round(df['实际宴席桌数'].mean(), 2)}")

show("5.11", f"表里的值是“上海片区”，不是“上海”，== 要求完全相等。"
             f"改成 == '上海片区' 或 .str.contains('上海')：{(df[col] == '上海片区').sum()}")

print("\n第 1 周答案结束。")
