import subprocess
import psutil
import time
from datetime import datetime
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import (NhanVien, KhachHang, TaiXe,
                     ChuyenXe, TuyenXe, Ve_Xe, Chi_Tiet_Ve_Xe, User, Like, Comment, Ghe, Xe, Khach_di, NgayLe, LoaiNguoiDung)
from . import serializers, paginators
from . import prems
import hashlib
from django.http import JsonResponse, HttpRequest
import json
import base64
import requests
import hmac
import random
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse



class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# Admin quản lý(thêm/xoá/sửa/tìm kiếm) chuyến xe, tuyến xe, nhân viên, tài xế công ty
class NhanVienViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = NhanVien.object.filter(active=True)
    serializer_class = serializers.NhanVienSerializer
    pagination_class = paginators.ChiaTrangPaginator
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        ma_nhanvien = self.request.query_params.get('ma_nhanvien')
        q = self.request.query_params.get('q')
        if ma_nhanvien:
            queryset = queryset.filter(id=ma_nhanvien)
        if q:
            queryset = queryset.filter(Ten_NV__icontains=q)

        return queryset

    @action(methods=['get'], url_path='NhanVien', detail=True, permission_classes=[IsAdminUserOrReadOnly])
    def get_NhanVien(self, request, pk):
        nhanvien = self.get_object().nhanvien_set.filter(active=True)
        return Response(serializers.NhanVienSerializer(nhanvien, many=True).data,
                        status=status.HTTP_200_OK)


    @action(methods=['post'], url_path='Them_NV', detail=False, permission_classes=[IsAdminUserOrReadOnly])
    def them_NV(self, request):
        if 'id' in request.data:
            del request.data['id']
        nhanvien = serializers.ThemNhanVienSerializer(data=request.data)
        if nhanvien.is_valid():
            nhanvien.save()
            return Response(nhanvien.data, status=status.HTTP_201_CREATED)
        return Response(nhanvien.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='Xoa_NV', detail=True, permission_classes=[IsAdminUserOrReadOnly])
    def Xoa_NV(self, request, pk):

        ma_nhanvien = NhanVien.object.get(id=pk)
        if ma_nhanvien:
            ma_nhanvien.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='Sua_NV', detail=True)
    def Sua_NV(self, request, pk=None):

        try:
            nhanvien = NhanVien.object.get(id=pk)
        except NhanVien.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách hàng'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.NhanVienSerializer(nhanvien, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KhachHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = KhachHang.object.filter(active=True)
    pagination_class = paginators.ChiaTrangPaginator
    serializer_class = serializers.KhachHangSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset

        makhach = self.request.query_params.get('makhach')
        q = self.request.query_params.get('q')
        if makhach:
            queryset = queryset.filter(id=makhach)

        if q:
            queryset = queryset.filter(Ten_KH__icontains=q)

        return queryset

    @action(methods=['post'], url_path='Them_KH', detail=False)
    def them_KH(self, request):

        khachhang= serializers.KhachHangSerializer(data=request.data)
        # kiểm tra khachhang có hợp lệ hay không
        if khachhang.is_valid():
            khachhang.save()
            return Response(khachhang.data, status=status.HTTP_201_CREATED)
        return Response(khachhang.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='Xoa_KH', detail=True)
    def Xoa_KH(self, request, pk):
        ma_khachhang = KhachHang.object.get(id=pk)
        if ma_khachhang:
            ma_khachhang.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='Sua_KH', detail=True)
    def Sua_KH(self, request, pk):
        try:
            khachhang = KhachHang.object.get(id=pk)
        except KhachHang.DoesNotExist:
            return Response({'message': 'Không tìm thấy khách hàng'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.KhachHangSerializer(khachhang, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaiXeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TaiXe.object.filter(active=True)
    pagination_class = paginators.ChiaTrangPaginator
    serializer_class = serializers.TaiXeSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset

        mataixe = self.request.query_params.get('mataixe')
        q = self.request.query_params.get('q')
        if mataixe:
            queryset = queryset.filter(id=mataixe)

        if q:
            queryset = queryset.filter(Ten_taixe__icontains=q)

        return queryset

    @action(methods=['post'], url_path='Them_TX', detail=False, permission_classes = [IsAdminUserOrReadOnly])
    def them_TX(self, request):
        taixe= serializers.TaiXeSerializer(data=request.data)

        if taixe.is_valid():
            taixe.save()
            return Response(taixe.data, status=status.HTTP_201_CREATED)
        return Response(taixe.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='Xoa_TX', detail=True, permission_classes = [IsAdminUserOrReadOnly])
    def Xoa_TX(self, request, pk):
        ma_taixe = TaiXe.object.get(id=pk)
        if ma_taixe:
            ma_taixe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='Sua_TX', detail=True, permission_classes = [IsAdminUserOrReadOnly])
    def Sua_TX(self, request, pk):
        try:
            taixe = TaiXe.object.get(id=pk)
        except TaiXe.DoesNotExist:
            return Response({'message': 'Không tìm thấy tài xế'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TaiXeSerializer(taixe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TuyenXeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TuyenXe.object.filter(active=True)
    serializer_class = serializers.TuyenXeSerializer
    pagination_class = paginators.ChiaTrangPaginator

    @action(methods=['get'], url_path='ChuyenXe', detail=True)
    def get_ChuyenXe(self, request, pk):
        chuyenxe = self.get_object().chuyenxe_set.filter(active=True)
        return Response(serializers.ChuyenXeSerializer(chuyenxe, many=True).data,
                        status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = self.queryset
        diemdi = self.request.query_params.get('diemdi')
        diemden = self.request.query_params.get('diemden')
        q = self.request.query_params.get('q')

        if diemdi:
            queryset = queryset.filter(Diendi__icontains=diemdi)

        if diemden:
            queryset = queryset.filter(Diemden__icontains=diemden)

        if q:
            queryset = queryset.filter(id=q)

        return queryset


    @action(methods=['post'], url_path='Them_TuyenXe', detail=False, permission_classes = [IsAdminUserOrReadOnly])
    def them_TuyenXe(self, request):
        tuyenxe = serializers.TuyenXeSerializer(data=request.data)

        if tuyenxe.is_valid():
            tuyenxe.save()
            return Response(tuyenxe.data, status=status.HTTP_201_CREATED)
        return Response(tuyenxe.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='Xoa_TuyenXe', detail=True, permission_classes = [IsAdminUserOrReadOnly])
    def Xoa_TuyenXe(self, request, pk):
        matuyenxe = TuyenXe.object.get(id=pk)
        if matuyenxe:
            matuyenxe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='Sua_TuyenXe', detail=True, permission_classes = [IsAdminUserOrReadOnly])
    def Sua_TuyenXe(self, request, pk):
        try:
            tuyenxe = TuyenXe.object.get(id=pk)
        except TuyenXe.DoesNotExist:
            return Response({'message': 'Không tìm thấy tuyến xe'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TuyenXeSerializer(tuyenxe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChuyenXeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ChuyenXe.object.filter(active=True)
    serializer_class = serializers.ChuyenXeSerializer
    pagination_class = paginators.ChiaTrangPaginator

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(id=q)

        matuyen = self.request.query_params.get('matuyen')
        if matuyen:
            queryset = queryset.filter(Ma_Tuyen_id=matuyen)

        giodi = self.request.query_params.get('giodi')
        if giodi:
            queryset = queryset.filter(Giodi=giodi)

        idtaixe = self.request.query_params.get('idtaixe')
        if idtaixe:
            queryset = queryset.filter(Ma_TaiXe_id=idtaixe)

        return queryset


    @action(methods=['post'], url_path='Them_ChuyenXe', detail=False, permission_classes = [IsAdminUserOrReadOnly])
    def them_ChuyenXe(self, request):
        chuyenxe = serializers.ChuyenXeSerializer(data=request.data)

        if chuyenxe.is_valid():
            chuyenxe.save()
            return Response(chuyenxe.data, status=status.HTTP_201_CREATED)
        return Response(chuyenxe.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], url_path='Xoa_ChuyenXe', detail=True, permission_classes = [IsAdminUserOrReadOnly])
    def Xoa_ChuyenXe(self, request, pk):
        machuyenxe = ChuyenXe.object.get(id=pk)
        if machuyenxe:
            machuyenxe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], url_path='Capnhat_ChuyenXe', detail=True, permission_classes = [IsAdminUserOrReadOnly])
    def Sua_ChuyenXe(self, request, pk):
        try:
            chuyenxe = ChuyenXe.object.get(id=pk)
        except ChuyenXe.DoesNotExist:
            return Response({'message': 'Không tìm thấy chuyến xe'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ChuyenXeSerializer(chuyenxe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').order_by('-id')
        paginator = paginators.ChiaTrangPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.CommentSerializer(comments, many=True).data)



    @action(methods=['post'], url_path='Them_comments', detail=True)
    def add_comment(self, request, pk):
        c = self.get_object().comment_set.create(content=request.data.get('content'),
                                                 user=request.user)
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)



    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        li, created = Like.object.get_or_create(chuyenxe=self.get_object(),
                                                 user=request.user)
        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.AuthenticatedChuyenXeSerializer(self.get_object()).data)


class VeXeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ve_Xe.object.filter(active=True)
    serializer_class = serializers.VeXeSerializer
    pagination_class = paginators.ChiaTrangPaginator

    def get_queryset(self):
        queryset = self.queryset

        mave = self.request.query_params.get('mave')
        if mave:
            queryset = queryset.filter(id=mave)
        return queryset


    @action(methods=['post'], url_path='Them_VeXe', detail=False)
    def them_VeXe(self, request):
        vexe = serializers.VeXeSerializer(data=request.data)
        if vexe.is_valid():
            vexe.save()
            return Response(vexe.data, status=status.HTTP_201_CREATED)
        return Response(vexe.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='Them_Chi_Tiet_Ve', detail=True)
    def add_chitietve(self, request, pk):
        ma_xe = request.data.get('Ma_Xe')
        ma_ghe = request.data.get('Vi_tri_ghe_ngoi')
        try:
            ghe_instance = Ghe.object.get(pk=ma_ghe)
            xe_instance = Xe.object.get(pk=ma_xe)
        except Xe.DoesNotExist:
            return Response({"error": "Không tìm thấy Xe tương ứng"}, status=status.HTTP_404_NOT_FOUND)

        c = self.get_object().chi_tiet_ve_xe_set.create(
            Ma_Xe=xe_instance,
            Vi_tri_ghe_ngoi=ghe_instance,
            Ghichu=request.data.get('Ghichu'),
            user=request.user
        )
        return Response(serializers.Chi_Tiet_Ve_XeSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], url_path='Xoa_VeXe', detail=True, permission_classes=[IsAdminUserOrReadOnly])
    def Xoa_VeXe(self, request, pk):
        ma_ve = Ve_Xe.object.get(id=pk)
        if ma_ve:
            ma_ve.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class ChiTietVeXeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Chi_Tiet_Ve_Xe.object.filter(active=True)
    serializer_class = serializers.Chi_Tiet_Ve_XeSerializer
    def get_queryset(self):
        queryset = self.queryset
        mauser = self.request.query_params.get('mauser')
        if mauser:
            queryset = queryset.filter(user_id=mauser)

        return  queryset

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='list_user', detail=False)
    def list_users(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'patch'], url_path='current_user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)


class GheViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ghe.object.filter(active=True)
    serializer_class = serializers.GheSerializer

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        gheID = self.request.query_params.get('gheID')
        if q:
            queryset = queryset.filter(Bienso_Xe=q)

        maghe = self.request.query_params.get('maghe')
        if maghe:
            queryset = queryset.filter(So_ghe=maghe)

        if gheID:
            queryset = queryset.filter(id=gheID)

        return queryset

    @action(methods=['patch'], url_path='CapNhat_TT' ,detail=True)
    def update_status(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except Ghe.DoesNotExist:
            return Response({"message": "Ghe not found"}, status=status.HTTP_404_NOT_FOUND)

        trangthai_value = request.data.get('trangthai')

        if trangthai_value is not None:
            instance.trangthai = trangthai_value
            instance.save()
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Update không thành công !"}, status=status.HTTP_400_BAD_REQUEST)


class XeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Xe.object.filter(active=True)
    serializer_class = serializers.XeSerializer

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(id=q)

        return queryset


class KhachHangDiViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Khach_di.object.filter(active=True)
    pagination_class = paginators.ChiaTrangPaginator
    serializer_class = serializers.KhachDiSerializer

    def get_queryset(self):
        queryset = self.queryset

        makhach = self.request.query_params.get('makhach')
        q = self.request.query_params.get('q')
        if makhach:
            queryset = queryset.filter(id=makhach)

        if q:
            queryset = queryset.filter(Ten_KH__icontains=q)

        return queryset

    @action(methods=['post'], url_path='Them_KH_Di', detail=False)
    def them_KH(self, request):
        khachhang= serializers.KhachDiSerializer(data=request.data)
        if khachhang.is_valid():
            khachhang.save()
            return Response(khachhang.data, status=status.HTTP_201_CREATED)
        return Response(khachhang.errors, status=status.HTTP_400_BAD_REQUEST)

class LeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = NgayLe.object.filter(active=True)
    serializer_class = serializers.LeSerializer

    def get_queryset(self):
        queryset = self.queryset
        ngay = self.request.query_params.get('ngay')
        if ngay:
            queryset = queryset.filter(Le__icontains=ngay)
        return queryset


class LoaiNguoiDungViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset =  LoaiNguoiDung.object.filter(active=True)
    serializer_class = serializers.LoaiNguoiDungSerializer

    def get_queryset(self):
        queryset = self.queryset
        ma = self.request.query_params.get('ma')
        if ma:
            queryset = queryset.filter(id=ma)
        return  queryset


# API Thanh Toán MOMO
@csrf_exempt
def payment_view(request: HttpRequest):
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    requestId = f"{partnerCode}{int(time.time() * 1000)}"
    orderId = 'MM' + str(int(time.time() * 1000))
    orderInfo = "pay with MoMo"
    redirectUrl = "https://momo.vn/return"
    ipnUrl = "https://callback.url/notify"
    amount = request.headers.get('amount', '')
    requestType = "payWithATM"
    extraData = ""

    # Construct raw signature
    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"

    # Generate signature using HMAC-SHA256
    signature = hmac.new(secretKey.encode(), rawSignature.encode(), hashlib.sha256).hexdigest()

    # Create request body as JSON
    data = {
        "partnerCode": partnerCode,
        "accessKey": accessKey,
        "requestId": requestId,
        "amount": amount,
        "orderId": orderId,
        "orderInfo": orderInfo,
        "redirectUrl": redirectUrl,
        "ipnUrl": ipnUrl,
        "extraData": extraData,
        "requestType": requestType,
        "signature": signature,
        "lang": "vi"
    }

    # Send request to MoMo endpoint
    url = 'https://test-payment.momo.vn/v2/gateway/api/create'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)

    # Process response
    if response.status_code == 200:
        response_data = response.json()
        pay_url = response_data.get('payUrl')
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": f"Failed to create payment request. Status code: {response.status_code}"},
                            status=500)



# TẠO API THANH TOÁN BẰNG ZALO PAY
config = {
      "app_id": 2553,
      "key1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
      "key2": "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz",
      "endpoint": "https://sb-openapi.zalopay.vn/v2/create"
}

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        # Lấy thông tin từ yêu cầu của người dùng
        amount = request.headers.get('amount', '')  # Lấy amount từ header
        transID = random.randrange(1000000)
        # Xây dựng yêu cầu thanh toán
        order = {
            "app_id": config["app_id"],
            "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID),  # mã giao dich có định dạng yyMMdd_xxxx
            "app_user": "user123",
            "app_time": int(round(time.time() * 1000)),  # miliseconds
            "embed_data": json.dumps({}),
            "item": json.dumps([{}]),
            "amount": amount,
            "description": "Thanh Toán Vé Xe #" + str(transID),
            "bank_code": "",
        }

        # Tạo chuỗi dữ liệu và mã hóa HMAC
        data = "{}|{}|{}|{}|{}|{}|{}".format(order["app_id"], order["app_trans_id"], order["app_user"],
                                             order["amount"], order["app_time"], order["embed_data"], order["item"])
        order["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

        # Gửi yêu cầu đến ZaloPay API
        try:
            response = urllib.request.urlopen(url=config["endpoint"], data=urllib.parse.urlencode(order).encode())
            result = json.loads(response.read())
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Only POST requests are allowed"})



# @csrf_exempt
# def payment_view(request: HttpRequest):
#     accessKey = 'F8BBA842ECF85'
#     secretKey = 'K951B6PE1waDMi640xX08PD3vg6EkVlz'
#     orderInfo = 'pay with MoMo'
#     partnerCode = 'MOMO'
#     redirectUrl = 'https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b'
#     ipnUrl = 'https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b'
#     requestType = "payWithMethod"
#     amount = request.headers.get('amount', '')  # Lấy amount từ header
#     orderId = partnerCode + str(int(time.time() * 1000))
#     requestId = orderId
#     extraData = ''
#     orderGroupId = ''
#     autoCapture = True
#     autoCapture = True
#     lang = 'vi'
#
#     # Tạo chuỗi signature
#     rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
#     signature = hmac.new(secretKey.encode(), rawSignature.encode(), hashlib.sha256).hexdigest()
#
#     # Tạo request body
#     data = {
#         "partnerCode": partnerCode,
#         "partnerName": "Test",
#         "storeId": "MomoTestStore",
#         "requestId": requestId,
#         "amount": amount,
#         "orderId": orderId,
#         "orderInfo": orderInfo,
#         "redirectUrl": redirectUrl,
#         "ipnUrl": ipnUrl,
#         "lang": lang,
#         "requestType": requestType,
#         "autoCapture": autoCapture,
#         "extraData": extraData,
#         "orderGroupId": orderGroupId,
#         "signature": signature
#     }
#
#     # Gửi request đến MoMo
#     response = requests.post('https://test-payment.momo.vn/v2/gateway/api/create', json=data)
#     response_data = response.json()
#     pay_url = response_data.get('payUrl')
#
#     return JsonResponse(response_data)
