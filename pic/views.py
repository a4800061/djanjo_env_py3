from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.http import FileResponse
from django.core import serializers # Django model,QuerySet 序列化成json的方法
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .models import *
# Create your views here.

def index(request):
    data_count = Pic.objects.all().order_by('-create_time')[:10]
    return render(request,'index.html',locals())

# 视频详情页
def picDetail(request,vid):
    return HttpResponse("这是{0}图片详情页".format(vid))

# 下载测试
def download_test(request,vid):
    pic = Pic.objects.get(id=vid)
    # 读取mongodb的文件到临时文件中
    # fileid_ = request.GET["fileid"]
    fileid_ = pic.ziplink
    return HttpResponse("地址是{0}".format(fileid_))

# 分页代码
def getPage(request, video_list):
    paginator = Paginator(video_list, 12)
    try:
        page = int(request.GET.get('page', 1))
        video_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        video_list = paginator.page(1)
    return video_list

# 登录页面
def logIn(request):
    # 判断是否已经登录
    if request.user.is_authenticated():
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        if request.method == 'GET':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            return render(request, 'login.html', locals())
        elif request.method == 'POST':
            username = request.POST.get("username", '')
            password = request.POST.get("password", '')
            if username != '' and password != '':
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    print("登录成功！")
                    return redirect(request.session['login_from'])
                else:
                    print(username, password, user)
                    errormsg = '用户名或密码错误！'
                    return render(request, 'login.html', locals())
            else:
                return JsonResponse({"e": "chucuo"})

# 注销
def logOut(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])

def file_down(request,vid):
    pic = Pic.objects.get(id=vid)
    fileid_ = pic.ziplink
    file=open(fileid_,'rb')
    filename_ = file.filename
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{}"'.format(filename_)
    return response

def data_fresh(request,vid):
    # if request.method == 'POST':
    m = Pic.objects.all().order_by("-create_time")[0]
    print(type(m))
    print (m.companyname)
    context = {"data1": "%s" %m.companyname}
    return JsonResponse(context)
    # else:
    #     return HttpResponse("<h1>test</h1>")

def get_comment(request, article_id):
    article_list = get_object_or_404(Article, id=article_id)
    comments = article_list.comment_set.all()
    html = ''
    for i in comments:
        ele = '<div class="row"><article class="col-xs-12"><p class="pull-right"><span class="label label-default">作者:' + 'i.user' + '</span></p><p>' + i.content + '<ul class="list-inline"><li><a href="#"></a></li></ul></article></div><hr>'
        html += ele
    return HttpResponse(json.dumps({'piclist': html}))