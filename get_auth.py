# Poll based authorized_keys file retrieval
# Steven Richards <sbrichards@mit.edu>
# put in your crontab and point at your authorized_keys server, run as root if multiple users


#IMPORTS -------------------------------------------------------
try:
    import requests #requests module by kennethreitz for http(s)
except ImportError:
    print "You need to install the requests module: \
           http://docs.python-requests.org/en/latest/"
    exit(1)
from sys import platform as _platform
import re as regex #regular expressions are fun 
import time #time, yo

#CONFIGURATION -------------------------------------------------
location = "http://<host>/<file>" #URI of authorized_keys
users_list = ['<user>'] #Username(s) to update
valid_uri_re = regex.compile('^(http|https)://') #RegEx for verifying valid URI
valid_keys_re = regex.compile('^(ssh-rsa|ssh-dsa)') #RegEx for verifying valid auth_keys file
if _platform == "linux" or _platform == "linux2":
    root = '/home/' #on linux, set root dir for users
elif _platform == "darwin":
    root = '/Users/'#on mac, set root dir for users
else: 
    print "Platform not supported"
    exit(1)

#MAIN ----------------------------------------------------------
def main():
    if (valid_uri_re.match(location) and len(users_list) != 0):
          print "Valid URI:\n"+location+"\nRetrieving file..."
          auth_keys_raw = requests.get(location)
          if (auth_keys_raw.status_code == 200 and \
              valid_keys_re.match(auth_keys_raw.text)):
          
              print "Success! File current as of: "+ \
                     time.asctime(time.localtime(time.time())) 
          
              for user in users_list:
                  try:
                      path = root+user+'/.ssh/authorized_keys'
                      open(path, 'w').close() #essentially delete the existing file
                      auth_key_file = open(path, 'w')
                      auth_key_file.write(auth_keys_raw.text)
                      auth_key_file.close()
                  except IOError:
                      print "IO Error in updating authorized_keys for " + user
                      exit(1)
                  print "Updated authorized_keys for: " + user
              exit(0)
          else:
              print "Something went wrong - Status Code: " + \
              str(auth_keys_raw.status_code) + \
              "\nand file marked as " + \
              str(valid_keys_re.match(auth_keys_raw.text)) + \
              auth_keys_raw.text  
    exit(1)          
#END -----------------------------------------------------------

if __name__ == '__main__':
    main() 
