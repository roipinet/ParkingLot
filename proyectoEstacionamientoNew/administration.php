<!DOCTYPE html>
<?php

require_once("configuration.php");
session_start();

    if (isset($_SESSION['loggedin'])) {  
    }
    else {
        header('location: sesionExpirada.php');
        exit;
    }

    if($_SESSION['admin']!=1)
    {
    	header('location: accessDenied.php');
    	exit;
    }

    // checking the time now when check-login.php page starts
    // $now = time();           
    // if ($now > $_SESSION['expire']) {
    //     session_destroy();
    //     header('location: sesionExpirada.php');
    //     exit;
    //     }
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

.gray {
	background-color: #575756
}

.table-header-gray th{
		text-align: center !important;
		color: white;
		background-color: #575756;
}

td{
	text-align: center !important;
}



</style> 

<body>

	<section class="hero-head">
		<nav class="navbar gray">
			<div class="container">
				<div class="navbar-brand">
					<div class="navbar-item">
            			<img src="logos/logoEstacionamiento.png">
          			</div>

					<a href="home.php" class="navbar-item has-text-white">
			        	Inicio
			        </a>

			        <a href="administration.php" class="navbar-item has-text-white">
			         	Administración
			        </a>

			        <a href="status.php" class="navbar-item has-text-white">
			         	Estado Actual
			        </a>
			        
			        <a href="historial.php" class="navbar-item has-text-white">
			         	Historial
			        </a>
			    </div>

			    <div class="navbar-end">
			    	<span class="navbar-item has-text-white">
				    	<?php echo $_SESSION['name']; ?>
			    	</span>

			    	<span class="navbar-item">
				    	<a href="logout.php" class="button is-info blanco">
				          LOGOUT
				        </a>
			    	</span>
			    </div>
		    </div>
	    </nav>
	</section>

	<section class="hero-body">
		<div class="container">
			<div class="columns">
				<div class="column is-1"> </div>

				<div class="column is-3 has-text-centered">
					<h1 class="title"> Generar Usuario </h1>
					<a href="newUser.php">
	            		<img src="images/newUser.jpg">
	        		</a>
	        	</div>

	        	<div class="column is-1"> </div>

        		<div class="column is-3 has-text-centered">
        			<h1 class="title"> Historial de ventas </h1>
					<a href="historialAdmin.php">
	            		<img src="images/historial.png">
	        		</a>

	        		<br> </br>
	        		<br> </br>

	        		<form action="home.php">
			            <div class="field">
			            	<button class="button is-info is-fullwidth is-rounded"> MENÚ PRINCIPAL</button>
			            </div>
			        </form>

	        	</div>

	        	<div class="column is-1"> </div>

	        	<div class="column is-3 has-text-centered">
	        		<h1 class="title"> Establecer precios </h1>
					<a href="prices.php">
	            		<img src="images/moneyLogo.png">
	        		</a>
	        	</div>

			</div>

		</div>	
	</section>

</body>

<script>

</script>

</html>