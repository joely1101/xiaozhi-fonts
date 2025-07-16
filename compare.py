def compare_utf8_chars(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        str1 = f1.read()
        str2 = f2.read()
    count=0
    datalist=[]
    max_len = max(len(str1), len(str2))
    for i in range(max_len):
        ch1 = str1[i] if i < len(str1) else '[EOF]'
        ch2 = str2[i] if i < len(str2) else '[EOF]'
        if ch1 != ch2:
            #print(f'Index {i}: "{ch1}" != "{ch2}"')
            data=(ch1, ch2)
            datalist.append(data)
            count=count+1
    print(f"diff counter={count}")
    with open('diff.txt', 'w', encoding='utf-8') as f:
        for simp, trad in datalist:
            f.write(f'{{"{simp}","{trad}"}},\n')
    
    X_sorted = sorted(datalist, key=lambda x: x[0])
    for simp, trad in X_sorted:
        cfile.write(f'{{"{simp}","{trad}"}},\n')
    

# 用法（請更換為你實際的檔案路徑）
def write_file():
    ofile=open('output.txt', 'w', encoding='utf-8')
    return ofile

cfile=write_file()
cfile.write("static const ZhMap zh_t2s_table[] = {")
compare_utf8_chars('gb2000.txt', 'zhtw2000.txt')
cfile.write("};")
#static const ZhMap zh_t2s_table[] = {
#    {"於", "于"},
#    {"錶", "表"},
#};

#compare_utf8_chars('zhtw2000.txt', 'gb2000.txt')
