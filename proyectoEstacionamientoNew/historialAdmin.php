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

    if(isset($_POST['enviar']))
    {
    	if($_POST['enviar']=='1')
    	{
			$sql = "SELECT * FROM ticket INNER JOIN costo ON ticket.costo = costo.ID WHERE status = 0 AND entrada >= '".$_POST['primeraFecha']." 00:00' and salida <= '".$_POST['segundaFecha']. " 23:59';";
			$result = $conn->query($sql);

			echo "<tr> <th> Id </th> <th> Matrícula</th> <th> Hora de entrada </th> <th> Hora de salida </th> <th> Tiempo estacionado </th> <th> Costo </th> <th> Pago </th> </tr>";

			$sumaDinero = 0;
			
			if ($result->num_rows == 0)
			{
				$sumaDinero = 0;
			}

			while($row = $result->fetch_assoc())
			{

				$entrada = new DateTime($row['entrada']);
				$salida = new DateTime($row['salida']);
				$dif = date_diff($salida, $entrada);
				$sumaDinero += $row['pago'];

				echo "<tr class='information'>";
				echo "<td>". $row['ID_ticket']. "</td>";
				echo "<td>". $row['matricula']. "</td>";
				echo "<td>". $row['entrada']. "</td>";
				echo "<td>". $row['salida']. "</td>";
				echo "<td>". $dif->format('%d Días %h Hrs %i Mins %s Seg'). "</td>";
				echo "<td>". $row['costoActual']. ".00$". "</td>";
				echo "<td>". $row['pago']. ".00$". "</td>";
				echo "</tr>";
			}
			echo "<script>var sumaDinero=".$sumaDinero.";</script>";

			$sumaDinero = 0;

			exit;
		}
		else if($_POST['enviar']=='2')
		{

			$sql = "SELECT tipo FROM costo";
			$result = $conn->query($sql);

			while($row = $result->fetch_assoc()) { 
												
			echo "<option>".$row['tipo']. "</option>";

			}

			exit;

		}

		else if($_POST['enviar']=='3')
		{	
			$sql = "SELECT * FROM ticket INNER JOIN costo ON ticket.costo = costo.ID WHERE status = 0 AND entrada >= '". $_POST['hoy']." ".$_POST['primeraHora']."' AND salida <= '".$_POST['hoy']. " ".$_POST['segundaHora']."'";

			$result = $conn->query($sql);

			echo "<tr> <th> Id </th> <th> Matrícula</th> <th> Hora de entrada </th> <th> Hora de salida </th> <th> Tiempo estacionado </th> <th> Costo </th> <th> Pago </th> </tr>";
			$sumaDinero = 0;

			if ($result->num_rows == 0)
			{
				$sumaDinero = 0;
			}

			while($row = $result->fetch_assoc())
			{

				$entrada = new DateTime($row['entrada']);
				$salida = new DateTime($row['salida']);
				$dif = date_diff($salida, $entrada);
				$sumaDinero += $row['pago'];

				echo "<tr class='information'>";
				echo "<td>". $row['ID_ticket']. "</td>";
				echo "<td>". $row['matricula']. "</td>";
				echo "<td>". $row['entrada']. "</td>";
				echo "<td>". $row['salida']. "</td>";
				echo "<td>". $dif->format('%d Días %h Hrs %i Mins %s Seg'). "</td>";
				echo "<td>". $row['costoActual']. ".00$". "</td>";
				echo "<td>". $row['pago']. ".00$". "</td>";
				echo "</tr>";
			}

			echo "<script>var sumaDinero=".$sumaDinero.";</script>";

			$sumaDinero = 0;
			exit;
		}

		else if($_POST['enviar']=='4')
		{
			$sql = "SELECT * FROM ticket INNER JOIN costo ON ticket.costo = costo.ID WHERE status = 0 AND entrada >= '". $_POST['primerFecha']." ".$_POST['primerHora']."' AND salida <= '".$_POST['segundaFecha']. " ".$_POST['segundaHora']."'"."AND tipo='".$_POST['seleccion']."'";
			
			$result = $conn->query($sql);

			echo "<tr> <th> Id </th> <th> Matrícula</th> <th> Hora de entrada </th> <th> Hora de salida </th> <th> Tiempo estacionado </th> <th> Costo </th> <th> Pago </th> </tr>";
			$sumaDinero = 0;

			if ($result->num_rows == 0)
			{
				$sumaDinero = 0;
			}

			while($row = $result->fetch_assoc())
			{

				$entrada = new DateTime($row['entrada']);
				$salida = new DateTime($row['salida']);
				$dif = date_diff($salida, $entrada);
				$sumaDinero += $row['pago'];

				echo "<tr class='information'>";
				echo "<td>". $row['ID_ticket']. "</td>";
				echo "<td>". $row['matricula']. "</td>";
				echo "<td>". $row['entrada']. "</td>";
				echo "<td>". $row['salida']. "</td>";
				echo "<td>". $dif->format('%d Días %h Hrs %i Mins %s Seg'). "</td>";
				echo "<td>". $row['costoActual']. ".00$". "</td>";
				echo "<td>". $row['pago']. ".00$". "</td>";
				echo "</tr>";
			}

			echo "<script>var sumaDinero=".$sumaDinero.";</script>";

			$sumaDinero = 0;
			exit;
		}

		if(isset($_POST['valor']))
			{
				$sql = "SELECT * FROM ticket INNER JOIN costo ON ticket.costo = costo.ID WHERE status = 0 AND tipo = '".$_POST['valor']."'";
				$result = $conn->query($sql);

				echo "<tr> <th> Id </th> <th> Matrícula</th> <th> Hora de entrada </th> <th> Hora de salida </th> <th> Tiempo estacionado </th> <th> Costo </th> <th> Pago </th> </tr>";
				$sumaDinero = 0;

				if ($result->num_rows == 0)
				{
					$sumaDinero = 0;
				}

				while($row = $result->fetch_assoc())
				{

					$entrada = new DateTime($row['entrada']);
					$salida = new DateTime($row['salida']);
					$dif = date_diff($salida, $entrada);
					$sumaDinero += $row['pago'];

					echo "<tr class='information'>";
					echo "<td>". $row['ID_ticket']. "</td>";
					echo "<td>". $row['matricula']. "</td>";
					echo "<td>". $row['entrada']. "</td>";
					echo "<td>". $row['salida']. "</td>";
					echo "<td>". $dif->format('%d Días %h Hrs %i Mins %s Seg'). "</td>";
					echo "<td>". $row['costoActual']. ".00$". "</td>";
					echo "<td>". $row['pago']. ".00$". "</td>";
					echo "</tr>";
				}

				echo "<script>var sumaDinero=".$sumaDinero.";</script>";

				$sumaDinero = 0;
				exit;
			}
    }
?>

<html>

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">
	<link href="bulma-calendar/dist/css/bulma-calendar.min.css" rel="stylesheet">
	<script src="bulma-calendar/dist/js/bulma-calendar.min.js"></script>
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
    <script src="https://code.jquery.com/jquery-3.5.0.min.js" integrity="sha256-xNzN2a4ltkB44Mc/Jz3pT4iU1cmeR0FkXs4pru/JxaQ=" crossorigin="anonymous"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <link rel="stylesheet" href="http://github.hubspot.com/odometer/themes/odometer-theme-default.css" />
	<script src="http://github.hubspot.com/odometer/odometer.js"></script>
    <title> Estacionamiento "El Borrego" </title>
</head>

<style>

.odometer {
    font-size: 40px;
}

.odom {
	font-size: 36px;
	font-family: "Helvetica Neue", sans-serif;
}

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

	    <h1 class="title has-text-centered"> Historial de vehículos </h1>
		
		<div class="tabs is-toggle is-toggle-rounded is-centered">
		  <ul>
		    <li id="fechaButton">
		      <a>
		        <span class="icon is-small"><i class="fas fa-table"></i></span>
		        <span>Fecha</span>
		      </a>
		    </li>
		    <li id="tipoButton">
		      <a>
		        <span class="icon is-small"><i class="fas fa-car"></i></span>
		        <span>Tipo</span>
		      </a>
		    </li>
		    <li id="horaButton">
		      <a>
		        <span class="icon is-small"><i class="fas fa-clock"></i></span>
		        <span>Hora</span>
		      </a>
		    </li>
		    <li id="customButton">
		      <a>
		        <span class="icon is-small"><i class="fas fa-users-cog"></i></span>
		        <span>Personalizado</span>
		      </a>
		    </li>
		  </ul>
		</div>

		<div class="container">
			<div id="espacioPrincipalControl" class="columns is-centered">

			</div>
		</div>

		<br></br>

		<div class="container">
			<div class="columns is-centered">
				<div class="column is-10 is-centered has-text-centered">
					<table width="100%" class="table table-header-gray" id="tabla">

					</table>
					<div id="cuenta" class="odom is-hidden">Ingresos: $<div id="odometer" class="odometer is-hidden"></div> </div>
				</div>
			</div>
		</div>
	</div>
</body>

<script>

	insertarDiv = '<div class="column is-5 has-text-centered" id="espacioCalendario"></div>';
	insertarDiv2 = '<br> <div class="column is-3 has-text-centered" id="espacioSelect"></div>';
	insertarDiv3 = '<br> <div id="odometer" class="odometer"> </div>';
	insertarCalendario = '<br><p class="has-text-weight-bold">Inserte la fecha a consultar </p> <br><input type="date" data-color="info" data-display-mode="dialog" data-date-format="YYYY/MM/DD" data-is-range="true" data-close-on-select="false" id="calendario">';
	insertarHora = '<br><p class="has-text-weight-bold">Inserte la hora a consultar </p> <br>  <input type="time" data-color="info" data-display-mode="dialog" data-date-format="YYYY/MM/DD" data-is-range="true" data-close-on-select="false" id="hora">';
	insertarHoraCalendario = '<br><p class="has-text-weight-bold">Inserte la fecha y hora a consultar </p> <br> <input type="datetime" data-color="info" data-display-mode="dialog" data-date-format="YYYY/MM/DD" data-is-range="true" data-close-on-select="false" id="horaDia">';

	$(fechaButton).click(function()
	{	
		$(fechaButton).addClass("is-active");
		$(tipoButton).removeClass("is-active");
		$(horaButton).removeClass("is-active");
		$(customButton).removeClass("is-active");
		$(".odom, .odometer").addClass("is-hidden");

		$("#espacioCalendario").remove();
		$("#espacioPrincipalControl").html(insertarDiv);
		$("#espacioCalendario").html(insertarCalendario);
		
		// Initialize all input of type date
		var calendar = bulmaCalendar.attach('[type="date"]');

		calendar[0].on('select', function(){

			odometer.innerHTML = 0;

		    rango = calendar[0].value();
		    tokens = rango.split("-");
		    primeraFecha = tokens[0];
		    segundaFecha = tokens[1];

		    $("tr").remove(".information");
		   

		    var parametros = {
		                "enviar" : 1,
		                "primeraFecha" : primeraFecha,
		                "segundaFecha" : segundaFecha
		        };

			$.ajax({
		                data:  parametros,
		                type:  'post',
		                success: function(data) {
		                $("#tabla").html(data);
		                console.log("Ejecutado");
		                $(".odom, .odometer").removeClass("is-hidden");
		                if($(sumaDinero).length)
							odometer.innerHTML = sumaDinero;
		            	}
		            });
		});
	});

	$(tipoButton).click(function()
	{	
		$(fechaButton).removeClass("is-active");
		$(tipoButton).addClass("is-active");
		$(horaButton).removeClass("is-active");
		$(customButton).removeClass("is-active");
		$(".odom, .odometer").addClass("is-hidden");
		$("tr, th").remove();
		$("#espacioCalendario").remove();

		$("#espacioPrincipalControl").html(insertarDiv);
		insertarSelect = '<br> <p class="has-text-weight-bold"> Seleccione el tipo de vehículo </p> <br> <div class="select is-fullwidth has-text-centered"> <select name="selector" id="selector" onChange="functionAux()"><option hidden> </option> </select> </div>'
		$("#espacioCalendario").html(insertarSelect);

		odometer.innerHTML = 0;


		var parametros = {
		                "enviar" : 2,
		        };

		$.ajax({
	                data:  parametros,
	                type:  'post',
	                success: function(data) {
	                $("#selector").append(data);
	                console.log("Ejecutado");

	            	}
	            });

	});

	function functionAux()
	{
		odometer.innerHTML = 0;
		var parametros = {
		                "enviar" : 0,
		                "valor" : document.getElementById("selector").value
		        };

		$.ajax({
	                data:  parametros,
	                type:  'post',
	                success: function(data) {
	                $("#tabla").html(data);
	                console.log(data);
	                $(".odom, .odometer").removeClass("is-hidden");
		                if($(sumaDinero).length)
							odometer.innerHTML = sumaDinero;
	            	}
	            });

	}

	$(horaButton).click(function()
	{	
		$(fechaButton).removeClass("is-active");
		$(tipoButton).removeClass("is-active");
		$(horaButton).addClass("is-active");
		$(customButton).removeClass("is-active");
		$(".odom, .odometer").addClass("is-hidden");
		$("th, tr").remove();
		$("#espacioCalendario").remove();

		$("#espacioPrincipalControl").html(insertarDiv);
		$("#espacioCalendario").html(insertarHora);

		calendarHour = bulmaCalendar.attach('[type="time"]');

		odometer.innerHTML = 0;

		calendarHour[0].on('select', function(){

			odometer.innerHTML = 0;
		    rango = calendarHour[0].value();
		    tokens = rango.split(" ");
		    primeraHora = tokens[0];
		    segundaHora = tokens[2];

		    $("tr").remove(".information");
		    
		    var today = new Date();
			var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();

		    var parametros = {
		                "enviar" : 3,
		                "primeraHora" : primeraHora,
		                "segundaHora" : segundaHora,
		                "hoy" : date
		        };

			$.ajax({
		                data:  parametros,
		                type:  'post',
		                success: function(data) {
		                $("#tabla").html(data);
		                console.log("Ejecutado Hora");
		                $(".odom, .odometer").removeClass("is-hidden");
		                if($(sumaDinero).length)
							odometer.innerHTML = sumaDinero;
		            	}
		            });

		});
	});

	$(customButton).click(function()
	{	
		$(fechaButton).removeClass("is-active");
		$(tipoButton).removeClass("is-active");
		$(horaButton).removeClass("is-active");
		$(customButton).addClass("is-active");
		$(".odom, .odometer").addClass("is-hidden");
		$("th, tr").remove();

		$("#espacioCalendario").remove();
		$("#espacioPrincipalControl").html(insertarDiv);
		$("#espacioCalendario").html(insertarHoraCalendario);

		$("#espacioCalendario").after(insertarDiv2);

		insertarSelect = '<br> <p class="has-text-weight-bold"> Seleccione el tipo de vehículo </p> <br> <div class="select is-fullwidth has-text-centered"> <select name="selector" id="selector" onChange="functionAux2()">  </select> </div>'
		$("#espacioSelect").html(insertarSelect);


		var parametros = {
		                "enviar" : 2
		        };

		$.ajax({
            data:  parametros,
            type:  'post',
            success: function(data) {
            $("#selector").html(data);
            console.log("Ejecutado");
        	}
        });
		
		// Initialize all input of type date
		var calendarandHour = bulmaCalendar.attach('[type="datetime"]');

		calendarandHour[0].on('select', function(){

			odometer.innerHTML = 0;
		    rango = calendarandHour[0].value();
		    tokens = rango.split("-");
		    tokens = rango.split(" ");
		    primerFecha = tokens[0];
		    primerHora = tokens[1];
		    segundaFecha = tokens[3];
		    segundaHora = tokens[4];

		    $("tr").remove(".information");
		   

		    var parametros = {
		                "enviar" : 4,
		                "seleccion" : document.getElementById("selector").value,
		                "primerFecha" : primerFecha,
		                "segundaFecha" : segundaFecha,
		                "primerHora" : primerHora,
		                "segundaHora" : segundaHora
		        };

			$.ajax({
		                data:  parametros,
		                type:  'post',
		                success: function(data) {
		                $("#tabla").html(data);
		                console.log("Ejecutado");
		                $(".odom, .odometer").removeClass("is-hidden");
		                if($(sumaDinero).length)
							odometer.innerHTML = sumaDinero;
		            	}
		            });
		});
	});

	function functionAux2()
	{
		odometer.innerHTML = 0;

		var parametros = {
		                "enviar" : 4,
		                "seleccion" : document.getElementById("selector").value,
		                "primerFecha" : primerFecha,
		                "segundaFecha" : segundaFecha,
		                "primerHora" : primerHora,
		                "segundaHora" : segundaHora
		        };

		$.ajax({
	                data:  parametros,
	                type:  'post',
	                success: function(data) {
	                $("#tabla").html(data);
	                console.log(data);
	                $(".odom, .odometer").removeClass("is-hidden");
		                if($(sumaDinero).length)
							odometer.innerHTML = sumaDinero;
	            	}

	            });

	}
</script>

</html>