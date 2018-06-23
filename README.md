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
* http://xxx/api/?<arguments>   (For request website)
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
- {“response”:<source code>}
* Use session.(http://localhost/api?url=http://www.baidu.com&session=True)
- {“response”:<source code>,’session’:<session character>,’cookies’:<cookies>}
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
- {“error”:<error message>}



