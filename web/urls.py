from django.urls import path
from web.views.guest import trangchu, danhmuc, baiviet, timkiem
from web.views.manage import admin, canhan, danhmuc_ad, baiviet_ad, ajax, nguoidung
from web.views import dangki, dangnhap, dangxuat, active

urlpatterns = [
    path('trangchu/', trangchu.index, name='trangchu'),
    path('', trangchu.index),
    # path('danhmuc/(?P<danh_muc_id>[0-9]+)/', danhmuc.index),
    path('danhmuc/<int:danhmuc_id>', danhmuc.index),
    path('baiviet/<int:baiviet_id>', baiviet.index),
    path('timkiem/>', timkiem.index, name="timkiem"),

    path('dangki/', dangki.index, name="dangki"),
    path('dangnhap/', dangnhap.index, name="dangnhap"),
    path('dangxuat/', dangxuat.index, name="dangxuat"),
    path('Active/<str:active_id>', active.index, name="Active"),

    path('admin/', admin.index, name="admin"),
    path('danhmuc_ds/', danhmuc_ad.danhmuc_view.danhsach, name="danhmuc_ds"),
    path('danhmuc_them/', danhmuc_ad.danhmuc_view.them, name="danhmuc_them"),
    path('danhmuc_sua/<int:dm_id>', danhmuc_ad.danhmuc_view.sua, name="danhmuc_sua"),
    path('danhmuc_xoa/<int:dm_id>', danhmuc_ad.danhmuc_view.xoa, name="danhmuc_xoa"),
    path('is_menu/<int:dm_id>', danhmuc_ad.danhmuc_view.is_menu, name="is_menu"),

    path('baiviet_ds/', baiviet_ad.baiviet_view.danhsach, name="baiviet_ds"),
    path('baiviet_them/', baiviet_ad.baiviet_view.them, name="baiviet_them"),
    path('baiviet_sua/<int:bv_id>', baiviet_ad.baiviet_view.sua, name="baiviet_sua"),
    path('baiviet_xoa/<int:bv_id>', baiviet_ad.baiviet_view.xoa, name="baiviet_xoa"),
    path('get_dlsearch/', ajax.baiviet_view.get_dlsearch, name="get_dlsearch"),

    path('nguoidung_ds/', nguoidung.nguoidung_view.danhsach, name="nguoidung_ds"),
    path('nguoidung_xoa/<str:user_id>', nguoidung.nguoidung_view.xoa, name="nguoidung_xoa"),
    path('nguoidung_trangthai/<str:user_id>', nguoidung.nguoidung_view.trangthai, name="nguoidung_trangthai"),
    path('canhan/', canhan.nguoidung_view.index, name="canhan"),
]