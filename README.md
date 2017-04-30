# cinman 

**cinman** is a software system for monitoring system informations like softwares installed, hard disk usages, log files, etc. from computers connected to the local network and monitor them from a web browser. It contains two parts:- client and server. Client part is installed in the computers that you want ot monitor. Server part is installed on a computer which will work as a server.   

## Installation
**Client**
1. install python-2.5 or above
2. extract client.tar.gz contained in the root directory \(cinman\)
3. change the server address in file daemon.py and devices.py
4. enter python daemon.py
5. enter python devices.py
6. whenever required enter python message.py to run messaging client to send messages to administrator

**Server**
1. install postgresql
2. install python-2.5 or above
3. install django
4. install python package pyscopg2
5. extract the cinman folder \(root folder\)
6. enter python manage.py createsuperuser 
   * give the required details, which will create a superuser
7. open cinman/cinman/settings.py and change the username and password of email
   * this email id will be used to send notifications
8. enter python manage.py runserver \[0.0.0.0\] \[port\]
   * this will run the server at the given port
9. Now the server is running, go to url http\:ipaddress:port to view web application

## Contributor
* contributors for server and web application
   * Bikash
   * Anvesh
   * Akshay
* contributors for client side softwares
   * Premnath
   * Mithil
