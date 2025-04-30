# LeakcheckDumper
Python3 script to dump breach data from Leakcheck.io

````
usage: leakcheckdumper.py [-h] (-d <domain> | --domains <file>) -t <token> [-f] [-s]

options:
  -h, --help            show this help message and exit
  -d, --domain <domain>
                        Domain name to extract leaks
  --domains <file>      Newline-separated file with domain names
  -t, --api-token <token>
                        LeakCheck API token
  -f, --full            Dump all data from LeakCheck into CSV
  -s, --show            Show each leak
````
