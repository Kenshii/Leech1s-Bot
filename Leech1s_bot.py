'''
This script takes the list of links, from links_in.txt.
Premium links are then generated and outputted to links_out.txt
'''

import requests, json, time
from bs4 import BeautifulSoup

loginData = {
    'pword': '<chat password>',
    'sublog': 'Log in'
}

messageSubmissionData = {
    'nme': '<chat username>',
    'key': 'bf4a9597e5897f442',
    'pst': '',
}

loginHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'clid_2352971=2; nme_2352971=' + messageSubmissionData['nme']
}

messageSubmissionHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
}

s = requests.Session()
s.post('http://www2.cbox.ws/box/?boxid=2352971&boxtag=ltttao&sec=profile&n=' + messageSubmissionData['nme'] + '&k=' + messageSubmissionData['key'], data = loginData, headers = loginHeaders)
messageSubmissionData['key'] = s.cookies['key_2352971']
with open('links_in.txt','r') as inputFile:
    priorGeneratedLink = ''
    priorChatMsgs = requests.get('http://www2.cbox.ws/box/?boxid=2352971&boxtag=ltttao&sec=main')
    priorChatSoup = BeautifulSoup(priorChatMsgs.text, 'html.parser')
    priorMsgsSentToUser = priorChatSoup(text = ' ' + messageSubmissionData['nme'] + ' ')
    if priorMsgsSentToUser:
        priorGeneratedLinkAnchor = priorMsgsSentToUser[0].parent.parent.parent.find('a', {'class' : 'bbURL'})
        if priorGeneratedLinkAnchor:
            priorGeneratedLink = priorGeneratedLinkAnchor['href']
    for originalLink in inputFile:
        linkCheckResp = s.post('http://cdn.leech1s.com/autocheck/ch.php?links=' + originalLink)
        linkInfo = json.loads(linkCheckResp.text[1 : -1])
        messageSubmissionData['pst'] = '[center] ' + linkInfo['link'] + ' link_live  | [color=#CD0000][b] ' + linkInfo['filename'] + ' [/b][/color]  | [color=black][b] ' + linkInfo['filesize'] + ' [/b][/color][br][den]Checked By[/mau] [vang] F.A Team [/mau] [/center]  [sub](sent from Ireland)[/sub]',
        # Submit link request (chat message)
        s.post('http://www2.cbox.ws/box/index.php?boxid=2352971&boxtag=ltttao&sec=submit', data = messageSubmissionData, headers = messageSubmissionHeaders)

        time.sleep(1)
        failed = True
        num_attempts = 0
        while failed == True:
            if num_attempts < 15: # There is a lot of nesting here, now that I look at it again.
                newChatMsgs = requests.get('http://www2.cbox.ws/box/?boxid=2352971&boxtag=ltttao&sec=main')
                newChatSoup = BeautifulSoup(newChatMsgs.text, 'html.parser')
                newMsgsSentToUser = newChatSoup(text = ' ' + messageSubmissionData['nme'] + ' ')
                if newMsgsSentToUser:
                    generatedLinkAnchor = newMsgsSentToUser[0].parent.parent.parent.find('a', {'class' : 'bbURL'})
                    if generatedLinkAnchor:
                        generatedLink = generatedLinkAnchor['href']
                        if generatedLink != priorGeneratedLink:
                            with open('links_out.txt', 'a+') as outputFile:
                                outputFile.write(generatedLink + '\n')
                            failed = False
                            priorGeneratedLink = generatedLink
                            num_attempts = 0
            else:
                # Re-submit link request (chat message)
                s.post('http://www2.cbox.ws/box/index.php?boxid=2352971&boxtag=ltttao&sec=submit', data = messageSubmissionData, headers = messageSubmissionHeaders)
                num_attempts = 0
            num_attempts += 1
            if failed == True:
                time.sleep(1)
