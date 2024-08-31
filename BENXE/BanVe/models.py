from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from datetime import datetime
from django.utils import timezone


class BaseModel(models.Model):
    object = models.Manager()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class LoaiNguoiDung(BaseModel):
    loai = models.CharField(max_length=255)


class User(AbstractUser):
    Loai_NguoiDung = models.CharField(max_length=255, default=1)
    avatar = CloudinaryField(null=True)


class Loai_NV(BaseModel):
    # thêm loại online vào
    Ten_loai = models.CharField(max_length=255)

    def __str__(self):
        return self.Ten_loai


class NhanVien(BaseModel):
    Ten_NV = models.CharField(max_length=255)
    NgaySinh = models.CharField(max_length=255)
    GioiTinh = models.CharField(max_length=25)
    DiaChi = models.CharField(max_length=255)
    CMND = models.CharField(max_length=255)
    DienThoai = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Loai_NV = models.ForeignKey(Loai_NV, on_delete=models.PROTECT, default=1)
    avatar = CloudinaryField(null=True)

    def __str__(self):
        return self.Ten_NV


class LoaiKhachHang(BaseModel):
    Ten_Loai = models.CharField(max_length=255)

    def __str__(self):
        return self.Ten_Loai


class KhachHang(BaseModel):
    Ten_KH = models.CharField(max_length=255)
    Loai_KH = models.ForeignKey(LoaiKhachHang, on_delete=models.PROTECT)
    NgaySinh = models.CharField(max_length=255)
    GioiTinh = models.CharField(max_length=25)
    DiaChi = models.CharField(max_length=255)
    CMND = models.CharField(max_length=255)
    DienThoai = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    avatar = CloudinaryField(null=True)

    def __str__(self):
        return self.Ten_KH


class TaiXe(BaseModel):
    Ten_taixe = models.CharField(max_length=255)
    DiaChi = models.CharField(max_length=255)
    GioiTinh = models.CharField(max_length=25)
    NgaySinh = models.CharField(max_length=255)
    CMND = models.CharField(max_length=255)
    DienThoai = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    avatar = CloudinaryField(null=True)

    def __str__(self):
        return str(self.Ten_taixe)


class TuyenXe(BaseModel):
    Ten_tuyen = models.CharField(max_length=255)
    Diendi = models.CharField(max_length=255)
    Diemden = models.CharField(max_length=255)
    BangGia = models.CharField(max_length=255)

    def __str__(self):
        return str(self.Ten_tuyen)


class LoaiXe(BaseModel):
    Ten_loai = models.CharField(max_length=255)

    def __str__(self):
        return self.Ten_loai


class Xe(BaseModel):
    Ten_xe = models.CharField(max_length=255)
    Bien_so = models.CharField(max_length=255, default="1")
    So_ghe = models.CharField(max_length=255)
    Loaixe = models.ForeignKey(LoaiXe, on_delete=models.PROTECT)

    def __str__(self):
        return self.Bien_so


class ChuyenXe(BaseModel):
    TenChuyenXe = models.CharField(max_length=255)
    Ma_Tuyen = models.ForeignKey(TuyenXe, on_delete=models.PROTECT)
    Ngay = models.DateField(default=timezone.now)
    Giodi = models.CharField(max_length=255)
    Gioden = models.CharField(max_length=255)
    Noidi = models.CharField(max_length=255, default="Bến Xe")
    Noiden = models.CharField(max_length=255, default="Bến Xe")
    Cho_trong = models.CharField(max_length=255)
    Ma_TaiXe = models.ForeignKey(TaiXe, on_delete=models.PROTECT)
    Ma_Xe = models.ForeignKey(Xe, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.TenChuyenXe


class Loai_ghe(BaseModel):
    Ten_loai = models.CharField(max_length=255)

    def __str__(self):
        return self.Ten_loai


class Ghe(BaseModel):
    So_ghe = models.CharField(max_length=255)
    trangthai = models.CharField(max_length=255, default="Còn trống")
    Loai_ghe = models.ForeignKey(Loai_ghe, on_delete=models.PROTECT)
    Bienso_Xe = models.ForeignKey(Xe, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.So_ghe


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chuyenxe = models.ForeignKey(ChuyenXe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} - {self.chuyenxe_id}'

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255)


class Like(Interaction):
    class Meta:
        unique_together = ('user', 'chuyenxe')


class Khach_di (BaseModel):
    Ten_KH = models.CharField(max_length=255)
    DiaChi = models.CharField(max_length=255)
    CMND = models.CharField(max_length=255)
    DienThoai = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)

    def __str__(self):
        return self.Ten_KH


class Ve_Xe(BaseModel):
    Ma_NhanVien = models.ForeignKey(NhanVien, on_delete=models.PROTECT, null=True)
    Ma_KhachHang = models.ForeignKey(Khach_di, on_delete=models.PROTECT)
    Ma_ChuyenXe = models.ForeignKey(ChuyenXe, on_delete=models.PROTECT)
    Gia = models.CharField(max_length=255, default="0");
    trangthai_TT = models.CharField(max_length=255, default="trực tiếp")

    def __str__(self):
        return str(self.id)

class VeXeInteraction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vexe = models.ForeignKey(Ve_Xe, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user_id} - {self.vexe_id}'

    class Meta:
        abstract = True

class Chi_Tiet_Ve_Xe(VeXeInteraction):
    Ma_Xe = models.ForeignKey(Xe, on_delete=models.CASCADE, null=True)
    Vi_tri_ghe_ngoi = models.ForeignKey(Ghe, on_delete=models.CASCADE, null=True)
    Ghichu = models.CharField(max_length=255)


class NgayLe(BaseModel):
    Le = models.CharField(max_length=255);
    Tang = models.CharField(max_length=255);
