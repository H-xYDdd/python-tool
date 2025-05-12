import csv
import os
import argparse
from collections import defaultdict

def split_by_column(input_file, column_index=4, encoding='utf-8-sig', quote_columns=None):
    # 保持原spiltLargeFile.py的列拆分逻辑
    file_dir = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    file_name, file_ext = os.path.splitext(base_name)
    
    writers = defaultdict(lambda: None)
    
    with open(input_file, 'r', encoding=encoding) as f_in:
        reader = csv.reader(f_in)
        header = next(reader)
        
        for row in reader:
            if len(row) <= column_index:
                continue
                
            # 处理需要加单引号的列
            if quote_columns:
                for col in quote_columns:
                    if len(row) > col:
                        row[col] = f"'{row[col]}"

            group_key = row[column_index]
            
            if not writers[group_key]:
                output_path = os.path.join(file_dir, f"{file_name}_{group_key}{file_ext}")
                f_out = open(output_path, 'w', newline='', encoding=encoding)
                writer = csv.writer(f_out)
                writer.writerow(header)
                writers[group_key] = (writer, f_out)
            
            writers[group_key][0].writerow(row)
        
        for _, f in writers.values():
            if f: f.close()

def split_by_lines(input_file, max_lines, output_dir):
    # 保持原split_large_file.py的行数拆分逻辑
    os.makedirs(output_dir, exist_ok=True)
    
    file_count = 1
    line_count = 0
    output_file = None
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line_count % max_lines == 0:
                if output_file:
                    output_file.close()
                output_path = os.path.join(output_dir, f'output_{file_count}.csv')
                output_file = open(output_path, 'w', encoding='utf-8')
                file_count += 1
            output_file.write(line)
            line_count += 1
    
    if output_file:
        output_file.close()


# # 为第3列和第5列添加单引号，同时按第4列进行拆分
# python split_tool.py "data.csv" --mode column --column 4 --quote_columns 3,5

# # 按行拆分单个文件
# python split_tool.py "d:/bigfile.csv" --mode lines --max_lines 10000
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='多功能文件拆分工具')
    parser.add_argument('input_path', help='输入文件/目录路径')
    parser.add_argument('--mode', choices=['column', 'lines'], required=True, 
                      help='拆分模式：column-按列拆分，lines-按行拆分')
    
    # 按列拆分专用参数
    parser.add_argument('--column', type=int, default=4, help='(column模式)拆分依据列，从0开始')
    parser.add_argument('--encoding', default='utf-8-sig', help='(column模式)文件编码格式')
    
    # 新增参数（添加到column模式参数部分）
    parser.add_argument('--quote_columns', type=lambda s: [int(x) for x in s.split(',')], 
                      default=[], help='(column模式)需要添加单引号的列索引，用逗号分隔')
    
    args = parser.parse_args()

    try:
        if args.mode == 'column':
            # 修改调用方式（在现有调用中添加新参数）
            if os.path.isdir(args.input_path):
                for filename in os.listdir(args.input_path):
                    if filename.endswith('.csv'):
                        file_path = os.path.join(args.input_path, filename)
                        split_by_column(file_path, args.column, args.encoding, args.quote_columns)
            else:
                split_by_column(args.input_path, args.column, args.encoding, args.quote_columns)
                
        elif args.mode == 'lines':
            if not args.max_lines:
                raise ValueError("lines模式需要指定--max_lines参数")
                
            output_dir = os.path.join(os.path.dirname(args.input_path), 'result')
            split_by_lines(args.input_path, args.max_lines, output_dir)
            
        print("操作完成！")
        
    except Exception as e:
        print(f"错误发生：{str(e)}")
