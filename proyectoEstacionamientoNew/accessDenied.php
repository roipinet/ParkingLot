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
		<div class="container" id="contenido">
			<div class="columns is-centered">
		        <div class="column is-4 has-text-centered">
			        <form action="home.php" class="box" method= "POST">
			        	<p class="text"> Necesitas permisos de administrador.</p>
			        	<br>
			            <div class="field has-text-centered is-large">
			            	<button class="button is-info"> Regresar</button>
			            </div>
			        </form>
		        </div>
		    </div>
		</div>	
	</section>

</body>

<script>

</script>

</html>