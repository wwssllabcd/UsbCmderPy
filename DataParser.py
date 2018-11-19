from ExtendCmd import *
from EricCorePy.Utility.EricUtility import *


class DataParser:
    def parser(self, cmd, data):
        res = ""
        if cmd.cdb[0] == VDR_SCSI_BASE:
            if cmd.cdb[4] == VDR_READ_PUA_STRONG:
                res = self.parser_pua_read(cmd, data)

        return res

    def parser_pua_read(self, cmd, data):
        util = EricUtility()
        res = ""
        base = 32*1024
        ecc = data[base:base+128]
        cnt = 0
        res += "ECC STATUS \r\n"
        for d in ecc:
            res += util.make_table_crlf(cnt)
            res += format(d, '02X') + " "
            cnt += 1
        res += "\r\n\r\n"
        base = 32*1024 + 512
        tag = data[base:base+128]

        cnt = 0
        res += "TAG STATUS\r\n"
        for d in tag:
            res += util.make_table_crlf(cnt)
            res += format(d, '02X') + " "
            cnt += 1
        res += "\r\n\r\n"

        return res
