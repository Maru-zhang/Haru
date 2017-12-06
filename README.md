# Haru
A command-line interface for generate CI Jobs automatically

# 使用方法

```
/// 在当前的目录中寻找.xcworkspace来在远程的jenkins中构建单元测试
haru job -i [--init]
/// 检索某一个远程job的信息
haru job -q [--query] [job name]
```