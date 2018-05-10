"""
void    showAllIP():
打印数据库 ipPool 中所有的 IP 信息
IP      getIPInfo(id):
输入一个 IP 的 id（int），返回这个 IP 的信息，若 id 不存在，返回 NULL
void    deleteIPinfo(id):
输入一个 IP 的 id（int），删除这一条记录，无返回
void    insertIPinfo(IP):
新增一条 IP 记录，若重复则不添加
int     getIPID(Address, Port):
输入地址（str）、端口（int），获取相应的 IP 的 id

void    showAllWeb():
打印数据库 Websites 中所有的信息
list    getWebsiteInfo(id):
输入 Websites 的 id，获取所有信息
int     insertWebsiteInfo(url):
新增一条 URL 记录， 返回其在数据库中的 id
void    deleteWebsiteinfo(id):
输入一个 URL 的 id（int），删除这一条记录，无返回
int     getidByURL(url):
输入 url（str）信息，获取在 Websites 表中的 id

void    showAllRes():
打印数据库 ResponseTime 中所有的信息
void    genResInfo(URLID, IPID, ResponseTime, Method, StatusCode, Header):
生成一条新的记录，数据类型（int，int，int，str，int，str）
void    updateResTimeByID(URLID, IPID, newtime):
------未定-------
void    updateResValueByID (URLID, IPID, Method, StatusCode, Header):
------未定-------
void    deleteByID(URLID, IPID):
根据 URLid 和 IPid 删除记录

list<IP>getIPs(n):
输入需要获取的 ip 数 n，随机返回 n 个 ip 地址

void    resetDatabases():
清空数据库

"""