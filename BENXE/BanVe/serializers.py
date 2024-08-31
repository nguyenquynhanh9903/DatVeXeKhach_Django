from rest_framework import serializers
from .models import (NhanVien, KhachHang, TaiXe,
                     TuyenXe, ChuyenXe, Ve_Xe, Chi_Tiet_Ve_Xe, User, Comment, Ghe, Xe, Khach_di, NgayLe, LoaiNguoiDung)


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avatar'] = instance.avatar.url
        return req

class KhachHangSerializer(ItemSerializer):
    class Meta:
        model = KhachHang
        fields = ['id', 'Ten_KH', 'NgaySinh', 'GioiTinh', 'DiaChi', 'CMND', 'DienThoai', 'Email', 'avatar', 'Loai_KH']

class TaiXeSerializer(ItemSerializer):
    class Meta:
        model = TaiXe
        fields = ['id', 'Ten_taixe', 'DiaChi', 'GioiTinh', 'NgaySinh', 'CMND', 'DienThoai', 'Email', 'avatar']

class TuyenXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuyenXe
        fields = '__all__'


class GheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ghe
        fields = '__all__'

class XeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xe
        fields = '__all__'

class ChuyenXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChuyenXe
        fields = ['id', 'TenChuyenXe', 'Ngay', 'Ma_Tuyen', 'Giodi', 'Gioden', 'Cho_trong',
                  'Noidi', 'Noiden', 'Ma_TaiXe', 'Ma_Xe']



class UserSerializer(ItemSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'avatar', 'Loai_NguoiDung']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

class NhanVienSerializer(ItemSerializer):
    class Meta:
        model = NhanVien
        fields = ['id', 'Ten_NV', 'NgaySinh', 'GioiTinh', 'DiaChi', 'CMND',
                  'DienThoai', 'Email', 'avatar']

class ThemNhanVienSerializer(ItemSerializer):
    class Meta:
        model = NhanVien
        fields = ['Ten_NV', 'NgaySinh', 'GioiTinh', 'DiaChi', 'CMND',
                  'DienThoai', 'Email', 'avatar']
        extra_kwargs = {
            'id': {'required': False}
        }

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'user']


class AuthenticatedChuyenXeSerializer(ChuyenXeSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, chuyenxe):
        return chuyenxe.like_set.filter(active=True).exists()

    class Meta:
        model = ChuyenXeSerializer.Meta.model
        fields = ChuyenXeSerializer.Meta.fields + ['liked']


class VeXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ve_Xe
        fields = '__all__'


class Chi_Tiet_Ve_XeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Chi_Tiet_Ve_Xe
        fields = '__all__'


class LeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NgayLe
        fields = '__all__'

class KhachDiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khach_di
        fields = '__all__'


class LoaiNguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiNguoiDung
        fields ='__all__'