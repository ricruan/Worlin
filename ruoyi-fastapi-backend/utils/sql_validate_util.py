# 判断用户的SQL代码是否合法、以及语法是否正确
# 防止SQL注入攻击 权限管理（只读权限）
# 数据库池子？  这里需要我来弄docker支持吗？（Docker 启完了 可以）
# （启得慢，但是还好）
# 这块我尝试一下，我之前有一个这样的想法……
# 有第三方包 


"""
Todo: 
1. Docker 判题环境
2. 这段时间有时间多聊聊
3. 分工（

宇峰：调试接口、前端
飞：测试库 和 判题 （SQL链接） （docker支持）


调用函数 每次需要一个新的SQL链接，或者链接好的cenection对象？
给一个销毁的类，销毁链接，内存泄漏

具体可以讨论一下（我想个方案）

其他的用户类什么的，？后面再说

4. 远程搞一个mysql redis 的环境 不用本地测试数据
然后commit push掉
"""
