from django.urls import path
from web.views.guest import trangchu, danhmuc, baiviet, timkiem
from web.views.manage import admin, canhan, danhmuc_ad, baiviet_ad, nguoidung
from web.views import dangki, log

urlpatterns = [
    path('trangchu/', trangchu.index, name='trangchu'),
    path('', trangchu.index),
    # path('danhmuc/(?P<danh_muc_id>[0-9]+)/', danhmuc.index),
    path('danhmuc/<str:danhmuc_id>', danhmuc.index),
    path('baiviet/<str:baiviet_id>', baiviet.index),
    path('timkiem/', timkiem.index, name="timkiem"),

    path('dangki/', dangki.UsersView.dangki, name="dangki"),
    path('dangnhap/', log.UsersView.login, name="dangnhap"),
    path('dangxuat/', log.UsersView.logout, name="dangxuat"),
    path('Active/<str:active_id>', dangki.UsersView.active, name="Active"),
    path('quenpass/', dangki.UsersView.quenpass, name="quenpass"),
    path('taolaipass/', dangki.UsersView.taolaipass, name="taolaipass"),

    path('admin/', admin.index, name="admin"),
    path('danhmuc_ds/', danhmuc_ad.CategoriesView.list, name="danhmuc_ds"),
    path('danhmuc_them/', danhmuc_ad.CategoriesView.create, name="danhmuc_them"),
    path('danhmuc_sua/<int:dm_id>', danhmuc_ad.CategoriesView.update, name="danhmuc_sua"),
    path('danhmuc_xoa/<int:dm_id>', danhmuc_ad.CategoriesView.delete, name="danhmuc_xoa"),
    path('is_menu/<int:dm_id>', danhmuc_ad.CategoriesView.show_as_menu, name="is_menu"),
    path('danhmuc_ajaxsearch/', danhmuc_ad.CategoriesView.get_dlsearch, name="danhmuc_ajaxsearch"),

    path('baiviet_ds/', baiviet_ad.PostsView.list, name="baiviet_ds"),
    path('baiviet_them/', baiviet_ad.PostsView.create, name="baiviet_them"),
    path('baiviet_sua/<int:bv_id>', baiviet_ad.PostsView.update, name="baiviet_sua"),
    path('baiviet_xoa/<int:bv_id>', baiviet_ad.PostsView.delete, name="baiviet_xoa"),
    path('baiviet_ajaxsearch/', baiviet_ad.PostsView.get_dlsearch, name="baiviet_ajaxsearch"),
    path('baiviet_getchart/', baiviet_ad.PostsView.get_chartdate, name="baiviet_getchart"),
    path('baiviet_getchart_user/', baiviet_ad.PostsView.get_chartuser, name="baiviet_getchart_user"),
    path('baiviet_getchart_profile/', baiviet_ad.PostsView.get_chartprofile, name="baiviet_getchart_profile"),
    path('baiviet_getchart_danhmuc/', baiviet_ad.PostsView.get_chartdanhmuc, name="baiviet_getchart_danhmuc"),
    path('baiviet_export_csv/<str:search>', baiviet_ad.PostsView.export_csv, name="baiviet_export_csv"),
    path('baiviet_export_excel/<str:search>', baiviet_ad.PostsView.export_excel, name="baiviet_export_excel"),
    # path('baiviet_export_docx/', baiviet_ad.baiviet_view.export_docx, name="baiviet_export_excel"),

    path('nguoidung_ds/', nguoidung.UsersView.danhsach, name="nguoidung_ds"),
    path('nguoidung_xoa/<str:user_id>', nguoidung.UsersView.xoa, name="nguoidung_xoa"),
    path('nguoidung_trangthai/<str:user_id>', nguoidung.UsersView.trangthai, name="nguoidung_trangthai"),
    path('canhan/', canhan.UsersView.index, name="canhan"),
    path('nguoidung_ajaxsearch/', nguoidung.UsersView.get_dlsearch, name="nguoidung_ajaxsearch"),
]