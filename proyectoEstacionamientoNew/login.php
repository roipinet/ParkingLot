<!DOCTYPE html>
<?php
	require_once("configuration.php");
	session_start();
	if (isset($_SESSION['loggedin'])) {  
	    header('location: home.php');
	    }
?>

<html>

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
    <title> Estacionamiento "El Borrego" </title>
</head>

<style>

.navbar-item img {
    max-height: 60px;
}

.hero {
	background: black url(fondo/fondo4.jpg) center / cover;
}

.box {
	opacity: 0.80;
	border: 2px solid #0099FF;
	border-radius: 20px;
}

footer{
    padding: 1rem 1rem 0.5rem !important;
    opacity: 0.70;
}

h1 {
  text-shadow: 1px 0 0 black, -1px 0 0 black, 0 1px 0 black, 0 -1px 0 black, 1px 1px black, -1px -1px 0 black, 1px -1px 0 black, -1px 1px 0 black;
}

.image {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 30%;
} 

</style>


<body>


<section class="hero is-fullheight">

	<div class="hero-head">
	  	<br>
	    <div class="container">
	    
		    <div class="columns is-centered">
		        <div class="column is-4 has-text-centered">
		        	
		        	<figure class="image is-squared">
						<img src="logos/logoEstacionamiento.png">
					</figure>

			        <form action="validarLogin.php" class="box" method= "POST">
			        	<div class="field">
			            	<label for="" class="label has-text-centered">Email</label>
			            	<div class="control has-icons-left">
			            		<input type="text" placeholder="Enter your username..." class="input" required name="username">
			            		<span class="icon is-small is-left">
			                  		<i class="fa fa-envelope"></i>
			                	</span>
			              	</div>
			            </div>
			            
			            <div class="field">
			              	<label for="" class="label has-text-centered">Password</label>
			              	<div class="control has-icons-left">
			                	<input type="password" placeholder="*********" class="input" required name="contrasena">
			                	<span class="icon is-small is-left">
			                  		<i class="fa fa-lock"></i>
			                	</span>
			              	</div>
			            </div>

			            <div class="field has-text-centered is-large">
			            	<button class="button is-info"> Login </button>
			            </div>
			        </form>
		        </div>
		    </div>
	    </div>
	</div>

<footer class="footer">
	<div class="content has-text-centered">
		<p>
  			<strong>Sistemas Embebidos</strong> by Fernando H, Alejandro V, Alejandro H. y Rodrigo L.
		</p>
	</div>
</footer>
</section>

</body>