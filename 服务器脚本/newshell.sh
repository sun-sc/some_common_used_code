#!/bin/bash

# 新建脚本，并赋予执行权限
# 使用方法./newshell.sh 新建脚本名
touch $1 &&
chmod +x $1 &&
echo "#!/bin/bash" > $1