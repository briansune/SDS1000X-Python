import sds1000x_series as _sds
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from quantiphy import Quantity

matplotlib.use('TKAgg')


def main():
    sds_hdr = _sds.SDS1000X()
    sds_hdr.sds_ip = "192.168.1.240"

    sds_hdr.sds_connect()

    sds_hdr.sds_get_stage()

    # sds_hdr.sdsSetup('ASET')
    # print(sds_hdr.sdsQuery('INR?'))
    # print(sds_hdr.sdsQuery('WFSU?'))

    sds_hdr.sds_get_scop_cfg(1)
    a_txt = [
        'Sample Rate: {}'.format(Quantity(sds_hdr.smpl_rat, 'a/s')),
        'Voltage Offset: {}'.format(Quantity(sds_hdr.volt_ofs, 'V')),
        'Voltage Division: {}'.format(Quantity(sds_hdr.volt_div, 'V')),
        'Time Offset: {}'.format(Quantity(sds_hdr.time_ofs, 'S')),
        'Time Division: {}'.format(Quantity(sds_hdr.time_div, 'S'))]
    [print(t) for t in a_txt]

    # print(sds_hdr.sdsChannelCapture(1, 'WF?', 'DESC'))
    b_status = sds_hdr.sds_channel_capture(1)
    if b_status:
        print('PASS - Plot Scope Data')
        fig, ax = plt.subplots()
        ax.plot(sds_hdr.plot_x, sds_hdr.plot_y)
        ax.plot(sds_hdr.plot_x, [sds_hdr.volt_ofs] * len(sds_hdr.plot_y))

        ax.set_ylim(sds_hdr.volt_axis)
        ax.set_xlim(sds_hdr.time_axis)
        ax.set_yticklabels([])
        ax.set_xticklabels([])

        ax.yaxis.set_major_locator(MultipleLocator(sds_hdr.volt_div))
        ax.xaxis.set_major_locator(MultipleLocator(sds_hdr.time_div))
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        ax.spines['left'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('center')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        ax.grid()
        ax.grid(b=True, which='major', color='dimgray', linestyle='-', linewidth=0.3)
        ax.grid(b=True, which='minor', color='silver', linestyle='-', linewidth=0.1)
        ax.minorticks_on()
        ax.title.set_text(a_txt[2] + '\n' + a_txt[4])

        fig.tight_layout()
        plt.savefig('test.png', dpi=300)

    sds_hdr.sds_close()


if __name__ == '__main__':
    main()
