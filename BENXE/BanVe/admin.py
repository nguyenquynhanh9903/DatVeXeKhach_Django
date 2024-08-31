from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import path
from django.db.models import Count, Sum
from django.template.response import TemplateResponse
from datetime import datetime, timedelta
from django.db.models.functions import ExtractMonth, ExtractQuarter, ExtractYear


from .models import NhanVien, KhachHang, LoaiXe, Loai_ghe, TaiXe, Xe, Ghe, TuyenXe, ChuyenXe, \
    Ve_Xe, Chi_Tiet_Ve_Xe, Comment, Like, User, LoaiNguoiDung, Loai_NV, LoaiKhachHang


def thong_ke_doanh_thu_theo_thang(nam):
    doanh_thu_theo_thang = {}

    for thang in range(1, 13):  # Lặp qua các tháng từ 1 đến 12
        doanh_thu = Ve_Xe.object.filter(created_date__year=nam, created_date__month=thang).aggregate(
            total_doanh_thu=Sum('Gia'))
        doanh_thu_theo_thang[thang] = doanh_thu['total_doanh_thu'] if doanh_thu['total_doanh_thu'] else 0

    return doanh_thu_theo_thang


def thong_ke_doanh_thu_theo_quy(nam):
    return Ve_Xe.object.filter(created_date__year=nam).annotate(quarter=ExtractQuarter('created_date')).values(
        'quarter').annotate(total_doanh_thu=Sum('Gia'))


def thong_ke_doanh_thu_theo_nam():
    now = datetime.now()
    five_years_ago = now - timedelta(days=365 * 5)

    # Lấy tất cả các năm trong khoảng thời gian quan tâm
    years = list(range(five_years_ago.year + 1, now.year + 1))

    # Tạo một danh sách trống để lưu trữ dữ liệu doanh thu cho mỗi năm
    doanh_thu_theo_nam = []

    # Lặp qua từng năm và truy vấn dữ liệu doanh thu cho từng năm
    for year in years:
        doanh_thu = Ve_Xe.object.filter(created_date__year=year).aggregate(
            total_doanh_thu=Sum('Gia')
        )
        # Nếu không có dữ liệu doanh thu cho năm đó, đặt giá trị thành 0
        total_doanh_thu = doanh_thu['total_doanh_thu'] if doanh_thu['total_doanh_thu'] else 0
        doanh_thu_theo_nam.append({'year': year, 'total_doanh_thu': total_doanh_thu})

    return doanh_thu_theo_nam


class MyBusAdminSite(admin.AdminSite):
    site_header = 'MAIANHBUS_QUANLY'

    def get_urls(self):
        return [path('bus-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        nam = request.GET.get('nam')
        # Thống kê mật độ chuyến xe theo tuyến
        tuyen_stats = TuyenXe.object.annotate(counter=Count('chuyenxe__id')).values('id', 'Ten_tuyen', 'counter')
        doanh_thu_theo_thang = thong_ke_doanh_thu_theo_thang(nam)
        doanh_thu_theo_quy = thong_ke_doanh_thu_theo_quy(nam)
        doanh_thu_nam = thong_ke_doanh_thu_theo_nam()
        return TemplateResponse(request, 'admin/stats.html', {
            'tuyen_stats': tuyen_stats,
            'doanh_thu_theo_thang': doanh_thu_theo_thang,
            'doanh_thu_theo_quy': doanh_thu_theo_quy,
            'doanh_thu_nam': doanh_thu_nam,
        })


admin_site = MyBusAdminSite(name='MAIANHBUS')


# Admin quản lý(thêm/xoá/sửa/tìm kiếm) chuyến xe, tuyến xe, nhân viên, tài xế công ty
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ['id', 'Ten_NV', 'NgaySinh', 'DienThoai', 'DiaChi', 'Email', 'Loai_NV']
    search_fields = ['id', 'Ten_NV']
    list_filter = ['id', 'Ten_NV', 'Loai_NV']
    readonly_fields = ['my_image']

    def my_image(self, NhanVien):
        if NhanVien.image:
            return mark_safe(f"<img src='https://res.cloudinary.com/duz2xltvs/{NhanVien.image}' width='200' />")


class KhachHangAdmin(admin.ModelAdmin):
    list_display = ['id', 'Ten_KH', 'NgaySinh', 'DienThoai', 'DiaChi', 'Email', 'Loai_KH']
    search_fields = ['id', 'Ten_KH']
    list_filter = ['id', 'Ten_KH', 'Loai_KH']
    readonly_fields = ['my_image']

    def my_image(self, KhachHang):
        if KhachHang.image:
            return mark_safe(f"<img src='https://res.cloudinary.com/duz2xltvs/{KhachHang.image}' width='200' />")


class TaiXeAdmin(admin.ModelAdmin):
    list_display = ['id', 'Ten_taixe', 'NgaySinh', 'DienThoai', 'DiaChi', 'Email']
    search_fields = ['id', 'Ten_taixe']
    list_filter = ['id', 'Ten_taixe']
    readonly_fields = ['my_image']

    def my_image(self, TaiXe):
        if TaiXe.image:
            return mark_safe(f"<img src='https://res.cloudinary.com/duz2xltvs/{TaiXe.image}' width='200' />")


# Nhanvien ở đây là tên bảng
admin.site.register(NhanVien, NhanVienAdmin)
admin.site.register(KhachHang, KhachHangAdmin)
admin.site.register(TaiXe, TaiXeAdmin)
admin.site.register(TuyenXe)
admin.site.register(ChuyenXe)
admin.site.register(LoaiXe)
admin.site.register(Loai_ghe)
admin.site.register(Xe)
admin.site.register(Ghe)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Ve_Xe)
admin.site.register(Chi_Tiet_Ve_Xe)
admin.site.register(User)
admin.site.register(LoaiNguoiDung)
admin.site.register(LoaiKhachHang)
admin.site.register(Loai_NV)
