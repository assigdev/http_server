# HTTP Server

Otus homework project

### install:

clone repository:

    $ git clone https://github.com/assigdev/async_http_server.git
    
    pipenv install
    
if you don't have pipenv:
    
    pip install pipenv

### Run
    
    python httpd.py  # multiproccessing deamon
    
    python httpd_threads.py # multithreading deamon
    
    python httpd_threads_new.py # multithreading deamon(socket.accept in child version)
    
    python httpd_one_process.py # simple deamon


### Configs
    
    optional arguments:
      -h, --help            show this help message and exit
      -r ROOT, --root ROOT  documents path
      -w WORKERS_COUNT, --workers_count WORKERS_COUNT
                            count of workers
      -a HOST, --host HOST  host address
      -p PORT, --port PORT  port for connection
      -t TIMEOUT, --timeout TIMEOUT
                            timeout for connection
      -l LOG, --log LOG     log file path
      -d, --debug           debug logging


### Functional testing

    python httpdtest.py
    

### AB Testing

    ab -c 100 -n 50000 {ip:port}
    

httpd.py 2 workers:

    Concurrency Level:      100
    Time taken for tests:   55.599 seconds
    Complete requests:      50000
    Failed requests:        32
       (Connect: 0, Receive: 0, Length: 32, Exceptions: 0)
    Non-2xx responses:      50001
    Total transferred:      11348019 bytes
    HTML transferred:       3597768 bytes
    Requests per second:    899.30 [#/sec] (mean)
    Time per request:       111.198 [ms] (mean)
    Time per request:       1.112 [ms] (mean, across all concurrent requests)
    Transfer rate:          199.32 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    4  59.5      0    3042
    Processing:     0   33 1153.7      1   54592
    Waiting:        0   33 1153.7      0   54592
    Total:          0   37 1169.6      1   55597
    
    Percentage of the requests served within a certain time (ms)
      50%      1
      66%      1
      75%      1
      80%      1
      90%      1
      95%      1
      98%      2
      99%      3
     100%  55597 (longest request)

    
httpd.py 4 workers:

    Concurrency Level:      100
    Time taken for tests:   30.898 seconds
    Complete requests:      50000
    Failed requests:        28
       (Connect: 0, Receive: 0, Length: 28, Exceptions: 0)
    Non-2xx responses:      50000
    Total transferred:      11348068 bytes
    HTML transferred:       3597984 bytes
    Requests per second:    1618.21 [#/sec] (mean)
    Time per request:       61.797 [ms] (mean)
    Time per request:       0.618 [ms] (mean, across all concurrent requests)
    Transfer rate:          358.66 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    3  57.0      0    1036
    Processing:     0   14 515.6      1   27181
    Waiting:        0   14 515.6      0   27182
    Total:          0   18 528.8      1   27846
    
    Percentage of the requests served within a certain time (ms)
      50%      1
      66%      1
      75%      1
      80%      1
      90%      1
      95%      1
      98%      1
      99%      2
     100%  27846 (longest request)

    
    
httpd.py 8 workers:

    Concurrency Level:      100
    Time taken for tests:   4.472 seconds
    Complete requests:      50000
    Failed requests:        0
    Non-2xx responses:      50000
    Total transferred:      11350000 bytes
    HTML transferred:       3600000 bytes
    Requests per second:    11181.14 [#/sec] (mean)
    Time per request:       8.944 [ms] (mean)
    Time per request:       0.089 [ms] (mean, across all concurrent requests)
    Transfer rate:          2478.63 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    6  76.3      0    1033
    Processing:     0    2  24.6      1    1822
    Waiting:        0    1  24.6      1    1822
    Total:          0    8  88.8      1    2826
    
    Percentage of the requests served within a certain time (ms)
      50%      1
      66%      2
      75%      2
      80%      2
      90%      2
      95%      2
      98%      3
      99%      5
     100%   2826 (longest request)


httpd_threads.py 4 threads:

    Concurrency Level:      100
    Time taken for tests:   21.150 seconds
    Complete requests:      50000
    Failed requests:        0
    Non-2xx responses:      50000
    Total transferred:      11350000 bytes
    HTML transferred:       3600000 bytes
    Requests per second:    2364.09 [#/sec] (mean)
    Time per request:       42.300 [ms] (mean)
    Time per request:       0.423 [ms] (mean, across all concurrent requests)
    Transfer rate:          524.07 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0   26 188.0      0    7288
    Processing:     1   16  36.7     11    3300
    Waiting:        1   16  36.7     11    3300
    Total:          1   42 200.5     11    7301
    
    Percentage of the requests served within a certain time (ms)
      50%     11
      66%     19
      75%     23
      80%     25
      90%     31
      95%     41
      98%   1017
      99%   1037
     100%   7301 (longest request)
    
    
httpd_threads.py 8 threads:

    Concurrency Level:      100
    Time taken for tests:   36.521 seconds
    Complete requests:      50000
    Failed requests:        1
       (Connect: 0, Receive: 0, Length: 1, Exceptions: 0)
    Non-2xx responses:      50000
    Total transferred:      11349931 bytes
    HTML transferred:       3599928 bytes
    Requests per second:    1369.08 [#/sec] (mean)
    Time per request:       73.042 [ms] (mean)
    Time per request:       0.730 [ms] (mean, across all concurrent requests)
    Transfer rate:          303.49 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0   40 289.4      0   15455
    Processing:     0   10 158.2      4   15364
    Waiting:        0   10 158.2      4   15364
    Total:          0   51 350.8      4   16384
    
    Percentage of the requests served within a certain time (ms)
      50%      4
      66%      5
      75%      5
      80%      5
      90%      6
      95%      7
      98%   1027
      99%   1228
     100%  16384 (longest request)

### Wrk Testing

run httpd.py and then run  wrk 
    
    wrk -t5 -c100 -d30  {ip:port}


httpd_one_process.py:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    22.66ms  119.12ms   1.93s    95.60%
        Req/Sec   334.92    381.38     2.98k    89.65%
      48952 requests in 30.05s, 10.60MB read
      Socket errors: connect 0, read 0, write 0, timeout 16
      Non-2xx or 3xx responses: 48952
    Requests/sec:   1629.11
    Transfer/sec:    361.14KB



httpd.py 2 workers:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     8.21ms   53.57ms   1.68s    97.58%
        Req/Sec   406.35      0.95k   11.98k    94.82%
      58711 requests in 30.08s, 12.71MB read
      Socket errors: connect 0, read 0, write 0, timeout 22
      Non-2xx or 3xx responses: 58711
    Requests/sec:   1952.08
    Transfer/sec:    432.74KB



httpd.py 4 workers:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    11.82ms   88.16ms   1.68s    97.89%
        Req/Sec   445.61      0.94k    8.78k    95.32%
      63697 requests in 30.08s, 13.79MB read
      Socket errors: connect 0, read 0, write 0, timeout 20
      Non-2xx or 3xx responses: 63697
    Requests/sec:   2117.65
    Transfer/sec:    469.44KB



httpd.py 6 workers:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    13.79ms   89.78ms   1.71s    97.13%
        Req/Sec   465.24      0.92k    7.62k    94.24%
      68280 requests in 30.08s, 14.78MB read
      Socket errors: connect 0, read 0, write 0, timeout 15
      Non-2xx or 3xx responses: 68280
    Requests/sec:   2269.96
    Transfer/sec:    503.20KB


httpd.py 8 workers:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    12.83ms   82.89ms   1.70s    97.51%
        Req/Sec   542.94      1.14k    7.87k    93.16%
      77483 requests in 30.07s, 16.77MB read
      Socket errors: connect 0, read 0, write 0, timeout 11
      Non-2xx or 3xx responses: 77483
    Requests/sec:   2576.93
    Transfer/sec:    571.25KB



httpd_threads.py 4 threads:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    29.91ms   51.90ms   1.68s    98.12%
        Req/Sec   383.93    254.52     2.11k    88.11%
      55970 requests in 30.08s, 12.12MB read
      Non-2xx or 3xx responses: 55970
    Requests/sec:   1860.88
    Transfer/sec:    412.52KB


    

httpd_threads.py 8 threads:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    19.07ms   50.44ms   1.67s    97.53%
        Req/Sec   322.53    151.66     1.82k    83.78%
      47406 requests in 30.08s, 10.26MB read
      Non-2xx or 3xx responses: 47406
    Requests/sec:   1575.88
    Transfer/sec:    349.34KB


httpd_threads.py 20 threads:
    
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    21.17ms   78.79ms   1.67s    97.82%
        Req/Sec   313.64    140.04     1.72k    84.71%
      45649 requests in 30.11s, 9.88MB read
      Socket errors: connect 0, read 0, write 0, timeout 15
      Non-2xx or 3xx responses: 45649
    Requests/sec:   1516.20
    Transfer/sec:    336.11KB




httpd_threads_new.py 4 threads:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     9.18ms   64.08ms   1.70s    98.77%
        Req/Sec   320.12    249.45     2.57k    86.77%
      42013 requests in 30.09s, 9.10MB read
      Socket errors: connect 0, read 0, write 0, timeout 18
      Non-2xx or 3xx responses: 42013
    Requests/sec:   1396.06
    Transfer/sec:    309.48KB



httpd_threads_new.py 8 threads:

      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    14.78ms   75.92ms   1.68s    97.46%
        Req/Sec   322.91    175.50     1.53k    85.56%
      47572 requests in 30.08s, 10.30MB read
      Socket errors: connect 0, read 0, write 0, timeout 14
      Non-2xx or 3xx responses: 47572
    Requests/sec:   1581.47
    Transfer/sec:    350.58KB



httpd_threads_new.py 20 threads:
    
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    17.75ms   66.58ms   1.68s    97.98%
        Req/Sec   318.40    149.03     1.51k    88.72%
      47118 requests in 30.10s, 10.20MB read
      Socket errors: connect 0, read 0, write 0, timeout 7
      Non-2xx or 3xx responses: 47118
    Requests/sec:   1565.55
    Transfer/sec:    347.05KB


