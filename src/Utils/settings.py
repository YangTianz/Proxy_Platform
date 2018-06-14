# Redis数据库地址
REDIS_HOST = '111.230.249.201'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'Sustech15'

REDIS_KEY = 'ProxyPlatform'

# MySQL 数据库地址
MYSQL_HOST = REDIS_HOST

# MySQL 端口
MYSQL_PORT = 3306

# MySQL 用户
MYSQL_USER = 'test'

# MySQL 密码
MYSQL_PASSWORD = 'Sustech15'

# MySQL 表格
MYSQL_DB = 'Proxy_Platform'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 20

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10
