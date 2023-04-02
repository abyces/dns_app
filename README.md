# dns_app

This is the code for NYU DCN Spring 2023 class.

There are three components:
- FS: Fibonacci server: answer queries for i-th fibonacci number
- US: User server: query for i-th fibonacci number
- AS: DNS server: provide DNS services

The code simulates the process of DNS registration and query. 
FS registers its domain name and IP address to the DS. US first obtains the IP address corresponding to the domain name by querying the DS.
Then, US queries for i-th Fibonacci number from FS.
