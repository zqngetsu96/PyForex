import matplotlib.animation as animation
import mplfinance as mpf


def show_realtime(rates):
    fig = mpf.figure(style='charles',figsize=(7,8))
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(3,1,3)
    rn = 72
    def animate(ival):
        if (rn+ival) > len(rates):
            print('no more data to plot')
            ani.event_source.interval *= 3
            if ani.event_source.interval > 12000:
                exit()
            return
        data = rates.iloc[ival:(rn+ival)]
        ax1.clear()
        ax2.clear()
        mpf.plot(data,ax=ax1,volume=ax2,type='candle')
        mpf.show()

    ani = animation.FuncAnimation(fig, animate, interval=100)
    mpf.show()

    