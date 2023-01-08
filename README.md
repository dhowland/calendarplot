# calendarplot
Plot daily data on a 1-year calendar using Python and Matplotlib

This project is an adaptation of code posted by @SO_tourist on StackOverflow,
here:  
https://stackoverflow.com/a/61277350

It has not been developed into a full-fledged library at this stage.  I simply
collected it into a form that I find useful and am saving it here for posterity.
As such, the library is half-baked and you should expect to have to hack on it
a little to make it work for you.

## Requirements

- Python 3.6+
- Pandas
- Numpy
- Matplotlib

## Capabilities

The library supports heatmap mode as well as annotated days for defined values.
It will create a file with the given filename in any format supported by
Matplotlib.  The result will be fitted to a 8.5" x 11" page.  The page can be
optionally oriented either landscape or portrait.  The entire plot may be
annotated with defined colors using the highlight map, or it may be entirely
heatmap, or a mixture of both.  The output can contain a legend and/or a color
bar.

## Usage

The module provides one function for plotting the calendar:

`create_year_calendar(df, year, title=None, filename=None, cmap='cool', hlmap={}, showcb=False, portrait=False)`

- `df` (required)  
  the Pandas DataFrame column with the data to plot.  It must be indexed by a
  date timestamp.  The values must be numbers and they must be unique to each
  date.  Dates with no data will be given a value of 0
- `year` (required)  
  the calendar year to plot
- `title`  
  the title of the plot.  If `None`, set to "`year`"
- `filename`  
  the filename to save.  If `None`, set to "`title`.png"
- `cmap`  
  the matplotlib colormap to use
- `hlmap`  
  the highlight map, which is a dictionary of annotation values.  The dict must
  map a data value key to a tuple of `('color', 'Name')` where `'color'` is a
  matplotlib color and `'Name'` is a string that will be used on the legend.
  Use None as the name to exclude a color from the legend
- `showcb`  
  a flag to create a color bar.  `True` to draw a color bar legend
- `portrait`  
  a flag to set page orientation. `True` for portrait, `False` for landscape

## Examples

If you have the following data in CSV format:  

Date       | Value
---------- | -----
1/1/2022   | 1
1/5/2022   | 1
1/7/2022   | 1
1/9/2022   | 2
1/10/2022  | 1
1/14/2022  | 1
1/20/2022  | 1
1/21/2022  | 2
...        | ...

A calendar plot is generated as follows:

```python
import pandas as pd

from calendarplot import create_year_calendar

# load the CSV into a DataFrame
df = pd.read_csv('data.csv')
# convert the date strings to timestamps
df['Date'] = pd.to_datetime(df.Date)
# set the index to the Date column
df.set_index('Date', inplace=True)

# create the highlight map for all possible values, as we intend to cover the
# entire calendar.  Days with no data will get a value of 0 and by using None
# as the description, it won't show up in the legend
hlmap = {0: ('gainsboro', None),
         1: ('lightblue', 'Near Miss'),
         2: ('tomato', 'Hit')}

# create the calendar using the Value column
create_year_calendar(df['Value'], 2022, '2022 Safety Report', 'example.png', hlmap=hlmap)
```

![example plot](example.png)

The following is an example of a heatmap calendar plot:

```python
import random
import datetime
import pandas as pd

from calendarplot import create_year_calendar

# create random data for every day of the year
datelist = []
valuelist = []
d = datetime.date(2022, 1, 1)
while d.year == 2022:
    # Gaussian distribution for a nicer appearance
    v = random.gauss(50, 20)
    # date indexes must be Pandas timestamps
    datelist.append(pd.Timestamp(d))
    valuelist.append(v)
    d += datetime.timedelta(days=1)

# create the DataFrame and set the index to the Date column
df = pd.DataFrame(data={'Date': datelist, 'Value': valuelist})
df.set_index('Date', inplace=True)

# create the calendar using the Value column
create_year_calendar(df['Value'], 2022, '2022 Heatmap', 'example2.png', cmap='Greens', showcb=True)
```

![example plot](example2.png)
