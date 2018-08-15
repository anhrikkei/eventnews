from django.urls import path
from web.views.guest import trangchu, danhmuc, baiviet, timkiem
from web.views.manage import admin, canhan, danhmuc_ad, baiviet_ad, nguoidung
from web.views import dangki, log

urlpatterns = [
    path('trangchu/', trangchu.index, name='trangchu'),
    path('', trangchu.index),
    # path('danhmuc/(?P<danh_muc_id>[0-9]+)/', danhmuc.index),
    path('danhmuc/<int:danhmuc_id>', danhmuc.index),
    path('baiviet/<int:baiviet_id>', baiviet.index),
    path('timkiem/', timkiem.index, name="timkiem"),

    path('dangki/', dangki.nguoidung_view.dangki, name="dangki"),
    path('dangnhap/', log.nguoidung_view.dangnhap, name="dangnhap"),
    path('dangxuat/', log.nguoidung_view.dangxuat, name="dangxuat"),
    path('Active/<str:active_id>', dangki.nguoidung_view.active, name="Active"),
    path('quenpass/', dangki.nguoidung_view.quenpass, name="quenpass"),
    path('taolaipass/', dangki.nguoidung_view.taolaipass, name="taolaipass"),

    path('admin/', admin.index, name="admin"),
    path('danhmuc_ds/', danhmuc_ad.danhmuc_view.danhsach, name="danhmuc_ds"),
    path('danhmuc_them/', danhmuc_ad.danhmuc_view.them, name="danhmuc_them"),
    path('danhmuc_sua/<int:dm_id>', danhmuc_ad.danhmuc_view.sua, name="danhmuc_sua"),
    path('danhmuc_xoa/<int:dm_id>', danhmuc_ad.danhmuc_view.xoa, name="danhmuc_xoa"),
    path('is_menu/<int:dm_id>', danhmuc_ad.danhmuc_view.is_menu, name="is_menu"),
    path('danhmuc_ajaxsearch/', danhmuc_ad.danhmuc_view.get_dlsearch, name="danhmuc_ajaxsearch"),

    path('baiviet_ds/', baiviet_ad.baiviet_view.danhsach, name="baiviet_ds"),
    path('baiviet_them/', baiviet_ad.baiviet_view.them, name="baiviet_them"),
    path('baiviet_sua/<int:bv_id>', baiviet_ad.baiviet_view.sua, name="baiviet_sua"),
    path('baiviet_xoa/<int:bv_id>', baiviet_ad.baiviet_view.xoa, name="baiviet_xoa"),
    path('baiviet_ajaxsearch/', baiviet_ad.baiviet_view.get_dlsearch, name="baiviet_ajaxsearch"),
    path('baiviet_getchart/', baiviet_ad.baiviet_view.get_chartdate, name="baiviet_getchart"),
    path('baiviet_getchart_user/', baiviet_ad.baiviet_view.get_chartuser, name="baiviet_getchart_user"),
    path('baiviet_getchart_profile/', baiviet_ad.baiviet_view.get_chartprofile, name="baiviet_getchart_profile"),
    path('baiviet_getchart_danhmuc/', baiviet_ad.baiviet_view.get_chartdanhmuc, name="baiviet_getchart_danhmuc"),
    path('baiviet_export_csv/', baiviet_ad.baiviet_view.export_csv, name="baiviet_export_csv"),
    path('baiviet_export_excel/', baiviet_ad.baiviet_view.export_excel, name="baiviet_export_excel"),

    path('nguoidung_ds/', nguoidung.nguoidung_view.danhsach, name="nguoidung_ds"),
    path('nguoidung_xoa/<str:user_id>', nguoidung.nguoidung_view.xoa, name="nguoidung_xoa"),
    path('nguoidung_trangthai/<str:user_id>', nguoidung.nguoidung_view.trangthai, name="nguoidung_trangthai"),
    path('canhan/', canhan.nguoidung_view.index, name="canhan"),
    path('nguoidung_ajaxsearch/', nguoidung.nguoidung_view.get_dlsearch, name="nguoidung_ajaxsearch"),
]