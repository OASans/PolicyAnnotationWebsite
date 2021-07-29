#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.shortcuts import redirect
import json
import re
import os
from itertools import chain

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.http import FileResponse

from django.http import JsonResponse

from . import models
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

num_per = 5
##### TODO:

policy_starts = models.PolicySentence.objects.filter(sentence_id=1)
num_policy = policy_starts.count()
policy_ids = [m.example_id for m in policy_starts]

# bio_dict = {0:'0:O',1:'1:I',2:'2:B-症状',3:'3:B-药品名',4:'4:B-药物类别',
#     5:'5:B-服用方式等',6:'6:B-检查',7:'7:B-操作',8:'8:B-注意事项'}

# act_dict = {1:'症状',2:'基本信息',3:'已有检查和治疗',4:'用药建议',
# 5:'就医建议',6:'注意事项',7:'其他'}


sections1 = models.LabelClass.objects.all()
bio_dict = {}
res1 = []
for i in sections1:
    bio_dict[i.labelid] = i.labelmeaning
    res1.append([i.labelid, i.labelmeaning])

sections2 = models.ActClass.objects.all()
act_dict={}
res2 = []
for i in sections2:
    act_dict[i.aid]=i.actid
    res2.append([i.aid, i.actid])
    

def taghome(request):
    return redirect('/login/')


def index(request):
    if request.session.get('is_login', None):
        reviewerid = request.session['userid']
        print('reviewerid:',reviewerid)
        lasttext = models.PolicySentenceTag.objects.filter(reviewer=reviewerid).order_by('-savedate')

        userstart = models.PolicyTagger.objects.get(id=reviewerid).start
        userend = models.PolicyTagger.objects.get(id=reviewerid).end
        start_index = policy_ids.index(userstart)
        end_index = policy_ids.index(userend)
        text_exist = lasttext.exists()
        if text_exist:
            unique_list = models.PolicySentenceTag.objects.filter(reviewer=reviewerid,sentence_id=1).order_by('savedate').values('unique_id')
            complete_text = len(list(unique_list))
            total_text = end_index-start_index+1
            complete_percent = int((complete_text/total_text)*100)
            undo_text = end_index-start_index-complete_text+1
            undo_percent = int((undo_text/total_text)*100)
            return render(request, 'index.html', {'complete': complete_text,'percent1':complete_percent,'undo':undo_text,'percent2':undo_percent})
        else:
            last_textid = 0
            undo_text = end_index-start_index+1
            complete_percent = 0
            undo_percent = 100
            return render(request, 'index.html', {'complete': last_textid, 'percent1': complete_percent, 'undo': undo_text,'percent2': undo_percent})

    else:
        message = "您尚未登陆！"
        return render(request, 'page-login.html', {'message': message})


# 标注规范页
def example1(request):
    if request.session.get('is_login', None):
        return render(request, 'example1.html')
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})


# 标注示例页，TODO
def example2(request):
    if request.session.get('is_login', None):
        return render(request, 'example2.html')
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})


# 标注示例页，TODO
def example3(request):
    if request.session.get('is_login', None):
        return render(request, 'example3.html')
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})


@csrf_exempt
def policy_login(request):
    if request.session.get('is_login', None): # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:#用户名和密码非空
            try:
                print('username:',username)
                user = models.PolicyTagger.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'page-login.html', {'message': message})

            if user.password == password:
                #print(username, password)
                request.session.set_expiry(0)
                request.session['is_login'] = True
                request.session['userid'] = user.id
                request.session['username'] = user.name
                request.session['userstart'] = user.start
                request.session['userend'] = user.end
                return redirect("/index/")

            else:
                message = '密码不正确！'
                return render(request, 'page-login.html', {'message': message})
        else:
            message = '用户名和密码不能为空'
            return render(request, 'page-login.html', {'message': message})
    return render(request, 'page-login.html')


@csrf_exempt
def policy_tagging(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    # 先确定标注用户，此时标注内容
    reviewerid = request.session['userid']
    # print('reviewerid:',reviewerid)
    lasttext = models.PolicySentenceTag.objects.filter(reviewer=reviewerid, sentence_id=1).order_by('-savedate')
    text_exist = lasttext.exists()

    userstart = models.PolicyTagger.objects.get(id=reviewerid).start
    topid = models.PolicyTagger.objects.get(id=reviewerid).end  # end 是example_id

    if not text_exist:  # 尚未开始标注
        now_id = userstart

    else:  # 已有标注记录
        # 得到已标记的exampid 在 dia_act 中的index
        id_exist = [i.example_id for i in lasttext]
        id_nopermission = [i.example_id for i in lasttext if (i.permissions==None and i.sentence_tag=='准入条件')]

        id_exist_set = set(id_exist)
        id_nopermission_set = set(id_nopermission)
        if list(id_nopermission_set) != []:
            example_id = list(id_nopermission_set)[0]
            tag_info = models.PolicySentenceTag.objects.filter(example_id=example_id, reviewer=reviewerid,
                                                               sentence_tag='准入条件')
            sentences = [tag.sentence for tag in tag_info]
            uids = [tag.unique_id for tag in tag_info]
            permission_sentences = zip(uids, sentences)
            return render(request, 'policy_permission.html', {
                'message': '以下为您选择的准入条件句子，请开始标注四元组',
                'nowtext_id': example_id, 'permission_sentence': permission_sentences})

        id_all = [i for i in policy_ids[policy_ids.index(userstart): policy_ids.index(topid) + 1]]
        id_no = []
        for eid in id_all:
            if eid not in id_exist_set:
                id_no.append(eid)

        if id_no != []:
            now_id = id_no[0]
        else:
            return render(request, 'policy_complete.html', {'message': '您已完成当前所有标注任务', 'from': 'tag'})

    nowtext0 = models.PolicySentence.objects.filter(example_id=now_id)
    cutted_text = [i.sentence for i in nowtext0]  # cutsent(nowtext)
    uid = [i.unique_id for i in nowtext0]

    label = []
    for i in nowtext0:
        label.append(['1'] * len(i.sentence))

    lenpos = [dict(zip(range(1, len(i) + 1), [bio_dict[j] for j in i])) for i in label]
    acts = ['请选择类别' for i in nowtext0]
    cutted = zip(uid, cutted_text, acts, lenpos)

    whole_policy = models.PolicyText.objects.get(example_id=now_id).text
    return render(request, 'new_policy_tag.html', {'whole_policy': whole_policy,
                                        'nowtext_id': now_id, 'cutted': cutted, 'sections_BIO': res1,
                                        'sections_ACT': res2, 'lenpos': lenpos})
    # TODO：换了新的tagging页面


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def check(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    reviewerid = request.session['userid']
    lasttext = models.PolicySentenceTag.objects.filter(reviewer=reviewerid).order_by('-savedate')
    text_exist = lasttext.exists()
    if not text_exist: #尚未开始标注
        message = "您尚未开始标注!"
        return render(request, 'check.html', {'message': message})
    else: #已有标注记录
        message = "您标注过以下文本："
        textlist = models.PolicySentenceTag.objects.filter(reviewer=reviewerid, sentence_id=1).order_by('-savedate')
        example_ids = [i.example_id for i in textlist]
        # unique_ids = [i.unique_id for i in textlist]
        policies = [models.PolicyText.objects.get(example_id=i).text[0] for i in example_ids]
        savetime = [models.PolicySentenceTag.objects.get(reviewer=reviewerid, sentence_id=1, example_id=i).savedate for i in example_ids]

        tagged = zip(example_ids, policies, savetime)
        return render(request,'check.html', {'tagged':tagged,'message': message})


@csrf_exempt
def lookandmodify(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    eid = request.POST.get('eid', None)

    reviewer = request.session['userid']

    TagData = models.PolicySentenceTag.objects.filter(example_id=eid, reviewer=reviewer)
    cutted_text = [i.sentence for i in TagData]  # cutsent(nowtext)
    uid = [i.unique_id for i in TagData]

    label = []
    for i in TagData:
        try:
            add_ = list(i.label)
        except:
            add_ = []
        label.append(add_)

    lenpos = [dict(zip(range(1, len(i) + 1), [bio_dict[j] for j in i])) for i in label]

    acts = [i.sentence_tag for i in TagData]

    cutted = zip(uid, cutted_text, acts, lenpos)

    whole_policy = models.PolicyText.objects.get(example_id=eid).text

    return render(request, 'policy_modify.html', {'whole_policy': whole_policy,
                                               'nowtext_id': eid, 'cutted': cutted, 'sections_BIO': res1,
                                               'sections_ACT': res2, 'lenpos': lenpos})


@csrf_exempt
def modifytag(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    userid = request.session['userid']

    if request.is_ajax():
        example_id = request.POST.get('example_id', None)
        sentence_id = request.POST.get('sent_id', None)
        sent_act = request.POST.get('sent_act', None)
        Bios = request.POST.get('Bios', None)

    search_dict = dict()
    search_dict['example_id'] = example_id
    search_dict['sentence_id'] = sentence_id
    search_dict['reviewer'] = userid

    user_tag_info = models.PolicySentenceTag.objects.filter(**search_dict)
    rawlabel = models.PolicySentenceTag.objects.get(**search_dict).label
    label = ''
    for i, w in enumerate(Bios):
        if w != '*':
            label += w
        else:
            label += rawlabel[i]

    data = {'label': label, 'sentence_tag': sent_act}
    user_tag_info.update(**data)

    return HttpResponse(json.dumps({"msg": 'success'}))


@csrf_exempt
def savetag(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    userid = request.session['userid']
    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)
        sentid = request.POST.get('sentid', None)
        ActBios = request.POST.get('ActBios', None)

    unique_id = str(nowtextid) + '_' + sentid
    rawdata = models.PolicySentence.objects.get(unique_id=unique_id)
    sentence = rawdata.sentence

    search_dict = dict()
    if nowtextid:
        search_dict['unique_id'] = unique_id
    # if sentid:
    #     search_dict['sentence_id'] = sentid
    if userid:
        search_dict['reviewer'] = userid

    user_tag_info = models.PolicySentenceTag.objects.filter(**search_dict)
    text_exist = user_tag_info.exists()

    # print('default:',default_label)
    # print('ActBios:',ActBios)

    label = ActBios[1:]

    sentence_act = ActBios[:1]

    if text_exist:
        data = {'label': label, 'sentence_act': sentence_act}
        user_tag_info.update(**data)
    else:
        new_tag = models.PolicySentenceTag()
        new_tag.example_id = nowtextid
        # print('*********savetag:*********',new_tag.example_id)
        new_tag.unique_id = unique_id
        new_tag.sentence_id = sentid
        new_tag.sentence = sentence

        new_tag.label = label
        if sentence_act != '*':
            new_tag.sentence_tag = act_dict[sentence_act]  # act_dict[int(dialogue_act)]
        else:
            new_tag.sentence_tag = '未标记'
        new_tag.reviewer = userid
        # print('*********savetag:*********',new_tag.sentence_id, new_tag.dialogue_act)
        new_tag.save()
    return HttpResponse(json.dumps({"msg": 'success'}))


@csrf_exempt
def savepermissions(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    userid = request.session['userid']
    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)
        objects = request.POST.get('objects', None)
        vars = request.POST.get('vars', None)
        relations = request.POST.get('relations', None)
        fields = request.POST.get('fields', None)

    unique_id = str(nowtextid)
    data_tagged = models.PolicySentenceTag.objects.get(unique_id=unique_id, reviewer=userid)

    objects = objects.strip().split(' ')
    vars = vars.strip().split(' ')
    relations = relations.strip().split(' ')
    fields = fields.strip().split(' ')
    permissions = []
    for o,v,r,f in zip(objects, vars, relations, fields):
        permissions.append((o,v,r,f))

    # add_data = {'permissions': permissions}
    # data_tagged.update(**add_data)
    data_tagged.permissions = permissions
    data_tagged.save(update_fields=['permissions'])

    return HttpResponse(json.dumps({"msg": 'success'}))


@csrf_exempt
def permission(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    reviewerid = request.session['userid']
    if request.is_ajax():
        example_id = request.POST.get('textid', None)
        tag_info = models.PolicySentenceTag.objects.filter(example_id=example_id, reviewer=reviewerid,
                                                           sentence_tag='准入条件')
    else:
        # 先确定标注用户，此时标注内容
        lasttext = models.PolicySentenceTag.objects.filter(reviewer=reviewerid, sentence_id=1).order_by('-savedate')
        text_exist = lasttext.exists()
        userstart = models.PolicyTagger.objects.get(id=reviewerid).start
        topid = models.PolicyTagger.objects.get(id=reviewerid).end
        if not text_exist:
            message = "您尚未开始标注!"
            return render(request, 'policy_complete.html', {'message': message, 'from': 'no_tag'})
        else:
            id_exist = []
            for text in lasttext:
                if text.permissions != None:
                    id_exist.append(text.example_id)
            id_exist = set(id_exist)

            id_all = set([i for i in policy_ids[policy_ids.index(userstart): policy_ids.index(topid) + 1]])
            id_no = id_all - id_exist

            id_no = list(id_no)
            # print('id_no:',id_no)
            if id_no != []:
                example_id = id_no[0]
                tag_info = models.PolicySentenceTag.objects.filter(example_id=example_id, reviewer=reviewerid,
                                                                   sentence_tag='准入条件')
            else:
                return render(request, 'policy_complete.html', {'message': '您已完成当前所有准入条件四元组标注！', 'from': 'permission'})

    if not tag_info.exists():
                    return render(request, 'policy_complete.html', {'message': '您已完成当前所有准入条件四元组标注！', 'from': 'permission'})
    search_dict = dict()
    if example_id:
        search_dict['example_id'] = example_id
    if reviewerid:
        search_dict['reviewer'] = reviewerid

    sentences = [tag.sentence for tag in tag_info]
    uids = [tag.unique_id for tag in tag_info]

    permission_sentences = zip(uids, sentences)

    return render(request, 'policy_permission.html', {'message': '以下为您选择的准入条件句子，请开始标注四元组', 'nowtext_id': example_id,
                                                      'permission_sentence': permission_sentences})