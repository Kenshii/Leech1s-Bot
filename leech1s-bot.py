import requests, json, time
from bs4 import BeautifulSoup

chat_username = '<chat username>'
chat_password = '<chat password>'
chat_key = 'bf4a9597e5897f442'
box_id = '2352971'
box_tag = 'ltttao'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'

def login(s):
    url = 'http://www2.cbox.ws/box/?boxid={0}&boxtag={1}&sec=profile&n={2}&k={3}'.format(box_id, box_tag, chat_username, chat_key)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'clid_{0}=2; nme_{0}={1}'.format(box_id, chat_username)
    }
    data = {
        'pword': chat_password,
        'sublog': 'Log in'
    }
    s.post(url, data = data, headers = headers)

def buildMessageBody(s, original_link):
    link_check = s.post('http://cdn.leech1s.com/autocheck/ch.php?links={0}'.format(original_link))
    link_info = json.loads(link_check.text[1 : -1])
    return (
        '[center] {0} link_live  | [color=#CD0000][b] {1} [/b][/color]  | [color=black][b] {2}'
        ' [/b][/color][br][den]Checked By[/mau] [vang] F.A Team [/mau] [/center]  [sub](sent from Ireland)[/sub]'
    ).format(link_info['link'], link_info['filename'], link_info['filesize'])

def sendChatMessage(s, message_body):
    url = 'http://www2.cbox.ws/box/index.php?boxid={0}&boxtag={1}&sec=submit'.format(box_id, box_tag)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'nme': chat_username,
        'key': chat_key,
        'pst': message_body,
        'key': s.cookies['key_{0}'.format(box_id)]
    }
    s.post(url, data = data, headers = headers)

def getGeneratedLink(s):
    generated_link = None
    chat_msgs = s.get('http://www2.cbox.ws/box/?boxid={0}&boxtag={1}&sec=main'.format(box_id, box_tag))
    chat_soup = BeautifulSoup(chat_msgs.text, 'html.parser')
    msgs_sent_to_me = chat_soup(text = ' {0} '.format(chat_username))
    if msgs_sent_to_me:
        link_anchor = msgs_sent_to_me[0].parent.parent.parent.find('a', {'class' : 'bbURL'})
        if link_anchor:
            generated_link = link_anchor['href']
    return generated_link

def main():
    s = requests.Session()
    s.headers.update({'User-Agent': user_agent})
    login(s)
    with open('links_in.txt','r') as inputFile:
        prior_generated_link = getGeneratedLink(s)
        for original_link in inputFile:
            message_body = buildMessageBody(s, original_link)
            sendChatMessage(s, message_body)
            time.sleep(1)
            failed = True
            num_attempts = 0
            while failed == True:
                if num_attempts == 15: # Re-submit request
                    sendChatMessage(s, message_body)
                    num_attempts = 0
                    continue
                generated_link = getGeneratedLink(s)
                if generated_link != prior_generated_link:
                    with open('links_out.txt', 'a+') as output_file:
                        output_file.write(generated_link + '\n')
                    failed = False
                    prior_generated_link = generated_link
                    num_attempts = 0
                else:
                    num_attempts += 1
                    if failed == True:
                        time.sleep(1)

if __name__ == '__main__':
    main()
