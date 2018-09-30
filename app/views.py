from django.shortcuts import render
import requests
import wikiquotes
from watson_developer_cloud import ToneAnalyzerV3
import json
from aylienapiclient import textapi
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
import requests
# @csrf_exempt
def get_image(request):
    if request.method == 'POST':
        img = request.FILES.get("image")
        path = default_storage.save('mrcaption/image', ContentFile(img.read()))
        print (request.FILES)
        headers  = {'Ocp-Apim-Subscription-Key': '2593b2ee7a9345c7823c2dd3df0f028d',
        "Content-Type": "application/octet-stream" }
        image_data = open(path , "rb").read()
        vision_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=Categories,Tags&language=en"
        response = requests.post(vision_url, headers=headers, data=image_data)
        data = response.json()
        print (data)       
        
    #     li = []
    # for d in data['tags']:
    #     li.append(d['name'])
        
    # print(li)
    # cap = []
    # count=0
    # for i in li:
    #     count+=1
    #     if(count<4):
    #         dd = wikiquotes.get_quotes(i, "english")
    #         cap.append(dd[0])
    # print(cap)

    # tone_analyzer = ToneAnalyzerV3(
    #     username='09ad450e-eb00-4ef4-a6ab-e51093e505c4',
    #     password='kGnXm8HrMFWw',
    # version='2017-09-26')

    # for c in cap:
    #     utterances = [{'text': c, 'user': 'trailblazerr'}]    
    #     rtone=  tone_analyzer.tone_chat(utterances)
    #     #print(type(rtone))
    #     sent = rtone["utterances_tone"][0]["tones"][0]["tone_name"]
    #     # if(srtone["utterances_tone"][0]["tones"])
        
        
    # client = textapi.Client(" 016eb657", " 590dff367360e75235f3753b78ef1488")
    # sentiment = client.Hashtags({'text': cap[0]})
    # hashtag = sentiment['hashtags']
    
    # dictt = {}

    # dictt = {"quotes" : cap , 
    # "sent" : sent,
    # "hashtag" : hashtag}
    # print (dictt)
    li = []




    for d in data['tags']:
        li.append(d['name'])
        
    print(li)
    cap = []
    count=0
    for i in li:
        count+=1
        if(count<3):
            dd = wikiquotes.get_quotes(i, "english")
            #print(type(dd[0]))
            qq = dd[0].replace('\n', ' ')
            cap.append(qq)
    print(cap)

    tone_analyzer = ToneAnalyzerV3(
        username='09ad450e-eb00-4ef4-a6ab-e51093e505c4',
        password='kGnXm8HrMFWw',
    version='2017-09-26')
    client = textapi.Client(" 016eb657", " 590dff367360e75235f3753b78ef1488")

    ret = []
    i=0
    hsh=[]
    for c in cap:
        utterances = [{'text': c, 'user': 'trailblazerr'}]    
        rtone=  tone_analyzer.tone_chat(utterances)
        #print(rtone["utterances_tone"][0]["tones"])
        sent = rtone["utterances_tone"][0]["tones"]
        hh = requests.get("https://api.ritekit.com/v1/stats/hashtag-suggestions/"+li[i]+"?client_id=438d12f890281e8fde7f206aeea377f3a07a902286fb")
        h = hh.json()
        #print(type(h))
        hashtag = h["data"]
        i+=1
        for hashta in hashtag:
            hsh.append("#"+hashta["hashtag"])
        ret.append({"quote": c,"sent": sent,"hashtag":hsh})
    
    print(ret)
    return JsonResponse(ret, safe=False)







