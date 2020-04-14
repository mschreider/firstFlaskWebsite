from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot')
def plot():
    import datetime
    from pandas_datareader import data
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2015,12,1)
    end = datetime.datetime(2016,3,10)
    df = data.DataReader(name="GOOG", data_source="yahoo",start=start,end=end) #dataframe object

    # date_increase = df.index[df.Close > df.Open]    # Condition applied to the range
    # date_decrease = df.index[df.Close < df.Open]
    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)
    hours_12 = 12*60*60*1000 # 12 hours conv. to ms
    print(df)

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")   #last parameter = chart adjusts with window size 
    p.title.text = "Candlestick Chart"
    p.grid.grid_line_alpha = 0.3  #Grid Transparency


    # Make candlestick lines
    p.segment(df.index, df.High, df.index, df.Low, color="black") # (X_highest point, Y_highest point, X_lowest point, Y_lowest point)

    # Make candle sticks green if Close Price > Opening Price
    p.rect(df.index[df.Status == "Increase"],
        df.Middle[df.Status == "Increase"], 
        hours_12, 
        df.Height[df.Status == "Increase"], 
        fill_color="green", 
        line_color="black")  # (x,y,width,height,rect color,line color) (Center of rect in X direction, center of rect in Y direction)

    # Make candle sticks red if Close Price < Opening Price
    p.rect(df.index[df.Status == "Decrease"],
        df.Middle[df.Status == "Decrease"], 
        hours_12, 
        df.Height[df.Status == "Decrease"], 
        fill_color="red", 
        line_color="black")  # (x,y,width,height,rect color,line color) (Center of rect in X direction, center of rect in Y direction)

    # Need 4 elements to import to Flask Website
    script1, div1 = components(p)   # Java script for Bokeh chart, HTML for Bokeh chart
    cdn_js = CDN.js_files[0]           # CDN Javascript
    
    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js)

@app.route('/')         #http://localhost:5000/
def home():
    return render_template("home.html")

@app.route('/about/')   #http://localhost:5000/about/
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=False)
    # app.run(port=5000)