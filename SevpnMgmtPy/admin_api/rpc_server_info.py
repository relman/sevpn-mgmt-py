# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.os_info import OsInfo


class RpcServerInfo:
    def __init__(self, server_product_name='', server_version_string='', server_build_info_string='', server_ver_int=0,
                 server_build_int=0, server_host_name='', server_type=0, server_build_date=0L, server_family_name='',
                 os_info=OsInfo()):
        self.server_product_name = server_product_name
        self.server_version_string = server_version_string
        self.server_build_info_string = server_build_info_string
        self.server_ver_int = server_ver_int
        self.server_build_int = server_build_int
        self.server_host_name = server_host_name
        self.server_type = server_type
        self.server_build_date = server_build_date
        self.server_family_name = server_family_name
        self.os_info = os_info

    def in_rpc_server_info(self, pack):
        if pack is None:
            return
        self.server_product_name = pack.get_value("ServerProductName")
        self.server_version_string = pack.get_value("ServerVersionString")
        self.server_build_info_string = pack.get_value("ServerBuildInfoString")
        self.server_ver_int = pack.get_value("ServerVerInt")
        self.server_build_int = pack.get_value("ServerBuildInt")
        self.server_host_name = pack.get_value("ServerHostName")
        self.server_type = pack.get_value("ServerType")
        self.server_build_date = pack.get_value("ServerBuildDate")
        self.server_family_name = pack.get_value("ServerFamilyName")
        self.os_info = self.in_rpc_os_info(pack)

    def in_rpc_os_info(self, pack):
        if pack is None:
            return
        os_info = OsInfo(os_type=pack.get_value("OsType"),
                         os_service_pack=pack.get_value("OsServicePack"),
                         os_system_name=pack.get_value("OsSystemName"),
                         os_product_name=pack.get_value("OsProductName"),
                         os_vendor_name=pack.get_value("OsVendorName"),
                         os_version=pack.get_value("OsVersion"),
                         kernel_name=pack.get_value("KernelName"),
                         kernel_version=pack.get_value("KernelVersion"))
        return os_info
