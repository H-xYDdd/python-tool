# python-tool
python小工具合集

## 1. csv大文件拆分工具

### 帮助文档
```Bash
root@ubuntu-virtual-machine:~/code# python3 split_tool.py --help
usage: split_tool.py [-h] --mode {column,lines} [--column COLUMN] [--encoding ENCODING] [--quote_columns QUOTE_COLUMNS] input_path

多功能文件拆分工具

positional arguments:
  input_path            输入文件/目录路径

optional arguments:
  -h, --help            show this help message and exit
  --mode {column,lines}
                        拆分模式：column-按列拆分，lines-按行拆分
  --column COLUMN       (column模式)拆分依据列，从0开始
  --encoding ENCODING   (column模式)文件编码格式
  --quote_columns QUOTE_COLUMNS
                        (column模式)需要添加单引号的列索引，用逗号分隔
```


### 样例
```python
# 为第3列和第5列添加单引号，同时按第4列进行拆分
python split_tool.py "data.csv" --mode column --column 4 --quote_columns 3,5

# 按行拆分单个文件
python split_tool.py "d:/bigfile.csv" --mode lines --max_lines 10000
```
