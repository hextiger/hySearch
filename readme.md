hySearch 慧搜

(C)Hextiger 2019  hxhy.blog.home

------

### 用法：

- **在搜索栏输入题目部分文字或拼音首字母即可**，输入内容越多结果越准确。  

- 按回车完成本次搜索，并清空搜索框等待新的搜索内容。 

- 点击左上角🔍可调出菜单，增加自定义题库，增加题库格式为：

 >  AAA/BB  
 >
 >  按吨位分,  （） 吨位以上才可算是大型航空母舰。 /C6万
 >
 >  奥运历史上第一个既举办过夏季奥运会，又举办冬季奥运会的城市是()。/B北京

​      其中AAA为题目，BB为答案，中间用/分割，每行1题  

​      如需建立全新题库，请删除程序所在文件夹中的data.zip文件即可

- 本程序使用python 3.x编写，用到的库包括wxpyhon、pandas、pypinyin
- 附带学习强国挑战答题和看视频答题题库，均为网上收集整理，希望大家共同补充完善

### 文件说明：
- data.zip 数据文件，需放至与主程序hySearch相同文件夹
- hySearch.pyw 源代码文件
- hySearch3-amd64-3.7.rar windows 64位版本，解压后运行hySearch.exe即可
- readme.md 说明文档
- setup.py cx-freeze生成exe文件模板

### log： 

- 3.191121：重建题库，收录1334条；搜索可以使用中文或拼音首字母，打包工具由pyingstaller改为cx_freeze
- 2.190930：增加题库录入，答案突出显示，更新题库至1325条
- 1.190912：初始版，仅包含检索功能，题库约800+