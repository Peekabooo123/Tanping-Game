# 安装 pykakasi
# pip install pykakasi

import pykakasi

# 初始化转换器
kks = pykakasi.kakasi() # "H" 表示平假名，"K" 表示片假名，"J" 表示汉字， "a" 表示转换为罗马字， "r" 设置罗马字系统（如 Hepburn）
kks.setMode("H", "a")  # 平假名 -> 罗马字
kks.setMode("K", "a")  # 片假名 -> 罗马字
kks.setMode("J", "a")  # 汉字 -> 罗马字
kks.setMode("r", "Hepburn")  # 使用 Hepburn 罗马字系统
kks.setMode("s", True)  # 保留空格
converter = kks.getConverter()

# 输入日文字符串
text   = "舗装された道路やコンクリートのビルが集まる都市は、大雨が降ると排水が追いつかなくなり「内水氾濫」が発生します。あふれた水は地下室や地下街に集まり被害が出る危険があります。短時間に一気に状況が悪化するのが特徴で、気象情報などを見て早めに危険を察知し、安全な場所へ避難することが大切です。"
result = converter.do(text)

print(result)  # watashi ha gakusei desu