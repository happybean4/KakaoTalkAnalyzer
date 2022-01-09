users = {} #유저별 메세지 보낸 갯수 { 이름 : 갯수 }
emoticon = {} #유저별 이모티콘 보낸 갯수 { 이름 : 갯수 }
keywords = {} #띄어쓰기로 구분된 단어 개별 갯수 { 단어 : 갯수 }
photo = {} #유저별 사진 보낸 갯수 { 이름 : 갯수 }
dates = {} #날짜별 메세지 갯수 { 날짜 : 갯수 }
mention = {} #유저별 멘션 갯수 { 이름 : 갯수 }
receiverRankingByUser = {} #특정 사람의 대화를 받아준 사람 목록 { 이름 : { '이름'의 대화 받아준 사람 이름 : 갯수 } }
senderRankingByUser = {} #특정 사람이 대화를 받아준 사람 목록 { 이름 : {'이름'이 대화를 받아준 사람 이름 : 갯수 } }
times = {'오전 1': 0, '오후 1': 0, '오전 2': 0, '오후 2': 0, '오전 3': 0, '오후 3': 0, '오전 4': 0, '오후 4': 0, '오전 5': 0, '오후 5': 0, '오전 6': 0, '오후 6': 0, '오전 7': 0, '오후 7': 0, '오전 8': 0, '오후 8': 0, '오전 9': 0, '오후 9': 0, '오전 10': 0, '오후 10': 0, '오전 11': 0, '오후 11': 0, '오전 12': 0, '오후 12': 0}
totalSum = 0 #전체 메세지 갯수




filename = "분석파일폴더\\분석용.txt"
f = open(filename,'r',encoding='UTF8')
title = ""
fileSize = f.read().count("\n")+1
f.close()
f = open(filename,'r',encoding='UTF8')

def parseChat():
    global totalSum
    global title
    percent = 10
    countChats = 0
    dateTemp = ""
    parsedChats = 0
    
    line = f.readline()
    title = line[:line.find('님과 카카오톡 대화')]

    line = f.readline()
    line = f.readline()
    pastSender = ''
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


            if pastSender == '': pastSender = nickN
            elif pastSender != nickN:
                if receiverRankingByUser.get(pastSender) == None:
                    receiverRankingByUser.update({pastSender:{'1coun2t3' : 1,nickN:1}}) # 1coun2t3 : 어떻게 사람 이름이 1coun2t3 ㅋㅋ
                else:
                    if receiverRankingByUser[pastSender].get(nickN) == None:
                        receiverRankingByUser[pastSender].update({nickN:1})
                    else:
                        receiverRankingByUser[pastSender][nickN] +=1
                    receiverRankingByUser[pastSender]['1coun2t3'] +=1

                
                if senderRankingByUser.get(nickN) == None:
                    senderRankingByUser.update({nickN:{'1c2o3u4n5t' : 1,pastSender:1}})
                else:
                    if senderRankingByUser[nickN].get(pastSender) == None:
                        senderRankingByUser[nickN].update({pastSender:1})
                    else:
                        senderRankingByUser[nickN][pastSender]+=1
                    senderRankingByUser[nickN]['1c2o3u4n5t'] +=1
            pastSender = nickN


                
            if users.get(nickN) == None:
                users.update({nickN:1})
            else:
                users[nickN] += 1


            
            content = line[line.find(']',line.find(']')+1)+1:]
            nouns = content.split(" ")
            time = line[line.find('[',line.find('[')+1)+1:line.find(':')]
            times[time]+=1


            for noun in nouns:
                noun = noun.replace('\n','').replace(' ','')
                if  noun == '삭제된' or noun == '메시지입니다.' or noun == '샵검색':
                    continue
                if noun == '이모티콘':
                    if emoticon.get(nickN) == None:
                        emoticon.update({nickN:1})
                    else:
                        emoticon[nickN]+=1
                    continue
                if noun == '사진':
                    if photo.get(nickN) == None:
                        photo.update({nickN:1})
                    else:
                        photo[nickN] +=1
                    continue

                if '@' in noun:
                    if mention.get(nickN) == None:
                        mention.update({nickN:1})
                    else:
                        mention[nickN] +=1
                    continue
                if keywords.get(noun) == None:
                    keywords.update({noun:1})
                else:
                    keywords[noun]+=1
            countChats+=1
            totalSum+=1

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
timeRank = sorted(times.items(),key = lambda x: x[1], reverse= True)[1:]


print('---------- {}님과의/에서의 채팅 분석 ----------'.format(title))
t = 1
print('전체 메세지 갯수 : {}'.format(totalSum))



while True:
    print('---------------------------------------------------------------')
    print("1. 대화 참여자 랭킹 보기")
    print("2. 키워드 랭킹 보기")
    print('3. 가장 톡방이 활발한 시간 보기')
    print("4. 가장 톡방이 활발했던 날짜 보기")
    print("5. 특정 사람의 대화를 받아준 사람의 랭킹 보기")
    print("6. 특정 사람이 누구의 대화를 잘 받아줬는지에 대한 랭킹 보기")
    print('7. 키워드 찾기')
    print('---------------------------------------------------------------')
    x = int(input())
    if x == 1:
        print('---------- 가장 메세지를 많이 보낸 사람 ----------')
        for i in userRank:
            
            print('{}.  {} : {} / 비율 : {}%'.format(t, i[0],i[1], "%.2f" % (100.0 * i[1] / totalSum)))
            t+=1
    if x == 2:
        print('---------- 가장 많이 쓰인 단어 ----------')
        x = int(input('몇번째 순위까지 보시겠습니까? : '))
        t = 1
        for i in wordsRank:
            print('{}.  {} : {}개'.format(t,i[0],i[1]))
            t+=1
            if t == x+1: break
    if x == 3:
        print('---------- 방이 가장 활발한 시간 ----------')
        t = 1
        for i in timeRank:
            print('{}. {}시 : {}'.format( t, i[0],i[1]))
            t+=1
    if x == 4:
        print('---------- 방이 가장 활발했던 날 ----------')
        x = int(input('몇번째 순위까지 보시겠습니까? : '))
        t = 1
        for i in dateRank:
            print('{}.  {} : {}개'.format(t,i[0],i[1]))
            t+=1
            if t == x+1: break
    if x == 5:
        y = input('확인하고 싶은 사람의 이름을 입력해주세요 : ')
        if receiverRankingByUser.get(y) == None:
            print("채팅방에 없는 사람이거나 대화를 한 번도 하지 않은 사람입니다.")
        else:
            rank = sorted(receiverRankingByUser[y].items(), key=lambda x: x[1],reverse=True)
            t = 1
            messageSum = 0
            print('{}님의 대화를 받아준 사람'.format(y))
            for i in rank:
                if i[0] == '1coun2t3':
                    messageSum = i[1]
                    continue
                print('{}.  {} : {} / 비율 : {}%'.format(t, i[0],i[1], "%.2f" % (100.0 * i[1] / messageSum)))
                t+=1
    if x == 6:
        y = input('확인하고 싶은 사람의 이름을 입력해주세요 : ')
        if senderRankingByUser.get(y) == None:
            print("채팅방에 없는 사람이거나 대화를 한 번도 하지 않은 사람입니다.")
        else:
            rank = sorted(senderRankingByUser[y].items(), key=lambda x: x[1],reverse=True)
            t = 1
            messageSum = 0
            print('{}님이 대화를 받아준 사람'.format(y))
            for i in rank:
                if i[0] == '1c2o3u4n5t':
                    messageSum = i[1]
                    continue
                print('{}.  {} : {} / 비율 : {}%'.format(t, i[0],i[1], "%.2f" % (100.0 * i[1] / messageSum)))
                t+=1
    if x == 7:
        y = input('찾을 단어를 입력해주세요 : ')
        for i in wordsRank:
            if y in i[0]:
                print(i)