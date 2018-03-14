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
    
    python httpd_one_process.py # simple deamon

### Functional testing

    python httpdtest.py

### AB Testing

    docker run --rm jordi/ab -k -c 100 -n 50000 {ip:port}
    
httpd_one_process.py:
    
    apr_pollset_poll: The timeout specified has expired (70007)
    Total of 49917 requests completed

httpd.py 2 workers:

    apr_pollset_poll: The timeout specified has expired (70007)

httpd_threads.py 4 threads:
    
    

### Wrk Testing

run httpd.py and then run  wrk on docker
    
    docker run --rm -v /etc/hosts:/etc/hosts skandyla/wrk -t5 -c10 -d30  {ip:port}


httpd_one_process.py:

    Running 30s test @ http://192.168.88.65:8080
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     6.85ms   30.18ms 415.83ms   96.51%
        Req/Sec   423.52    485.96     2.06k    85.28%
      61296 requests in 30.10s, 13.27MB read
      Non-2xx or 3xx responses: 61296
    Requests/sec:   2036.57
    Transfer/sec:    451.47KB


httpd.py 2 workers:

    Running 30s test @ http://192.168.88.65:8080
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.83ms  821.46us  24.79ms   73.28%
        Req/Sec   320.25    237.98     1.21k    81.94%
      28225 requests in 30.07s, 6.11MB read
      Socket errors: connect 4, read 0, write 0, timeout 0
      Non-2xx or 3xx responses: 28225
    Requests/sec:    938.54
    Transfer/sec:    208.06KB


httpd.py 4 workers:

    Running 30s test @ http://192.168.88.65:8080
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.67ms  677.07us  10.84ms   72.99%
        Req/Sec   335.04    266.55     1.25k    82.77%
      26865 requests in 30.10s, 5.82MB read
      Non-2xx or 3xx responses: 26865
    Requests/sec:    892.66
    Transfer/sec:    197.88KB


httpd.py 6 workers:

    Running 30s test @ http://192.168.88.65:8081
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.89ms    0.92ms  15.13ms   69.08%
        Req/Sec   312.65    229.96     1.16k    79.91%
      28225 requests in 30.07s, 6.11MB read
      Socket errors: connect 4, read 0, write 0, timeout 0
      Non-2xx or 3xx responses: 28225
    Requests/sec:    938.65
    Transfer/sec:    208.08KB


httpd_threads.py 4 threads:

    rk -t5 -c10 -d30  http://192.168.88.14:8080/
    Running 30s test @ http://192.168.88.14:8080/
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     3.01ms    4.64ms 208.07ms   99.53%
        Req/Sec   298.44     92.87     0.98k    83.58%
      44235 requests in 30.10s, 9.58MB read
      Non-2xx or 3xx responses: 44235
    Requests/sec:   1469.83
    Transfer/sec:    325.83KB

    

httpd_threads.py 10 threads:

    rk -t5 -c10 -d30  http://192.168.88.14:8080/
    Running 30s test @ http://192.168.88.14:8080/
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     2.80ms    3.57ms 208.62ms   98.93%
        Req/Sec   294.21     98.53     0.90k    83.17%
      42998 requests in 30.08s, 9.31MB read
      Non-2xx or 3xx responses: 42998
    Requests/sec:   1429.52
    Transfer/sec:    316.90KB

httpd_threads.py 100 threads:
    
    rk -t5 -c10 -d30  http://192.168.88.14:8080/
    Running 30s test @ http://192.168.88.14:8080/
      5 threads and 10 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     3.12ms    8.37ms 207.67ms   99.40%
        Req/Sec   309.51    138.05     1.01k    86.68%
      44945 requests in 30.10s, 9.73MB read
      Non-2xx or 3xx responses: 44945
    Requests/sec:   1493.30
    Transfer/sec:    331.03KB

    

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
