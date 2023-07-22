import sds1000x_series as _sds


def main():
    sds_hdr = _sds.SDS1000X()
    sds_hdr.sds_ip = "192.168.1.240"

    sds_hdr.sdsConnect()

    sds_hdr.sdsGetStage()

    sds_hdr.sdsClose()


if __name__ == '__main__':
    main()
