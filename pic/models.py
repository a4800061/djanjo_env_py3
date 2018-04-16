from django.db import models
from system.storage import ImageStorage
# Create your models here.
class Cate(models.Model):
    licensename = models.CharField(verbose_name="证件类型",max_length=120)
    licensetypeid = models.IntegerField(verbose_name='证件类型ID')

    def __str__(self):
        return self.licensename

    class Meta:
        verbose_name = '证件类型'
        verbose_name_plural = verbose_name

class Company(models.Model):
    companyname = models.CharField(verbose_name='公司名称',max_length=200)
    companyid = models.IntegerField(verbose_name='公司ERPID')
    companytype = models.CharField(verbose_name='公司类型',choices=(('供应商','供应商'),('客户','客户'),('其它','其它')),max_length=10,default="供应商")
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    create_date = models.DateField(verbose_name='创建日期',auto_now_add=True)
    status = models.CharField(verbose_name='状态',choices=(('正式','正式'),('作废','作废')),max_length=10,default="正式")

    def __str__(self):
        return self.companyname

    class Meta:
        verbose_name = '公司信息'
        verbose_name_plural = verbose_name

def get_zip_path(instance, filename):
    return 'zip/{0}/{1}'.format(str(instance.id),filename)

def get_pdf_path(instance, filename):
    return 'pdf/{0}/{1}'.format(str(instance.id),filename)

class Pic(models.Model):
    companyname = models.ForeignKey(Company,verbose_name='公司名称')
    ziplink = models.FileField(verbose_name='zip文档链接',upload_to='photos/%Y/%m/%d',storage=ImageStorage())
    pdflink = models.FileField(verbose_name='pdf文档链接',blank=True, null=True, upload_to='photos/%Y/%m/%d')
    cate = models.ForeignKey(Cate,verbose_name='证件类型')
    downloads = models.IntegerField(verbose_name='下载次数',default=0)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    create_date = models.DateField(verbose_name='创建日期',auto_now_add=True)
    status = models.CharField(verbose_name='状态',choices=(('正式','正式'),('作废','作废')),max_length=10,default="正式")

    def __str__(self):
        return "%s"%self.id

    class Meta:
        verbose_name = '电子档案'
        verbose_name_plural = verbose_name

