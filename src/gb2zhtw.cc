#include <iostream>
#include <string>
#include <vector>
#include <cstring>

struct ZhMap
{
    const char *simp; // UTF-8 encoded simplified
    const char *trad; // UTF-8 encoded traditional
};
#include "s2t_table.h"

static const int zh_s2t_table_size = sizeof(zh_s2t_table) / sizeof(zh_s2t_table[0]);
const char *zh_s2t_lookup(const char *utf8_char)
{
    if (!utf8_char || std::strlen(utf8_char) == 0)
        return "";

    int left = 0;
    int right = zh_s2t_table_size - 1;

    while (left <= right)
    {
        int mid = (left + right) / 2;
        int cmp = std::strcmp(utf8_char, zh_s2t_table[mid].simp);
        if (cmp == 0)
        {
            return zh_s2t_table[mid].trad;
        }
        else if (cmp < 0)
        {
            right = mid - 1;
        }
        else
        {
            left = mid + 1;
        }
    }
    return utf8_char;
}
// 取得 UTF-8 字元長度
int utf8_char_len(unsigned char c)
{
    if ((c & 0x80) == 0x00)
        return 1;
    else if ((c & 0xE0) == 0xC0)
        return 2;
    else if ((c & 0xF0) == 0xE0)
        return 3;
    else if ((c & 0xF8) == 0xF0)
        return 4;
    else
        return 1; // fallback
}
char *zh_s2t_string(const char *input)
{
    if (!input)
        return NULL;

    size_t input_len = strlen(input);
    size_t buffer_size = input_len * 4 + 1; // 預估最大長度
    char *output = (char *)malloc(buffer_size);
    if (!output)
        return NULL;

    output[0] = '\0';

    int offset = 0;
    while (input[offset])
    {
        int len = utf8_char_len((unsigned char)input[offset]);
        char utf8_char[5] = {0};
        memcpy(utf8_char, input + offset, len);
        utf8_char[len] = '\0';

        const char *trad = zh_s2t_lookup(utf8_char);
        strncat(output, trad, buffer_size - strlen(output) - 1);

        offset += len;
    }

    return output;
}