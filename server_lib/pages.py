#!/usr/bin/env python2.7


def show_then_redirect(count=5,message='Successful Command'):
	html_header_tag = """
	<!DOCTYPE html>
	<html lang="en">
	<head>
	</style>
	  <title>Success</title>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	</head>
	"""
	#
	count_part = '<script type="text/javascript">\n' + '	  var count = ' + str(count) + ';'
	# 
	html_js = """
	  var redirect = "http://192.168.0.8:8080";
	  function countDown(){
	      var timer = document.getElementById("timer");
	      if(count > 0){
	          count--;
	          timer.innerHTML = "This page will redirect in "+count+" seconds.";
	          setTimeout("countDown()", 1000);
	      }else{
	          window.location.href = redirect;
	      }
	  }
	</script>
	<html>
	"""
	html = html_header_tag + count_part + html_js

	body_start = """
	  <body>
	"""
	body_header = '<h1>' + message + '</h1>'

	body_end = """
	  		<span id="timer">
	     	<script type="text/javascript">countDown();</script>
	     	</span>
	  </body>
	"""

	body = body_start + body_header + body_end

	return html + body + '</html>'


def index_form_values(can_start_ambilight,can_start_loop,test=True):
	form_values = []
	# spc = '		'

	# Test
	if test:
		form_values.append('		<p><input type="submit" value="Test" name="action" /></p>')

	# Ambilight
	if can_start_ambilight:
		form_values.append('		<p><input type="submit" value="Start Ambilight" name="action" /></p>')
	else:
		form_values.append('		<p><input type="submit" value="Stop Ambilight" name="action" /></p>')

	# Demo Loop
	if can_start_loop:
		form_values.append('		<p><input type="submit" value="Loop On" name="action" /></p>')
	else:
		form_values.append('		<p><input type="submit" value="Loop Off" name="action" /></p>')

	return ''.join(form_values)


def index(menu=(True,True,True)):
	start = """
	<!DOCTYPE html>
	<html lang="en">
	<head>
	<style>
	input[type=submit] {
	  background: linear-gradient(to bottom right, DeepSkyBlue, RoyalBlue);
	  border: 2px solid black;
	  border-radius: 12px;
	  font-size: 22px;
	  color: white;
	  padding: 16px 32px;
	  margin: 4px 2px;
	  width: 100%;
	}
	</style>
	  <title>Ambilight Control Panel</title>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	</head>
	<html>
	   <body>
	   <script src="/script/jscolor.js"></script>
	   	<div class="container-fluid">
	   		<h1>Ambilight Control Panel</h1>
	   		<form action = "http://192.168.0.8:8080/action" method = "post">
	   		<p>Color:<button class="jscolor {valueElement:'chosen-value', onFineChange:'setTextColor(this)'}">
	   			Pick text color
	   		</button><p/>
	   		<input type="hidden" name="color" value="English" id="color">
	   		<p><input type="submit" value="Color" name="action" /></p>

	   		"""

	end = """
	   		</form>
	   		<script>
	   		function setTextColor(picker) {
	   			document.getElementById("color").value = picker.toRGBString();
	   			document.getElementsByTagName('body')[0].style.color = '#' + picker.toString()
	   		}
	   		</script>
	   	</div>  
	   </body>
	</html>
	"""



	index_page = start + index_form_values(menu[0],menu[1],menu[2]) + end

	return index_page

def redirect_to_index():
	return """
	<!DOCTYPE html>
	<html lang="en">
	<head>
	</style>
	  <title>Success</title>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	</head>
	<script type="text/javascript">
	  var count = 5;
	  var redirect = "http://192.168.0.8:8080";
	  function countDown(){
	      var timer = document.getElementById("timer");
	      if(count > 0){
	          count--;
	          timer.innerHTML = "This page will redirect in "+count+" seconds.";
	          setTimeout("countDown()", 1000);
	      }else{
	          window.location.href = redirect;
	      }
	  }
	</script>
	<html>
	   <body>
	   		<h1>Successful Command</h1>
	   		<span id="timer">
	      <script type="text/javascript">countDown();</script>
	      </span>
	   </body>
	</html>
	"""