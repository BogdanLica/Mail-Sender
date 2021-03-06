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

---
### Installation & Usage

* add an API Key for VirusTotal to **handle_files.py**


#### Pip
> pip install -r requirements.txt
> python main.py

#### Docker
##### Inside the **docker** folder
> docker-compose build

> docker-compose run mail-sender

**Note:** put the files to be sent via email in the **docker/attachments** folder