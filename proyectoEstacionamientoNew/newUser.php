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

    if (isset($_POST['submit']))
    {
    	$nombre = $_POST['nombre'];
    	$usuario = $_POST['usuario'];
    	$contrasena = $_POST['contrasena'];
    	
    	if(isset($_POST['questionAdmin']))
    		$tipo = $_POST['questionAdmin'];
    	else
    		$tipo = 0;


    	$sql = "INSERT INTO administradores (nombre, username, password, tipo) VALUES ('$nombre', '$usuario', '$contrasena', '$tipo')";
    	
    	if ($conn->query($sql) === TRUE) {
		    echo "<script>alert('Usuario creado exitosamente')</script>";
		} else {
		    echo "<script>alert('Error al crear el usuario, intente de nuevo más tarde...')</script>";
		}

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
			<div class="columns is-centered">
				<div class="column is-6">

	        		<form action="newUser.php" class="box" method="POST">
						<div class="field">
						  <label class="label">Name</label>
						  <div class="control">
						    <input class="input" type="text" placeholder="Ej. David Antonio Torres" required name="nombre">
						  </div>
						</div>

						<div class="field">
						  <label class="label">Username</label>
						  <div class="control has-icons-left has-icons-right">
						    <input class="input" type="text" placeholder="Ej. 1davidant" required name="usuario">
						    <span class="icon is-small is-left">
						      <i class="fas fa-user"></i>
						    </span>
						  </div>
						</div>

						<div class="field">
			              	<label for="" class="label">Password</label>
			              	<div class="control has-icons-left">
			                	<input type="password" placeholder="*********" class="input" required name="contrasena">
			                	<span class="icon is-small is-left">
			                  		<i class="fa fa-lock"></i>
			                	</span>
			              	</div>
			            </div>
			            <br>

						<div class="field">
						  <div class="control">
						    <label class="checkbox">
						      <input type="radio" id="si" name="questionAdmin" value="1">
							  <label for="si">¿Permisos de administrador?</label><br>
						    </label>
						  </div>
						</div>

						<div class="field has-text-centered">
						  <div class="control has-text-centered	">
						    <button class="button is-link is-rounded" type="submit" name="submit">Enviar</button>
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