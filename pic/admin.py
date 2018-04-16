from django.contrib import admin
from .models import *
# Register your models here.
class CateAdmin(admin.ModelAdmin):
    list_display = ['licensetypeid','licensename']
    list_per_page = 20

class PicAdmin(admin.ModelAdmin):
    list_display = ['companyname', 'cate', 'pdflink', 'status', 'create_date']
    list_editable = ['status']
    list_filter = ['cate', 'status']
    # 搜索项如为外键词 本表外键字段__外键所在表需查询字段
    search_fields = ['companyname_id__companyname', 'cate_id__licensename']
    list_per_page = 20


admin.site.register(Cate, CateAdmin)
admin.site.register(Pic,PicAdmin)
admin.site.register(Company,)