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

    if (isset($_POST['submit']))
    {
    	$costoActualizado = $_POST['newCost'];
    	$nombreActualizado = $_POST['selector'];

    	$sql = "UPDATE costo SET precio = '$costoActualizado' WHERE tipo = " . '"' .$nombreActualizado.'"';

    	if ($conn->query($sql) === TRUE) {
		    echo "<script>alert('Cambio realizado exitosamente')</script>";
		} else {
		    echo "<script>alert('Error al modificar el costo, intente de nuevo más tarde...')</script>";
		}
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

	<section>
		<div class="hero-body">
			<div class="container">
				<div class="columns is-centered">
					<div class="column is-6">
						<h1 class="title has-text-centered"> Lista de precios actual </h1>
							<table width="100%" class="table table-header-gray">
								<tr>
									<th> Tipo de Vehículo </th>
									<th> Costo por hora ó fracción</th>
								</tr>

								<?php
									$sql = "SELECT tipo,precio FROM costo";
									$result = $conn->query($sql);

									while($row = $result->fetch_assoc()) { ?>

									<tr>
										<td><?php echo $row['tipo']?> </td>
										<td><?php echo $row['precio'];?>.00$ </td>
									</tr>

								<?php } ?>
							</table>

						<div class="field has-text-centered">
			            	<button class="button is-warning is-rounded has-text-centered modal-button" data-target="#myModal" aria-haspopup="true"> Modificar precio </button>
			            </div>
			        </div>
			    </div>
			</div>
		</div>

        <div class="modal" id="myModal">
		  
				<div class="modal-background"></div>
				  
				<div class="modal-card">
			    
				    <header class="modal-card-head">
				      <p class="modal-card-title has-text-centered">Modificación de precios</p>
				      <button class="delete modal-delete" aria-label="close"></button>
				    </header>

				    <form action="" method="POST">

				    <section class="modal-card-body">
				     	<div class="container has-text-centered">
				      		
				     		<div class="columns is-centered">
				     			<div class="column is-3 is-centered">
				     				Seleccione el tipo
						      		<div class="select is-rounded">
								  		<select name="selector">
									    	<?php

												$sql = "SELECT tipo,precio FROM costo";
												$result = $conn->query($sql);

												while($row = $result->fetch_assoc()) { ?>
												
												<option><?php echo $row['tipo']?> </option>

											<?php } ?>
									  	</select>
									</div>

									<div>
										<br>Ingrese el costo
									</div>

									<p class="control has-icons-left has-icons-right">
									    <input class="input" type="text" placeholder="20.00" name="newCost">
									    <span class="icon is-small is-left">
									      <i class="fas fa-dollar-sign"></i>
									    </span>
									</p>

								</div>
							</div>
				      	</div>
				    </section>
				    
				    <footer class="modal-card-foot">
				    	<div class="container has-text-centered">
				            <div class="field has-text-centered">
				            	<button class="button is-success has-text-centered" name="submit">Guardar cambios</button>
				            </div>
					    </div>
				    </footer>
					
					</form>
			    
			<button class="modal-close is-large" aria-label="close"></button>
	
	</section>

</body>

<script>

	document.querySelectorAll('.modal-button').forEach(function(el) {
	  el.addEventListener('click', function() {
	    var target = document.querySelector(el.getAttribute('data-target'));
	    
	    target.classList.add('is-active');
	    
	    target.querySelector('.modal-close').addEventListener('click',   function() {
	        target.classList.remove('is-active');
	     });

	    target.querySelector('.modal-delete').addEventListener('click',   function() {
	        target.classList.remove('is-active');
	     });

	  });
	});

</script>

</html>