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

	    <h1 class="title has-text-centered"> Historial de vehículos </h1>
		<div class="container">
			<div class="columns is-centered">
				<div class="column is-10">
					<br>
					<table width="100%" class="table table-header-gray">
						<tr>
							<th> Id </th>
							<th> Matrícula</th>
							<th> Hora de entrada </th>
							<th> Hora de salida </th>
							<th> Tiempo estacionado </th>
							<th> Costo </th>
							<th> Pago </th>
						</tr>

						<?php
							$sql = "SELECT * FROM ticket INNER JOIN costo ON ticket.costo = costo.ID WHERE status = 0;";
							$result = $conn->query($sql);

							while($row = $result->fetch_assoc()) { ?>

							<tr>
								<td><?php echo $row['ID_ticket']?> </td>
								<td><?php echo $row['matricula'];?> </td>
								<td><?php $entrada = new DateTime($row['entrada']); echo $row['entrada']?> </td>
								<td><?php $salida = new DateTime($row['salida']); echo $row['salida']?> </td>
								<td><?php $dif = date_diff($salida, $entrada); echo $dif->format('%d Días %h Hrs %i Mins %s Seg')?> </td>
								<td><?php echo $row['costoActual']; echo ".00$"?> </td>
								<td><?php echo $row['pago']; echo ".00$"?> </td>
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