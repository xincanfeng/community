# 本算法将收集到等客户信息实时存储在表格中，并从表格中读取数据，自动计算并生成适合开展网上料理教室的报告单。
# 接下来计划将优化数据分析方法，并将分析结果通过图像和表格等方式表示出来，增加说服力。

# import pandas as pd
# import numpy as np
# import datetime as dt
import random

# ---------------------------------------------------
# input of cooker:
# firstName: taro
# lastName: naist
# age: 30
# gender: M
# area: ikoma
# favoriteMeetingTime: 20:00-20:30
# recipeType: asian
# preferredIngredient: fish
# experienceYear: 10
# price: 1000 / 30m

# cookers =[[cookerId, age, experienceYear, ...]]
# cookers = [
#     ['6', 'mitsuki', 'hoshino', 35, 'F', np.nan, 2300, 'italian', 'tomato', 9],
#     ['7', 'hajime', 'aragawa', 40, 'M', np.nan, 2230, 'chinese', 'pork', 11]]

# ---------------------------------------------------
# input of user:
# firstName: taro
# lastName: naist
# age: 30
# gender: M
# area: ikoma
# favoriteMeetingTime: 20:00-20:30
# recipeType: asian
# preferredIngredient: fish
# experienceYear: 10

# users =[[userId, age, gender, area, favoriteMeetingTime, ...]]
# users  = [
#     ['1', 'taro', 'naist', 18, 'F', np.nan, 2300, 'okinawa', 'fish', 1], 
#     ['2', 'ichiro', 'naist', 20, 'M', np.nan, 1830, 'chinese', 'pork', 3], 
#     ['3', 'saburo', 'naist', 22, 'F', np.nan, 2000, 'sichuan', 'liver', 5], 
#     ['5', 'kogoro', 'mori', 24, 'M', np.nan, 2100, 'italian', 'tomato', 7]]

# ---------------------------------------------------
# followers
# followers = [
#     ['6', '1', '5'],
#     ['7', '2', '3']]

# ---------------------------------------------------
# if userClickFollow:
#     followerNumber += 1

cookersPath = '/Users/xincan-f/Documents/ceci/Naist/my project/community/cookers.tsv'
usersPath = '/Users/xincan-f/Documents/ceci/Naist/my project/community/users.tsv'
followersPath = '/Users/xincan-f/Documents/ceci/Naist/my project/community/followers.tsv'
followers1BeforePath = '/Users/xincan-f/Documents/ceci/Naist/my project/community/followers1Before.tsv'

cookers = []
users = []
followers = {} 
followers1Before = {}
followersNum = {}
# meet = False
meetingReport = {} 

with open(cookersPath) as fCookers:
    for item in fCookers:
        cookers.append(item.strip().split('\t'))
# print(cookers)

with open(usersPath) as fUsers:
    for item in fUsers:
        users.append(item.strip().split('\t'))

# save current followers information in a dictionary
with open(followersPath) as fFollowers:
    userId = []
    for item in fFollowers:
        cookerId = item[0]
        usersId = item.strip().split('\t')[1:]
        followers[cookerId] = []
        for item in usersId:
            followers[cookerId].append(item)
# print(followers)

# save 1 month before followers information in a dictionary
with open(followers1BeforePath) as fFollowers1Before:
    userId = []
    for item in fFollowers1Before:
        cookerId = item[0]
        usersId = item.strip().split('\t')[1:]
        followers1Before[cookerId] = []
        for item in usersId:
            followers1Before[cookerId].append(item)
# print(followers1Before)

# save followers number in before-current sequence
# for item in followers1Before:
#     cookerId = item[0]
#     followersNum[cookerId] = []
#     followersNum[cookerId].append(len(followers1Before[cookerId]))
#     if cookerId in followers:
#         followersNum[cookerId].append(len(followers[cookerId]))
# print(followersNum)

# save followers number in current-before sequence
for item in followers:
    cookerId = item[0]
    followersNum[cookerId] = []
    followersNum[cookerId].append(len(followers[cookerId]))
    if cookerId in followers1Before:
        followersNum[cookerId].append(len(followers1Before[cookerId]))
# print(followersNum)

# save meeting report into a dictionary:
# 1) meetingNum, 
# 2) cookerId, cooker, cookerPayment, 
# 3) participantsId, participants, participantsNum, participationFeeTotal, participationFeePerPerson, 
# 4) meetingDateTime, meetingPlace

for item in followersNum:
    participants = []
    participantsDateTime = []
    # get ID of the cookers who is able to hold a meeting:
    if followersNum[item][0] >= followersNum[item][1] * 2:
        # meet = True
        # 1) append hashed meetingNum to the meeting report
        hash = random.getrandbits(128)
        meetingReport[hash] = []
        cookerId = item

        # 2-1) append cookerId to the meeting report
        meetingReport[hash].append(cookerId)

        # 2-2) append cooker to the meeting report
        # cooker = fisrtName + lastName
        for i in range(0, len(cookers)):
            if cookers[i][0] == cookerId:
                cooker = cookers[i][1] + ' ' + cookers[i][2]
                meetingReport[hash].append(cooker)
                # 2-3) append cooker's price to the meeting report
                cookerPrice = cookers[i][10]
                meetingReport[hash].append(cookerPrice)

        # 3-1) append participantsId to the meeting report
        # participants: only all the followers are hypothesized
        # but other users are also possible
        # also, followers may not participate
        participantsId = followers[cookerId]
        meetingReport[hash].append(participantsId)

        # 3-2) append users to the participants
        # append participants to the meeting report
        for j in range(0, len(users)):
            if users[j][0] in participantsId:
                participants.append(users[j][1] + ' ' + users[j][2])
                # 4-1)' recoreding the participantsDateTime
                participantsDateTime.append(users[j][6])
        meetingReport[hash].append(participants)

        # 3-3) append participantsNum to the meeting report
        meetingReport[hash].append(len(participants))

        # 3-4) append participationFeeTotal to the meeting report
        # the participationFeeTotal now equals to cookerPrice, but it actually should be revised
        participationFeeTotal = cookerPrice
        meetingReport[hash].append(participationFeeTotal)

        # 3-5) append participationFeePerPerson to the meeting report
        participationFeePerPerson = int(int(participationFeeTotal) / len(participants))
        meetingReport[hash].append(participationFeePerPerson)

        # 4-1) append meetingDateTime to the meeting report
        # sort participantsDateTime by frequency, choose the element that has the highest frequency
        sortedParticipantsDateTime = sorted(participantsDateTime, key = participantsDateTime.count, reverse = True)
        meetingDateTime = sortedParticipantsDateTime[0]
        meetingReport[hash].append(meetingDateTime)

        # 4-2) append meetingPlace to the meeting report
        meetingPlace = 'zoom'
        meetingReport[hash].append(meetingPlace)
# print(meetingReport)

# print in format
for item in meetingReport:
    print('\n' + 'Report of MeetingNum' + ': ' + str(item))
    print('-------------------------------------------------------------')
    print('cookerId' + ': ' + meetingReport[item][0])
    print('cooker' + ': ' + meetingReport[item][1])
    print('cookerPayment' + ': ' + meetingReport[item][2])
    print('participantsId' + ': ' + ', '.join(meetingReport[item][3]))
    print('participants' + ': ' + ', '.join(meetingReport[item][4]))
    print('participantsNum' + ': ' + str(meetingReport[item][5]))
    print('participationFeeTotal' + ': ' + meetingReport[item][6])
    print('participationFeePerPerson' + ': ' + str(meetingReport[item][7]))
    print('meetingDateTime' + ': ' + meetingReport[item][8])
    print('meetingPlace' + ': ' + meetingReport[item][9])
    print('\n')





