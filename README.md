# soucha项目

## 运行
```bash
# 需要python2.7
./prepare.sh # 用于pip安装第三方依赖库

# 首次运行时,需要初始化数据库
fab db_init 

# 运行web服务器
fab web

# 运行图片匹配测试程序
fab match #将app/cha/sample/candidate中的每一张图片和app/cha/sample/original中的图片对比, 并计算汉明距离
```