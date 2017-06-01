import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import codecs
import numpy as np

import lda
import config

tweetsFile = codecs.open('tweets/tweets.txt', 'r', encoding='utf-8').read()

style.use('fivethirtyeight')

fig1, ax1 = plt.subplots()
ax1.pie([], labels=[], autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

totalDict = {}

def visualize(topicDict):
    total = sum(topicDict.values())
    
    labels = []
    sizes = []
    colors = []
    
    for key in topicDict.keys():
        labels.append(key)
        #sizes.append(100.0 * topicDict[key] / total)
        sizes.append(topicDict[key])
        colors.append(config.colorDict[key])
         
    
    ax1.clear()
    
    ind = np.arange(len(labels))
    width = 0.35 
    ax1.set_xticks(ind + width/2.)
    ax1.set_xticklabels(topicDict.keys())
    
    #ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',shadow=True, startangle=90)
    plt.bar(ind, sizes, width, align='center', color=(0.2588,0.4433,1.0))




def animate(i):
    tweetsStream = tweetsFile.split('###')
    print(tweetsStream)
    
    tweets = tweetsStream[-2:]
    print(tweets)
    
    topicDict = lda.createTopicDictionary(tweetsStream, config.food_style_topics)
    print(topicDict)
    
    for key in topicDict.keys():
        if(key in totalDict.keys()):
            totalDict[key] = totalDict[key] + topicDict[key]
        else:
            totalDict.update({key: topicDict[key]})
    
    #visualize(topicDict)


ani = animation.FuncAnimation(fig1, animate, interval=1000)
plt.show()

