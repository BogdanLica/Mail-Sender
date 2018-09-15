## Sending E-mails to an SMTP Server
* **smtpservers_scraper.py**
    * from a list of sources, fetch all the SMTP servers that exists and filter the output written to a file called **servers.txt**
* **main.py**
    * read the list of servers from **servers.txt**
    * try to find the SMTP server which is a match for the domain of the e-mail provided
    * attempt to login using TLS
    * if the login is successful, get the recipient, subject of the message and the body
    * send the e-mail(...takes around 4 minutes...)

**Note:** You need to enable 'unsecure login'

### TO-DO
- [ ] attach email and password stored sately in a database