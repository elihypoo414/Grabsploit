
# About Grabsploit

This project is intended to create a github version of search functions for exploits through Criminal IP. Data will be saved on edb_contents file.

# Prerequisites

-   [criminalip.io](http://criminalip.io/)  API Key
    

->> [here](https://www.criminalip.io/)  <<-

# Installation Process  

Clone repository to install:  

$ git clone https://github.com/elihypoo414/Grabsploit.git

$ cd Grabsploit

$ python3 -m venv .venv  
$ source .venv/bin/activate

$ pip3 install -r requirements.txt

  

# Getting started

$ python3 Grabsploit.py [Command]

# Optional Arguments

`-A/--auth`

**API key**

api authentication with a valid  [criminalip.io](http://criminalip.io/)  api key

`-Q/--query`

**Exploit Query**

Return exploit data from query

`-D/--download`

**File Path**

CSV download result of the exploit search

`-R/--read`

**File Path**

Read the exploit search result CSV file

`-C/--cve-id`

**CVE_ID**

Exploit search with CVE_ID

`-E/--edb-id`

**EDB_ID**

Exploit search with EDB_ID

`-P/--platform`

**Platform**

Exploit search with platform
