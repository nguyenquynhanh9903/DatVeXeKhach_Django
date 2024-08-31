from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('NhanVien', views.NhanVienViewSet, 'NhanVien')
r.register('KhachHang', views.KhachHangViewSet, 'KhachHang')
r.register('KhachHangDi', views.KhachHangDiViewSet, 'KhachHangDi')
r.register('TaiXe', views.TaiXeViewSet, 'TaiXe')
r.register('TuyenXe', views.TuyenXeViewSet, 'TuyenXe')
r.register('ChuyenXe', views.ChuyenXeViewSet, 'ChuyenXe')
r.register('VeXe', views.VeXeViewSet, 'Vexe')
r.register('Ghe', views.GheViewSet, 'Ghe')
r.register('Xe', views.XeViewSet, 'Xe')
r.register('users', views.UserViewSet, 'users')
r.register('le', views.LeViewSet, 'Le')
r.register('chitietve', views.ChiTietVeXeViewSet, 'chitietve')
r.register('loainguoidung', views.LoaiNguoiDungViewSet, 'loainguoidung')

urlpatterns = [
    path('', include(r.urls)),
    path('payment/', views.payment_view, name='payment'),
    path('zalo/payment/', views.create_payment, name='zalopay'),
]
