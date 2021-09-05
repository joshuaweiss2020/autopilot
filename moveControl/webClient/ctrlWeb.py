#!/usr/bin/python3
import cgitb;cgitb.enable()
print('Content-type: text/html\n')


times= 3
url = "192.168.1.100:8080"

html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title> AutoPilot by Joshua</title>
<link href="alex_css.css" rel="stylesheet" type="text/css" />
</head>
<script type="text/javascript">

//---------------------------????--------------------

var imageNr = 0; // Serial number of current image
var finished = new Array(); // References to img objects which have finished downloading
var paused = false;

function createImageLayer() {{
  var img = new Image();
  img.style.position = "absolute";
  img.style.zIndex = -1;
  img.onload = imageOnload;
  img.onclick = imageOnclick;
  img.src = "http://{}/?action=snapshot&n=" + (++imageNr);
  var webcam = document.getElementById("webcam");
  webcam.insertBefore(img, webcam.firstChild);
}}

// Two layers are always present (except at the very beginning), to avoid flicker
function imageOnload() {{
  this.style.zIndex = imageNr; // Image finished, bring to front!
  while (1 < finished.length) {{
    var del = finished.shift(); // Delete old image(s) from document
    del.parentNode.removeChild(del);
  }}
  finished.push(this);
  if (!paused) createImageLayer();
}}

function imageOnclick() {{ // Clicking on the image will pause the stream
  paused = !paused;
  if (!paused) createImageLayer();
}}
//---------------------------???? END--------------------

//----------------------AJAX ???? --------------------------

function car_action(cmd) {{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {{
    if (this.readyState == 4 && this.status == 200) {{
      document.getElementById("info").innerHTML = this.responseText;
    }}
  }};
  xhttp.open("GET", "./ctrlWebAction.py?action=" + cmd, true);
  xhttp.send();
}}
</script>


<body onload="createImageLayer();">
<table width="1256" border="0" align="center" class="table1">
  <tr>
    <td align="center" class="text4">Car</td>
    <td width="640" rowspan="3" align="center" ><table width="640" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td>   
	  <div id="webcam" style="position: fixed;top: 0px;"><noscript><img src="http://192.168.1.100:8080/?action=snapshot" /></noscript></div>
    </td>
  </tr>
</table>
</td>
    <td align="center" class="text4">Camera</td>
  </tr>
  <tr>
    <td width="300"><table width="300" border="0" bordercolor="0" class="table1">
      <tr>
        <td>&nbsp;</td>
        <td align="center">
            <input type="button" name="up" value="FORWARD" accesskey="w" onclick="car_action('car_up')"/>        </td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td><input type="button" name="left" value="LEFT" accesskey="a" onclick="car_action('car_left')" /></td>
        <td align="center"><input type="button" name="down" value="STOP" accesskey="x" onclick="car_action('car_stop')"/></td>
        <td align="right"><input type="button" name="right" value="RIGHT" accesskey="d" onclick="car_action('car_right')"/></td>
      </tr>
      <tr>
        <td>&nbsp;</td>
        <td align="center">            <input type="button" name="down" value="BACK" accesskey="s" onclick="car_action('car_down')"/></td>
        <td>&nbsp;</td>
      </tr>
    </table></td>
    <td width="300"><table width="300" border="0" class="table1">
      <tr>
        <td>&nbsp;</td>
        <td align="center"><input type="button" name="up2" value="FORWARD" accesskey="i" onclick="car_action('camera_up')" />        </td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td><input type="button" name="left2" value="LEFT" accesskey="j" onclick="car_action('camera_left')"/></td>
        <td align="center">
          <input type="button" name="down2" value="STOP" accesskey="m" onclick="car_action('camera_stop')"/>
          <br>
          <input type="button" name="reset" value="RESET" accesskey="v" onclick="car_action('camera_reset')"/>
        </td>
        <td align="right"><input type="button" name="right2" value="RIGHT" accesskey="l" onclick="car_action('camera_right')"/></td>
      </tr>
      <tr>
        <td>&nbsp;</td>
        <td align="center"><input type="button" name="down22" value="BACK" accesskey="k" onclick="car_action('camera_down')"/></td>
        <td align="center"></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td><table width="300" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td align="center"><input type="button" name="speedIncrease" value="+" /></td>
        <td align="center">{}</td>
        <td align="center"><input type="button" name="speedDecrease" value="-" /></td>
      </tr>
    </table>    </td>
    <td align="center"><input type="button" name="takePhoto" value="Take Photo"  accesskey="p" /></td>
  </tr>
</table>
<p id="info"></p>
<input type="button" name="exit" value="EXIT" accesskey="b" onclick="car_action('destory')"/>
</body>
</html>
<style>
.table1 {{

    top: 0px;
	
}}
.text4 {{
	font-family: "????";
	font-size: 38px;
	font-weight: normal;
	height: 80px;
	width: 90px;
	border: 2px solid #000099;
	background-position: center;
	text-align: center;
}}
</style>

'''.format(url,times)
print(html)