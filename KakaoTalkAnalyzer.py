
filename = "분석파일폴더\\분석용.txt"
f = open(filename,'r',encoding='UTF8')
title = ""
users = {}

keywords = {}
dates = {}
fileSize = f.read().count("\n")+1
f.close()
f = open(filename,'r',encoding='UTF8')

def parseChat():
    global title
    percent = 10
    countChats = 0
    dateTemp = ""
    parsedChats = 0
    
    line = f.readline()
    title = line[:line.find('님과 카카오톡 대화')]

    line = f.readline()
    line = f.readline()

    parsedChats+=3
    nickN = "" #가장 최근 메세지 보낸 사람
    while True:
        
        line = f.readline()
        if not line: 
            dates.update({dateTemp:countChats})
            break


        if line.startswith('-------'):  #날짜
            dates.update({dateTemp:countChats})
            countChats = 0
            dateTemp = line.replace('---------------','').replace(' \n','')[1:]


        elif line.startswith('[') and line.find('[',1) != -1:  #한줄로된 메세지
            nickN = line[1:line.find(']')]
            if users.get(nickN) == None:
                users.update({nickN:1})
            else:
                users[nickN] += 1
            content = line[line.find(']',line.find(']')+1)+1:]
            nouns = content.split(" ")

            for noun in nouns:
                noun = noun.replace('\n','').replace(' ','')
                if noun == '사진' or noun == '이모티콘' or noun == '삭제된' or noun == '메시지입니다.' or noun == '샵검색':
                    continue
                
                    
                if keywords.get(noun) == None:
                    keywords.update({noun:1})
                else:
                    keywords[noun]+=1
            countChats+=1


        elif '님이 나갔습니다.' in line or '님이 들어왔습니다.' in line or '님을 내보냈습니다.' in line: #출입 메세지
            pass


        else:   #엔터가 들어가있는 메세지
            pass


        parsedChats+=1
        
        if int((parsedChats/fileSize)*100) == percent:
            percent+=10
            print("파싱중입니다. {}% 완료".format(percent-10))
    f.close()


parseChat()
userRank = sorted(users.items(), key=lambda x: x[1],reverse=True)
dateRank = sorted(dates.items(), key=lambda x: x[1],reverse=True)
wordsRank = sorted(keywords.items(),key = lambda x: x[1],reverse = True)[1:]
print('---------- {}님과의/에서의 채팅 분석 ----------'.format(title))
print('---------- 가장 메세지를 많이 보낸 사람 ----------')
t = 1
for i in userRank:

    print('{}.  {} : {}'.format(t, i[0],i[1]))
    t+=1

print('---------- 방이 가장 활발했던 날 ----------')
x = int(input('몇번째 순위까지 보시겠습니까? : '))
t = 1
for i in dateRank:
    print('{}.  {} : {}개'.format(t,i[0],i[1]))
    t+=1
    if t == x+1: break

print('---------- 가장 많이 쓰인 단어 ----------')
x = int(input('몇번째 순위까지 보시겠습니까? : '))
t = 1
for i in wordsRank:
    print('{}.  {} : {}개'.format(t,i[0],i[1]))
    t+=1
    if t == x+1: break
while True:
    x = input('키워드를 찾으시겠습니까? y/n : ')
    if x == 'y':
        y = input('찾을 단어를 입력해주세요 : ')
        for i in wordsRank:
            if y in i[0]:
                print(i)
    else:
        break
