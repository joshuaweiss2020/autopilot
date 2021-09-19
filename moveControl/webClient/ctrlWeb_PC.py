#!/usr/bin/python3
import cgitb;cgitb.enable()
import  json
print('Content-type: text/html\n')

with open("adr.json", "r") as f:
    IP = json.load(f)

times= 3
url = "{}:8080".format(IP)

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
<table width="960" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td colspan="4" align="center"><table width="640" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td><div id="webcam">
          <noscript>
            <img src="http://{}/?action=snapshot" />
            </noscript>
        </div><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><p id="info"></p></td>
    <td align="center"><a href='webList.py' class="STYLE1">Pictures</a></td>
    <td align="center"><input type="button" name="exit" value="EXIT" accesskey="b" onclick="car_action('destory')"/></td>
  </tr>
  <tr>
    <td><table width="300" border="0" bordercolor="0" class="table1">
      <tr>
        <td>&nbsp;</td>
        <td align="center"><span class="text4">Car</span></td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>&nbsp;</td>
        <td align="center"><input name="up" type="button" class="button" accesskey="w" onmousedown="car_action('car_up')" onmouseup="car_action('car_stop')" value="FORWARD"/></td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td><input name="left" type="button" class="button" accesskey="a" onmousedown="car_action('car_left')" onmouseup="car_action('car_stop')" value="LEFT" /></td>
        <td align="center"><input name="down" type="button" class="button" accesskey="x" onclick="car_action('car_stop')" value="STOP"/></td>
        <td align="right"><input name="right" type="button" class="button" accesskey="d" onmousedown="car_action('car_right')" onmouseup="car_action('car_stop')" value="RIGHT"/></td>
      </tr>
      <tr>
        <td>&nbsp;</td>
        <td align="center"><input name="down" type="button" class="button" accesskey="s" onmousedown="car_action('car_down')" onmouseup="car_action('car_stop')" value="BACK"/></td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td><input name="speedIncrease" type="button" class="button" value="+" /></td>
        <td align="center">{}</td>
        <td><input name="speedDecrease" type="button" class="button" value="-" /></td>
      </tr>
    </table></td>
    <td>&nbsp;</td>
    <td colspan="2"><table width="300" border="0" class="table1">
      <tr>
        <td>&nbsp;</td>
        <td align="center"><span class="text4">Camera</span></td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td>&nbsp;</td>
        <td align="center"><input name="up2" type="button" class="button" accesskey="i" onmousedown="car_action('camera_up')"  onmouseup="car_action('camera_stop')" value="FORWARD"/>        </td>
        <td>&nbsp;</td>
      </tr>
      <tr>
        <td><input name="left2" type="button" class="button" accesskey="j" onmousedown="car_action('camera_left')" onmouseup="car_action('camera_stop')" value="LEFT"/></td>
        <td align="center"><input name="down2" type="button" class="button" accesskey="m" onclick="car_action('camera_stop')" value="STOP"/>
            <br /></td>
        <td align="right"><input name="right2" type="button" class="button" accesskey="l" onmousedown="car_action('camera_right')"  onmouseup="car_action('camera_stop')" value="RIGHT"/></td>
      </tr>
      <tr>
        <td>&nbsp;</td>
        <td align="center"><input name="down22" type="button" class="button" accesskey="k" onmousedown="car_action('camera_down')"  onmouseup="car_action('camera_stop')" value="BACK"/></td>
        <td align="center"></td>
      </tr>
      <tr>
        <td colspan="2" align="center"><input name="takePhoto" type="button" class="button"  accesskey="p" onclick="car_action('camera_takePhoto')" value="Take Photo"/></td>
        <td align="center"><input name="reset" type="button" class="button" accesskey="v" onclick="car_action('camera_reset')" value="RESET"/></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td colspan="4">&nbsp;</td>
  </tr>
  <tr>
    <td colspan="4">&nbsp;</td>
  </tr>
</table>

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
.button {{
	font-size: 18px;
	background-color: #666666;
	height: 150px;
	width: 150px;
	color: #99FF00;
	text-align: center;
}}
</style>

'''.format(url,url,times)
print(html)