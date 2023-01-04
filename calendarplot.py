import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

WEEKS_IN_MONTH = 6
DAYS_IN_WEEK = 7
DAY_LABELS = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
MONTH_LABELS = ['January',   'February', 'March',    'April',
                'May',       'June',     'July',     'August',
                'September', 'October',  'November', 'December']

def split_months(df, year):
    # Empty matrices
    a = np.empty((6, 7))
    a[:] = np.nan

    day_nums = {m:np.copy(a) for m in range(1,13)}  # matrix for day numbers
    day_vals = {m:np.copy(a) for m in range(1,13)}  # matrix for day values

    # Logic to shape datetimes to matrices in calendar layout
    date = pd.Timestamp(year=year, month=1, day=1)
    oneday = pd.Timedelta(1, unit='D')
    while date.year == year:
        
        try:
            value = df[date]
        except KeyError:
            value = 0
        
        day = date.day
        month = date.month
        col = (date.dayofweek + 1) % 7

        if date.is_month_start:
            row = 0

        day_nums[month][row, col] = day  # day number (0-31)
        day_vals[month][row, col] = value # day value (the heatmap data)

        if col == 6:
            row += 1
        
        date = date + oneday

    return day_nums, day_vals


def create_year_calendar(df, year, title=None, filename=None, cmap='cool', hlmap={}, showcb=False, portrait=False):
    if title is None:
        title = str(year)
    if filename is None:
        filename = title.replace(' ', '_') + '.png'

    vmin = df.min()
    vmin = vmin if vmin < 0 else 0
    vmax = df.max() 
    day_nums, day_vals = split_months(df, year)
    
    if portrait:
        fig, ax = plt.subplots(4, 3, figsize=(8.5, 11))
    else:
        fig, ax = plt.subplots(3, 4, figsize=(11, 8.5))

    gridcolor = 'white'
    fontcolor = 'black'

    for i, axs in enumerate(ax.flat):

        axs.imshow(day_vals[i+1], cmap=cmap, vmin=vmin, vmax=vmax)  # heatmap
        axs.set_title(MONTH_LABELS[i])

        # Labels
        axs.set_xticks(np.arange(DAYS_IN_WEEK))
        axs.set_xticklabels(DAY_LABELS, fontsize=10, color=fontcolor)
        axs.set_yticklabels([])

        # Tick marks
        axs.tick_params(axis=u'both', which=u'both', length=0)  # remove tick marks
        axs.xaxis.tick_top()

        # Modify tick locations for proper grid placement
        axs.set_xticks(np.arange(-.5, 6, 1), minor=True)
        axs.set_yticks(np.arange(-.5, 5, 1), minor=True)
        axs.grid(which='minor', color=gridcolor, linestyle='-', linewidth=2.1)

        # Despine
        for edge in ['left', 'right', 'bottom', 'top']:
            axs.spines[edge].set_color(gridcolor)

        label_map = {}
        # Annotate
        for w in range(WEEKS_IN_MONTH):
            for d in range(DAYS_IN_WEEK):
                day_val = day_vals[i+1][w, d]
                day_num = day_nums[i+1][w, d]

                # If day number is a valid calendar day, add an annotation
                if not np.isnan(day_num):
                    axs.text(d-0.43, w-0.40, f"{int(day_num)}",
                             ha='left', va='top',
                             fontsize=8, color=fontcolor)
                    # draw a highlight
                    if day_val in hlmap:
                        vcolor,vlabel = hlmap[day_val]
                        patch_coords = ((d - 0.5, w - 0.5),
                                    (d - 0.5, w + 0.5),
                                    (d + 0.5, w + 0.5),
                                    (d + 0.5, w - 0.5))
                        square = Polygon(patch_coords, fc=vcolor)
                        axs.add_artist(square)
                        if vlabel is not None:
                            label_map[day_val] = (square, vlabel)

    # Figure metadata
    fig.suptitle(title, fontsize=16)
    showlegend = len(label_map) > 0
    if showlegend:
        handles = [h for h,l in label_map.values()]
        labels = [l for h,l in label_map.values()]
        if showcb:
            loc = (0.04, 0.01)
        else:
            loc = 'lower center'
        fig.legend(handles, labels, loc=loc, fontsize=10, ncol=3)
    if showcb:
        norm = Normalize(vmin=vmin, vmax=vmax)
        mappable = ScalarMappable(norm=norm, cmap=cmap)
        if showlegend:
            coords = [0.68, 0.027, 0.275, 0.01] if portrait else [0.752, 0.033, 0.208, 0.01]
            cax = fig.add_axes(coords)
        else:
            coords = [0.3625, 0.027, 0.275, 0.01] if portrait else [0.396, 0.033, 0.208, 0.01]
            cax = fig.add_axes(coords)
        fig.colorbar(mappable, cax=cax, orientation='horizontal')
    
    # Final adjustments
    if portrait:
        plt.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.04, wspace=0.12, hspace=0.24)
    else:
        plt.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.04, wspace=0.14, hspace=0.12)

    # Save to file
    plt.savefig(filename)
