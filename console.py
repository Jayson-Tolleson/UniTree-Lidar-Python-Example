#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import subprocess
from subprocess import Popen, PIPE, STDOUT
from flask import Flask, Response, request, render_template, redirect, url_for
import time
app = Flask(__name__, static_url_path='/static')
@app.route('/out/<number>')
def out(number):
  def output():
    yield """<html><style>div#container{background: black;width: 50%;margin: 100px auto;color: white;border-radius: 1em;width: 1200px;height: 1000px;overflow:hidden;overflow-x:hidden;-webkit-resize:vertical;-moz-resize:vertical;} iframe#Frame
{  
    width:1500px;       /* set this to approximate width of entire page you're embedding */
    height:1200px;      /* determines where the bottom of the page cuts off */
    margin-left:00px; /* clipping left side of page */
    margin-top:0px;  /* clipping top of page */
    overflow:hidden;
    /* resize seems to inherit in at least Firefox */
    -webkit-resize:none;
    -moz-resize:none;
    resize:none;
}
</style><body style='color:MediumSeaGreen;'><h1><div id='data' style='text-align: center;'>nothing received yet...for </div></h1><script>var div = document.getElementById('data');</script><script type="text/javascript">
   setInterval(refreshIframe, 1000);
   function refreshIframe() {
       var frame = document.getElementById("Frame");
       frame.src = frame.src;
   }
</script>

<div id='container'><iframe id="Frame" src="/static/xyz.jpg" frameborder="0"></iframe></container>
</body></html>"""
    p = subprocess.Popen('sudo python3 /home/jay/Documents/unitree\ lidar/unitreelidar.py '+str(number), shell=True, stdout=subprocess.PIPE, stderr=STDOUT)
    while True:
        out = ((p.stdout.readline()).strip()) 
        out =str(out)
        if out != "b''":
            print (out)
            yield """<html><body><h1><script>div.innerHTML = "OUTPUT: """+out+""" "</script></h1></body></html>"""
            time.sleep(.04)
  return Response(output())
@app.route('/fishviewer',methods = ['POST', 'GET'])
def searchterms():
    if request.method == 'POST':
        number = request.form['number']
        return redirect(url_for('out', number = number))
    else:
        number = request.args.get('number')
        return """<html><style>body {background: #1339de;} #data { text-align: center; }</style><body><h1>FishViewer!!!</h1><br><br><form method ='POST'>   OPTIONS: ...<br>   Number of Points: <input type="number" name="number" id="number" value="120">   <input type="submit" value="Shoot Lidar Now!!!"></form></body></html>"""
if __name__ == "__main__":  
    app.run(host='0.0.0.0', debug=True, port=80)
