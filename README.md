# pmtw
"Panierte Maultaschen" are on the menu !! 111

## Usage
usage: main.py [-h] [-l host] [-p port] -e email -c password
               [-k [keywords [keywords ...]]] [-r [email [email ...]]]

Which 'wichtel' url should be seached for which keywords?

optional arguments:
  -h, --help            show this help message and exit
  -l host, --link host  Smtp server
  -p port, --port port  The port for the smtp server
  -e email, --email email
                        Email address of the sender
  -c password, --code password
                        Password of sender email
  -k [keywords [keywords ...]], --keywords [keywords [keywords ...]]
                        Keywords and phrases to check in meals menu
  -r [email [email ...]], --recipients [email [email ...]]
                        Email addresses of people to notify
