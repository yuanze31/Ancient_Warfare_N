# -*- coding: utf-8 -*-
def sort_file_lines(file_path):
    """读取文件，对行排序后覆盖原文件"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        lines.sort()  # 按ASCII码排序（区分大小写）

        with open(file_path, 'w') as f:
            f.writelines(lines)
        return True
    except Exception as e:
        print "处理 %s 时出错: %s" % (file_path, str(e))
        return False


def process_files(file_list):
    """处理预定义文件列表"""
    success_count = 0
    for file_path in file_list:
        if sort_file_lines(file_path):
            success_count += 1
            print "已处理: %s" % file_path
    print "\n处理完成！成功处理 %d/%d 个文件" % (success_count, len(file_list))


# 在这里修改需要处理的文件列表（支持绝对路径和相对路径）
file_list = ['./main/awR/texts/zh_CN.lang']

if __name__ == "__main__":
    process_files(file_list)
