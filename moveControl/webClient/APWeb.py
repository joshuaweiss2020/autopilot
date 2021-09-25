#!/usr/bin/python3
import cgitb;

cgitb.enable()
import json

print('Content-type: text/html\n')

with open("./conf.json", "r") as f:
    conf = json.load(f)

conf_html = ""
for k in conf.keys():
    conf_html += '''
      <tr>
        <td align="center">{}:{}</td>
      </tr>
    '''.format(k,conf[k])

with open("./AP_picNames.txt", "r") as f:
    filenames = f.read().splitlines()

speed = 40


html = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title> AP. AutoPilot by Joshua</title>

</head>

<script type="text/javascript">

//----------------------AJAX ???? --------------------------

function car_action(cmd) {{
  var speed = document.getElementById("speed").value

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {{
    if (this.readyState == 4 && this.status == 200) {{
      document.getElementById("info").innerHTML = this.responseText;
    }}
  }};
  xhttp.open("GET", "./ctrlWebAction.py?action=" + cmd + "&speed=" + speed, true);
  xhttp.send();
}}

function change_pic() {{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {{
    if (this.readyState == 4 && this.status == 200) {{
        document.getElementById("info").innerHTML = this.responseText;
        document.getElementById("cam").src = "../img/AP/" + this.responseText;
    }}
  }};
  xhttp.open("GET", "./ctrlWebAction.py?action=getLastestPic&speed=0", true);
  xhttp.send();
}}

//__________________________________________ by joshua
function chgSpeed(chgVal){{
//change speed
    speedVal = parseInt(document.getElementById("speed").value)
    speedVal  += chgVal
    document.getElementById("speed").value = speedVal
}}

var timeID = 0
var changePhoto_timeID = 0
var i=0
function t()
{{

}}
function takePhoto(){{
//take one photo
    if (timeID) clearTimeout(timeID)
    car_action('camera_takePhoto')
}}
function collectPhotos(){{
//take photo per 2s
     //timeID = setTimeout("car_action('camera_takePhoto')", 2000)
     car_action('camera_takePhoto')
     document.getElementById("photo").innerHTML = (++i) + ""
     timeID = setTimeout("collectPhotos()", 1000)
}}

function changePhoto(){{
     // document.getElementById("cam").src = "../img/AP/now.jpg"
     //change_pic()
     //changePhoto_timeID = setTimeout("changePhoto()", 3000)
}}

function stopChangePhoto(){{
    if (changePhoto_timeID) clearTimeout(changePhoto_timeID)
}}

</script>


<body class="noselect">
<table width="960" border="0" cellspacing="0" cellpadding="0" class="noselect">
  <tr>
    <td width="160" rowspan="2" align="center"><table width="80%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td align="center"><span class="wordStyle">[AP Arguments]</span></td>
      </tr>
      {}
      <tr>
        <td align="center">&nbsp;</td>
      </tr>
    </table></td>
    <td width="640" rowspan="2"  align="center"><table width="640" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td><img id="cam" src="../img/AP/now.jpg" /> </td>
      </tr>
    </table></td>
    <td width="160" height="288" align="center"><input name="APStart" type="button" class="button" id="APStart" accesskey="b" value="AP START" ontouchstart="car_action('autoPilot');changePhoto()"/></td>
  </tr>
  <tr>
    <td align="center"><input name="APStop" type="button" class="button" id="APStop" accesskey="b" value="AP STOP" ontouchstart="car_action('destroy');stopChangePhoto()"/></td>
  </tr>
  <tr>
    <td colspan="2" align="center">&nbsp;</td>
    <td colspan="2" align="center">&nbsp;</td>
  </tr>
  <tr>
    <td colspan="2" align="center"><p id="info"></p></td>
    <td align="center"><a href='webAPPicList.py' class="wordStyle">Pictures</a></td>
    <td align="center"><input type="button" name="exit" value="EXIT" accesskey="b" ontouchstart="car_action('destroy')"/></td>
  </tr>
  <tr>
    <td colspan="4"><table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td align="center"><table width="300" border="0" bordercolor="0" class="table1">
          <tr>
            <td>&nbsp;</td>
            <td align="center"><span class="text4">Car</span></td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td align="center"><input name="up" type="button" class="button" accesskey="w" ontouchstart="car_action('car_up')" ontouchend="car_action('car_stop')" value="FORWARD"/></td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td><input name="left" type="button" class="button" accesskey="a" ontouchstart="car_action('car_left')"  ontouchend="car_action('car_stop')" value="LEFT" /></td>
            <td align="center"><input name="down" type="button" class="button" accesskey="x" ontouchstart="car_action('car_stop')" value="STOP"/></td>
            <td align="right"><input name="right" type="button" class="button" accesskey="d" ontouchstart="car_action('car_right')" ontouchend="car_action('car_stop')" value="RIGHT"/></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td align="center"><input name="down" type="button" class="button" accesskey="s" ontouchstart="car_action('car_down')"  ontouchend="car_action('car_stop')" value="BACK"/></td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td><input name="speedIncrease" type="button" class="button" value="+" ontouchstart="chgSpeed(2)"/></td>
            <td align="center"><input type='text' class="button" name='speed' id='speed' value='{}'/></td>
            <td><input name="speedDecrease" type="button" class="button" value="-" ontouchstart="chgSpeed(-2)"/></td>
          </tr>
        </table></td>
        <td>&nbsp;</td>
        <td align="center"><table width="300" border="0" class="table1">
          <tr>
            <td>&nbsp;</td>
            <td align="center"><span class="text4">Camera</span></td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td align="center"><input name="up2" type="button" class="button" accesskey="i" ontouchstart="car_action('camera_up')"  ontouchend="car_action('camera_stop')" value="UP"/>
            </td>
            <td>&nbsp;</td>
          </tr>
          <tr>
            <td><input name="left2" type="button" class="button" accesskey="j" ontouchstart="car_action('camera_left')" ontouchend="car_action('camera_stop')" value="LEFT"/></td>
            <td align="center"><input name="down2" type="button" class="button" accesskey="m" ontouchstart="car_action('camera_lookRoad')" value="LOOKROAD"/>
                    <br /></td>
            <td align="right"><input name="right2" type="button" class="button" accesskey="l" ontouchstart="car_action('camera_right')"  ontouchend="car_action('camera_stop')" value="RIGHT"/></td>
          </tr>
          <tr>
            <td>&nbsp;</td>
            <td align="center"><input name="down22" type="button" class="button" accesskey="k" ontouchstart="car_action('camera_down')"  ontouchend="car_action('camera_stop')" value="DOWN"/></td>
            <td align="center"></td>
          </tr>
          <tr>
            <td align="center"><input name="takePhoto" type="button" class="button"  accesskey="p" ontouchstart="takePhoto()" value="Take Photo"/></td>
            <td align="center"><input name="collectPhotos" id="collectPhotos" type="button" class="button"  accesskey="p" ontouchstart="collectPhotos()" value="Collect Photos"/></td>
            <td align="center"><input name="reset" type="button" class="button" accesskey="v" ontouchstart="car_action('camera_reset')" value="RESET"/></td>
          </tr>
        </table></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td colspan="4">&nbsp;
        <p id='photo'>0</p></td>
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
.wordStyle {{
  font-size: 16px;
  font-family: Helvetica, 'Hiragino Sans GB', 'Microsoft Yahei',Arial, sans-serif;
  color: #0000FF
}}
.noselect {{

-webkit-touch-callout: none;

-webkit-user-select: none;
}}
</style>
'''.format(conf_html,speed)
print(html)