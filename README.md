# Proxy Platform
## Introduction
* Programmers can use our API to access websites.
 Then the website cannot know about the IP of programmer, 
 the website consider that it is our IP accessing the website.
 So the website cannot forbid the IP of programmer.
## Feature
1. Expand IP pool – By Free IP collector.<br/>
About 1000 high-anonymity IP at a time.
2. Maintain IP dynamically – By IP Validator.
3. Different IP using strategy – By API parameters.
4. “Session” function optional.
5. HTTP and HTTPS.
6. Load balancing and failover – By Nginx.
7. IP Pool’s condition monitoring.
## Quick start for single deployment
### Environment requirement
* Python 3.6
### Dependencies
- cd Proxy_Platform <br/>
- python -m pip install -r requirements.txt
### Run 
- cd src <br/>
- python Listener.py
## API
### API format
* http://xxx/api/?[arguments]   (For request website)
* http://xxx/status             (For condition monitoring)
### Arguments
* url : The website you want to request.
* headers : The headers you want to add into datagram.
* cookies : The cookies you want to add into datagram.
* method : ‘get’ or ‘post’.
* data : The data you want to add into datagram.
* time_max : The max request times for one IP.
* time_delay : The delay time between two requests.
* request_con : Task concurrency.
* timeout : The timeout of one request.
* Session : ‘Session’ function.
### Example
* http://localhost/api/?url=http://www.baidu.com&&time_max=2&&session=xoisuf02
* http://localhost/status
## Session
<strong>Introduction</strong><br/>
* Some websites have strategy that cookies bind with IP.
 So if user wants to request the website continuously, 
 we provide a session function that user can use the same IP.
<strong>How to use?</strong><br/>
The first time you want to use the session function, you should let ‘session=True’. <br/>
Then, you will get a session string character such as ‘UvQk7OIG’.<br/>
The next time you want to use the same IP just let ‘session’ equals to the character.
## Return format
* No session. (e.g. http://localhost/api?url=http://www.baidu.com)
- {“response”:[source code]}
* Use session.(http://localhost/api?url=http://www.baidu.com&session=True)
- {“response”:[source code],’session’:[session character],’cookies’:[cookies]}
* Condition monitoring. (e.g. http://localhost/status)<br/>
当前 IP 总数：xxx<br/>
IP 分数分布: (越高越好)<br/>
1 ~ 19:  xx<br/>
20 ~ 30: xx<br/>
31 ~ 40: xx<br/>
41 ~ 50: xx<br/>
51 ~ 60: xx<br/>
61 ~ 70: xx<br/>
71 ~ 80: xx<br/>
81 ~ 90: xx<br/>
90 ~ 100: xx<br/>
只有分数大于 xx 的 IP 地址会被使用
* Argument error. (e.g. http://localhost/api/?url=”w.baidu.com”)
- {“error”:[error message]}
## Principle
### Web framework
* Flask<br/>
![](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/web1.png)
![](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/web2.png)
### IP scheduler
* Path: /src/Schdule
* Function: 
<p>Acquire IP from database. </p>
<p>Schedule IP to visit website according to API arguments. </p>
<p>Use IP which score higher first. </p>

### IP collector 
This component is based on an open source project on Github[1]. 
 The file structure for this component is shown in the Fig.1.  
 ![Fig. 1 File Structure](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/file_structure.png)
 <br/>For the proxy spider, it uses xpath to drag IP proxy information from free IP proxy website.  
 The content of xpath, the url,
 and some other information are all stored in config.py which is the profile for this part. 
 While running, it creates one thread to crawl target website and fifty threads to test and verify the usability for each IP proxy. 
 All the usable IP proxy will be added to database. 
 The architecture of this part is shown in Fig.2. 
![Fig. 2 Component Architecture](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/Component_Architecture.png) 
 <br/>Because of network fluctuations and the limitation of visiting on some IP proxy website,
 this spider need to resend HTTP request to the target website once the HTTP response doesn’t be received after TIMEOUT which makes this spider a little bit slow.
 Some proxy websites use anti-crawl mechanism which means running proxy spider frequently will get IP proxies less and less.  
 Since they are all free IP proxies, it still can’t get that much usable IP proxies.  
 The running output on console is shown in Fig.3. <br/>
![Fig. 3 running output](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/running_output.png)
### IP calibrator
### Load balancing and failover
<p>We use Nginx to finish load balancing and failover. </p>
<p>Nginx can make a proxy to dispense requests to our servers. </p>
<p>For example, these pictures are our setting for Nginx.</p>

![1](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/Nginx1.png)
![1](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/Nginx2.png)
<p>The first picture means that we make 4 servers for Nginx. The first three servers are running and the forth server is backup. So if the first three servers all fail, then the backup server will receive the request. After servers, here is a ‘fair’ word means that it will dispense requests depend on server response time.
</p>
<p>The second picture is that we let Nginx proxy on 0.0.0.0:80. So if someone request 0.0.0.0:80, then it will dispense this request to the server.
</p>

### Database
* Redis
<p>To deal with large amounts of IP information, the proxy platform chooses redis as its IP proxy database. Each IP has a score to show its quality and it’s has the format as address:port:type (e.g. 11.22.33.44:80:HTTPS). All the proxy IPs are stored in a zset called ProxyPlatform sort by its score in order to facilitate the use and maintenance of IP. The scheduler can randomly get IP proxy from the database and the tester can check the IP score sequentially.
</p>

![Proxy IP in Redis](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/redis.png)
* MySQL
<p>The proxy platform uses MySQL to store other information about the operations made by users. </p>

* Table Saves stores the request method, response status code, response header and response time of each request operation. Users can query and get the information of the request they had made before.

![Request information in MySQL](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/request_information.png)
* Table Session stores the information of Session function. It generates a unique 8 characters length string and map it to the specific IP. Users can get the same IP as they used before by the unique string.

![Session information in MySQL](https://raw.githubusercontent.com/YangTianz/Proxy_Platform/master/pic/session_information.png)

## Test
<p>To simulate a environment for high loading, we used 4 computers create 500 threads to request our program. And we used 4 servers to receive requests.</p>
<p>Because it wasn’t let our server load fully, it only has over 100 requests per second.</p>
<strong>If you are interested, you can test our program and tell us.</strong>

## Reference
* ![proxyspider](https://github.com/zhangchenchen/proxyspider)
* ![haipproxy](https://github.com/SpiderClub/haipproxy)
* ![python3webspider](https://github.com/python3webspider)