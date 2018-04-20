from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.http import FileResponse
from django.core import serializers  # Django model,QuerySet 序列化成json的方法
from django.shortcuts import render_to_response
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
import os
from .models import *

# Create your views here.


def index(request):
    data_count = Pic.objects.all().order_by('-create_time')[:10]
    return render(request, 'index.html', locals())

# 视频详情页


def picDetail(request, vid):
    return HttpResponse("这是{0}图片详情页".format(vid))

@login_required()
def testurl(request):
    # 得到选中的证件类型ID, 如果不存在则默认值为1
    post_cateid = request.POST.get('cateidselect', -1)
    post_companyid = request.POST.get('companyid', -1)
    upload_file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
    file_obj = request.FILES.get('file')
    if post_companyid != -1 and post_cateid != -1 and upload_file != None:
        print (file_obj._get_name(), type(file_obj))
        # 处理文件名
        # name为上传文件名称
        import os, time, random
        # 文件扩展名
        ext = os.path.splitext(file_obj._get_name())[1]
        # 文件名部份
        d = os.path.splitext(file_obj._get_name())[0]
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        # 重写合成文件名(公司ID+证件ID+上传时间重命名）
        # name = os.path.join(d, fn + ext)
        name = post_companyid+'-'+post_cateid+'-'+fn + ext
        from django.core.files.uploadedfile import TemporaryUploadedFile
        if file_obj:  # 处理附件上传到方法
            with open(os.path.join("media", name),"wb") as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
        sets = Pic.objects.create(
            companyname_id=post_companyid,
            cate_id=post_cateid,
            ziplink=os.path.join("media", name)
        )
        result = {'res': '提交成功'}
        return render_to_response('upload_result.html', result)
    else:
        result = {'res': '提交的数据不符合要求'}
        return render_to_response('upload_result.html', result)


# 搜索


def search(request):
    data_count = Pic.objects.all().order_by('-create_time')[:10]
    return render(request, 'search.html', locals())


def get_search_data(request):
    if request.method == 'POST':
        ret = {'status': False, 'message': '', 'data': None}
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            print(post_data_dict['name'])
            query = Pic.objects.filter(
                companyname_id__companyname=post_data_dict['name'][0]).order_by('-create_time')
            # 包装数据
            content = {
                'cinemas': query
            }
            # 使用 render_to_response 函数处理模板数据并发送到前端
            return render_to_response('displist.html', content)
        except Exception as e:
            ret['message'] = str(e)
    else:
        return HttpResponse("<h1>提交数据错误</h1>")


# 上传文件
def upload_main(request):
    query = Cate.objects.all()
    content = {
        'cates': query
    }
    return render(request, 'upload.html', content)


def upload_search_companyname(request):
    if request.method == 'POST':
        ret = {'status': False, 'message': '', 'data': None}
        try:
            post_data = request.POST.get('post_data', None)
            post_data_dict = json.loads(post_data)
            print (post_data_dict['name'])
            query = Company.objects.filter(
                companyname=post_data_dict['name'])
            # 包装数据
            content = {
                'cinemas': query
            }
            # 使用 render_to_response 函数处理模板数据并发送到前端
            return render_to_response('upload_disp_company.html', content)
        except Exception as e:
            ret['message'] = str(e)
    else:
        return HttpResponse("<h1>提交数据错误</h1>")
# 下载测试


def download_test(request, vid):
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
            request.session['login_from'] = request.META.get(
                'HTTP_REFERER', '/')
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


def file_down(request, vid):
    pic = Pic.objects.get(id=vid)
    fileid_ = pic.ziplink
    file = open(fileid_, 'rb')
    filename_ = file.filename
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(
        filename_)
    return response


def data_fresh(request, vid):
    # if request.method == 'POST':
    m = Pic.objects.all().order_by("-create_time")[0]
    print(type(m))
    print (m.companyname)
    context = {"data1": "%s" % m.companyname}
    return JsonResponse(context)
    # else:
    #     return HttpResponse("<h1>test</h1>")


def get_comment(request, article_id):
    article_list = get_object_or_404(Article, id=article_id)
    comments = article_list.comment_set.all()
    html = ''
    for i in comments:
        ele = '<div class="row"><article class="col-xs-12"><p class="pull-right"><span class="label label-default">作者:' + \
            'i.user' + '</span></p><p>' + i.content + '<ul class="list-inline"><li><a href="#"></a></li></ul></article></div><hr>'
        html += ele
    return HttpResponse(json.dumps({'piclist': html}))
