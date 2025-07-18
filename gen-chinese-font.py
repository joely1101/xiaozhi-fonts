import opencc
from pprint import pprint
import os
import glob

# 設定絕對路徑
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'word.txt')
output_path = os.path.join(script_dir, 'output.txt')

# 初始化轉換器
s2t = opencc.OpenCC('s2t')
t2s = opencc.OpenCC('t2s')

# 讀取檔案內容
content=""
for filepath in glob.glob("words/*.txt"):
    with open(filepath, 'r', encoding='utf-8') as file:
        content += file.read()

# 字元分類
simplified = []
traditional = []
symbols = []
allchar=[]

for char in content:
    allchar.append(char)
    if '\u4e00' <= char <= '\u9fff':  # 中文字符範圍
        # 繁體檢測
        t_to_s = t2s.convert(char)
        if t_to_s == char:  # 原本就是簡體
            simplified.append(char)
        else:  # 繁體字
            traditional.append(char)
    else:
        symbols.append(char)

# 轉換與合併流程
# 簡轉繁並合併去重
converted_trad = [s2t.convert(c) for c in simplified]
combined_trad = list(set(traditional + converted_trad))

# 繁轉簡生成最終列表
final_simp = [t2s.convert(c) for c in combined_trad]

# 建立對照表 (排除相同項)
conversion_table = []
same_table = []
for s, t in zip(final_simp, combined_trad):
    if s != t:
        conversion_table.append((s, t))
    else:
        same_table.append((s, t))

# 排序對照表
conversion_table.sort(key=lambda x: x[0])

# 輸出結果
print(f"原始檔案字數統計:")
print(f"檔案字數: {len(allchar)} 個")
print(f"簡體字: {len(simplified)} 個")
print(f"繁體字: {len(traditional)} 個")
print(f"簡體字: all {len(final_simp)} 個")
print(f"繁體字: all {len(combined_trad)} 個")
print(f"共用字: {len(same_table)} 個")
print(f"符號: {len(symbols)} 個")
print(f"\n生成簡繁對照表共 {len(conversion_table)} 組")

# 寫入檔案
with open("final_words.txt", 'w', encoding='utf-8') as f:
    #combined_allwords = list(set(symbols + final_simp + combined_trad))
    combined_allwords = list(set(symbols + final_simp + combined_trad))
    f.write("".join(combined_allwords))

with open("src/s2t_table.h", 'w', encoding='utf-8') as cfile:
    cfile.write("static const ZhMap zh_s2t_table[] = {\n")
    for s, t in conversion_table:
        cfile.write(f'{{"{s}","{t}"}},\n')
    cfile.write("};")
print(f"\n結果已輸出至: src/s2t_table.h final_words.txt")
