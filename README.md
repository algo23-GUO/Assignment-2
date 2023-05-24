# Assignment-2
使用米筐API，调用rqfactor库获取股票相关数据

股票池选择

1.选取成长因子 (SUE+ROE+SUR) 排名前10%的股票SUE因子为[净利润(t)-净利润(t-4)]/过去四期净利润变化的波动率2.选取估值因子 (PB) 排名后40%的股票

2.换手率优选:
剔除月度换手率因了排名前10%的股票

3.位序估值优选:
为了避免追高与低估值陷阱，别除PB在时席上排名10% (6months) 和后10% (3years) 的股票

回测表现：

![cd10b92381cc8a998a170119aeaf0d6](https://github.com/algo23-GUO/Assignment-2/assets/128219105/a911f288-8173-42ef-a8f8-0a61af58c60d)
![5ff0966900e1682a7a9bfe41cf4516b](https://github.com/algo23-GUO/Assignment-2/assets/128219105/6d2b31d8-659d-43a9-8855-8e14ed8d560a)
