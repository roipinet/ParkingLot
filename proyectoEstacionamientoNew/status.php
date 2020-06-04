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
	    
	    <br>

	    <h1 class="title has-text-centered"> Vehículos Actuales </h1>

	    <div>
	    	<h2 class="subtitle has-text-centered"> Hora Actual </h2> 
			<iframe src="https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=es&size=small&timezone=America%2FMexico_City" width="100%" height="90" frameborder="0" seamless sandbox="allow-scripts"></iframe>
		</div>

		<div class="container">
			<div class="columns is-centered">
				<div class="column is-6">
					<table width="100%" class="table table-header-gray">
						<tr>
							<th> Id </th>
							<th> Matrícula</th>
							<th> Hora de entrada </th>
						</tr>

						<?php
							$sql = "SELECT ID_ticket,matricula,entrada FROM ticket WHERE status=1";
							$result = $conn->query($sql);

							while($row = $result->fetch_assoc()) { ?>

							<tr>
								<td><?php echo $row['ID_ticket']?> </td>
								<td><?php echo $row['matricula'];?> </td>
								<td><?php echo $row['entrada'];?> </td>
							</tr>

						<?php } ?>
					</table>
				</div>
			</div>
		</div>
	</section>
</body>

<script>

</script>

</html>