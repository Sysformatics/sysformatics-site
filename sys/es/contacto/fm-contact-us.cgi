#!/usr/bin/perl
use strict;
use warnings;
use Authen::Captcha;
use CGI ;

my $cgi = new CGI ;

# this directory is not accessible via the web.
my $captcha_datadir = "/websites/123reg/LinuxPackage25/sy/sf/or/sysformatics.com/public_html/.captcha_data";

# this directory will store the captcha images. This should
# be accessible via the web because it will be included on the page.
my $captcha_outputdir = "/websites/123reg/LinuxPackage22/sy/sf/or/sysformatics.com/public_html/sys/es/contacto/img";

# This directory is the same as above, but using the web accessible
# URL path.
my $image_dir = "/sys/es/contacto/img";

# This should be the location of the FormMail.cgi script.
my $formmail = "/sys/es/contacto/FormMail.cgi";

# This is where the user should be taken to after submitting the form.
my $redirect = "http://sysformatics.com/sys/es/contacto/email_sent.html";


my $captcha = Authen::Captcha->new(
    data_folder => $captcha_datadir,
    output_folder => $captcha_outputdir,
    );

my ($md5sum, $chars) = $captcha->generate_code(4);
# eliminate ambiguous chars from $chars
my $bad_chars = 1;
while ($bad_chars) {
    if ( $chars =~ m/o|0|O|l|i|1|q|9|6|b|s|S|5|2|Z/) {
        ($md5sum, $chars) = $captcha->generate_code(4);
    } else {
        $bad_chars = 0;
    }
}
my $title      = 'Contact us' ;
my $recipient  = 'info\@sysformatics.com' ;
my $invitation = '
Please enter your name, your email address, a subject, your
message, and the code for humans in the boxes and click send.
We apologise for asking you to enter a code but it blocks
those electronic robots from clogging up our mailbox with spam.

Thank you.
We shall get back to you as soon as possible.
' ;
my $email    ;
my $realname  ;

print $cgi->header () ;

print << "END_OF_HTML";

<!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <title>Sysformatics | Contáctenos</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Sysformatics">
    <meta name="description" content="">
    <meta name="keywords" content=""/>

    <!-- STYLES -->
    <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
    <link href="../../assets/css/bootstrap.min.css" rel="stylesheet">
    <link href="../../assets/css/social-buttons.css" rel="stylesheet">
    <link href="../../assets/css/bootstrap-glyphicons.css" rel="stylesheet">
    <link href="../../assets/css/systrap.css" rel="stylesheet">

    <style type="text/css">

    /* HEADER & LOGOS
    ------------------------------------------------- */
    .header .container {
	background-image: url(../../assets/img/sysformatics.svg);
}
.header h4 {
    padding-top:65px;
}

\@media (min-width: 767px) {
    .thumbnail-fix {min-height:790px;}
}
\@media (min-width: 992px) {
    .thumbnail-fix {min-height:606px;}
}

</style>

    <!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" href="../../assets/ico/apple-touch-icon.png">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">

    <!-- Google Analytics BEGIN -->
    <script type="text/javascript">

    var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-35786145-1']);
_gaq.push(['_trackPageview']);

(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script><!-- Google Analytics END -->

</head>

<body>

<div class="navbar navbar-inverse navbar-fixed-top">

      <!-- Visible Desktop -->
      <div class="hidden-sm">
      <div class="header">
      <div class="container">
      <h4>Soluciones informáticas inteligentes que pueden aprender y evolucionar con su empresa</h4>
      </div>
      </div>
      <div class="navbar-inner">
      <div class="container">
      <ul class="nav navbar-nav">
      <li><a href="../index.html">Inicio</a></li>
      <li class="dropdown">
      <a href="../servicios/" class="dropdown-toggle" data-toggle="dropdown">Servicios <b class="caret"></b></a>
      <ul class="dropdown-menu">
      <li><a href="../servicios/backup/copia-seguridad.html">Copia Seguridad en la Nube</a></li>
      <li><a href="../servicios/email/administracion-email.html">Administración Correo Electrónico</a></li>
      <li><a href="../servicios/web/desarrollo-web.html">Diseño & Desarrollo Web</a></li>
      <li class="divider"></li>
      <li class="dropdown-header">Servicios de Soporte</li>
      <li><a class="dropdown-item-adj" href="../servicios/soporte-ti/soporte-ti.html">Soporte TI</a></li>
      <li><a class="dropdown-item-adj" href="../servicios/soporte-ti/preventivo-ti.html">Mantenimiento Preventivo TI</a></li>
      </ul>
      </li>
      <li class="dropdown">
      <a href="../productos/" class="dropdown-toggle" data-toggle="dropdown">Productos <b class="caret"></b></a>
      <ul class="dropdown-menu">
      <li><a href="../productos/prioritix/prioritix.html">PrioritiX</a></li>
      <li><a href="../productos/syschecker/syschecker.html">SysChecker</a></li>
      <li class="divider"></li>
      <li class="dropdown-header">Proyectos Redes Sociales</li>
      <li><a class="dropdown-item-adj" href="http://www.wisebirk.com" target="_blank">Wisebirk</a></li>
      <li><a class="dropdown-item-adj" href="http://www.ummahsocialbook.com" target="_blank">Ummah Social Book</a></li>
      </ul>
      </li>
      <li><a href="../soporte/soporte.html">Soporte</a></li>
      <li class="dropdown">
      <a href="../acerca-de/" class="dropdown-toggle" data-toggle="dropdown">Acerca de <b class="caret"></b></a>
      <ul class="dropdown-menu">
      <li><a href="../acerca-de/quienes-somos.html">Quiénes Somos</a></li>
      </ul>
      </li>
      <li class="active"><a href="../contacto/fm-contact-us.cgi">Contáctenos</a></li>
      </ul>
      <ul class="nav navbar-nav pull-right">
      <li class="btn-warning"><a href="../tienda/tienda.html">Tienda</a></li>
      </ul>
      </div>
      </div>
      </div><!-- End Visible Desktop -->

           <!-- Hidden Desktop -->
      <div class="visible-sm">
	<div class="navbar-inner-nav">
	  <div class="container">
	    <div class="col-1 col-sm-1" style="padding-right:0;padding-left:0">
	      <button type="button" class="navbar-toggle" style="left:-15px" data-toggle="collapse" data-target=".nav-collapse">
		<span class="icon-bar"></span>
		<span class="icon-bar"></span>
		<span class="icon-bar"></span>
	      </button>
	    </div>
	    <div class="col-5 col-sm-5" style="padding-left:0;padding-right:0">
	      <a class="navbar-brand" href="../index.html">Sysformatics</a>
	    </div>
	    <div class="col-6 col-sm-6" style="text-align:right;padding-right:5px;padding-left:0">
	      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href='../tienda/tienda.html'">
		<span class="glyphicon glyphicon-shopping-cart"></span>
	      </button>
	      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href='../contacto/fm-contact-us.cgi'">
		<span class="glyphicon glyphicon-comment"></span>
	      </button>
	      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href='../soporte/soporte.html'">
		<span class="glyphicon glyphicon-asterisk"></span>
	      </button>
	    </div>

	    <div class="nav-collapse collapse">
	      <ul class="topnav nav navbar-nav navbar-nav-sm">		
		<li class="dropdown-sm header-link"><a href="../tienda/tienda.html">Tienda</a></li>
		<li class="dropdown dropdown-sm">
		  <a class="dropdown-toggle" data-toggle="collapse">Servicios <b class="caret"></b></a>
		  <ul class="nav navbar-nav-sub-sm">
		    <li><a href="../servicios/backup/copia-seguridad.html">Copia Seguridad en la Nube</a></li>
		    <li><a href="../servicios/email/administracion-email.html">AdministraciÃ³n Correo ElectrÃ³nico</a></li>
		    <li><a href="../servicios/web/desarrollo-web.html">DiseÃ±o & Desarrollo Web</a></li>
                    <li class="divider"></li>
                    <li><a class="dropdown-item-adj" href="../servicios/soporte-ti/soporte-ti.html">Soporte TI</a></li>
                    <li><a class="dropdown-item-adj" href="../servicios/soporte-ti/preventivo-ti.html">Mantenimiento Preventivo TI</a></li>
		  </ul>
		</li>
		<li class="dropdown dropdown-sm">
		  <a class="dropdown-toggle" data-toggle="collapse">Productos <b class="caret"></b></a>
		  <ul class="nav navbar-nav-sub-sm">
                    <li><a href="../productos/prioritix/prioritix.html">PrioritiX</a></li>
                    <li><a href="../productos/syschecker/syschecker.html">SysChecker</a></li>
                    <li class="divider"></li>
                    <li><a class="dropdown-item-adj" href="http://www.wisebirk.com" target="_blank">Wisebirk</a></li>
                    <li><a class="dropdown-item-adj" href="http://www.ummahsocialbook.com" target="_blank">Ummah Social Book</a></li>
		  </ul>
		</li>
		<li class="dropdown-sm header-link"><a href="../soporte/soporte.html">Soporte</a></li>
		<li class="dropdown dropdown-sm">
		  <a class="dropdown-toggle" data-toggle="collapse">Acerca de <b class="caret"></b></a>
		    <ul class="nav navbar-nav-sub-sm">
		      <li><a href="../acerca-de/quienes-somos.html">Quiénes somos</a></li>
		    </ul>
		</li>
		<li class="dropdown-sm header-link"><a href="../contacto/fm-contact-us.cgi">Contáctenos</a></li>
	      </ul>
	    </div><!-- End nav-collapse -->
	  </div>
	</div>
      </div><!-- End Hidden Desktop -->
      </div><!-- End Header & Menu bar -->

      <div class="container">
      <img src="../../assets/img/ID-201308201759.jpg" class="img-responsive" alt="">
      <h2 class="margin-fix">Contacte Sysformatics</h2>
      <div class="row">
      <div class="col-lg-4 col-sm-4">
      <div class="thumbnail thumbnail-fix">
      <div class="caption">
      <h3 class="h3-fix">Consultas</h3>
      <address>
      <dotted-underline>Email:</dotted-underline> <a href="mailto:info\@sysformatics.com">info&#64;sysformatics.com</a><br>
      <dotted-underline>Skype:</dotted-underline> <a href="skype:info.sysformatics?call">info.sysformatics</a>
      </address>
      <h3 class="h3-fix">Soporte</h3>
      <address>
      <dotted-underline>Email:</dotted-underline>  <a href="mailto:support&#64;sysformatics.com">support&#64;sysformatics.com</a><br>
      <dotted-underline>Skype:</dotted-underline> <a href="skype:support.sysformatics?call">support.sysformatics</a>
      </address><br>
      <h3 class="h3-fix">Directorio de Oficinas</h3>
      <address>
      <strong>AMERICAS</strong><br>
      Calle 8A 11E-31<br>
      Cúcuta, Norte de Santander<br>
      Colombia<br>
      <dotted-underline>Tel:</dotted-underline> +57 (9) 7595 0046<br/>
      </address>
      <address>
      <strong>EMEA</strong><br>
      11 Thessaly Road<br>
      London, SW8 4XN<br>
      United Kingdom<br>
      <dotted-underline>Tel:</dotted-underline> +44 (0) 79466 07895<br/>
      </address>
      </div>
      </div>
      </div>
      <div class="col-lg-8 col-sm-8">
      <div class="thumbnail thumbnail-fix">
      <div class="caption">
      <h3 class="h3-fix">Comentarios</h3>
      <p>¿Tiene alguna pregunta o comentario acerca de los productos y servicios de Sysformatics?<br>
      <small>Por favor llene el siguiente formulario. Responderemos  a sus preguntas y comentarios lo antes posible.</small></p>
      <form  action="/sys/es/contacto/FormMail.cgi" method='post'>
      <div class="row">
      <div class="col-lg-6">
      <div class="form-group">
      <label for="nombre">Nombre</label>
      <input type="text" class="form-control" id="feedbackInputFirstName1" name='nombre' placeholder="Ingrese nombre">
      </div>
      </div>
      <div class="col-lg-6">
      <div class="form-group">
      <label for="apellido">Apellido</label>
      <input type="text" class="form-control" id="feedbackInputLastName1" name='apellido' placeholder="Ingrese apellido">
      </div>
      </div>
      </div>
      <div class="row">
      <div class="col-lg-6">
      <div class="form-group">
      <label for="email">Correo electrónico</label>
      <input type="email" class="form-control" id="feedbackInputEmail1" name='email' placeholder="Ingrese email">
      </div>
      </div>
      <div class="col-lg-6">
      <div class="form-group">
      <label for="telefono" style="width:100%">Teléfono <small class="pull-right text-muted" style="padding-top:2px;padding-right:3px">Opcional</small></label>
      <input type="tel" class="form-control" id="feedbackInputTelephone1" name='telefono' placeholder="Ingrese teléfono">
      </div>
      </div>
      </div>
      <div class="form-group">
      <label for="asunto">Asunto</label>
      <input type="text" class="form-control" id="feedbackInputSubject1" name='asunto' placeholder="Ingrese asunto">
      </div>
      <div class="form-group">
      <label for="mensaje">Mensaje</label>
      <textarea class="form-control" rows="3" id="feedbackInputMessage1" name='mensaje' wrap=virtual></textarea>
      </div>
      <div class="form-group">
      <label for="captcha">Ingrese las letras</label>
      <div class="row">
      <div class="col-sm-3">
      <img src="/sys/es/contacto/img/$md5sum.png" />
      </div>
      <div class="visible-sm">
      <br>
      </div>
      <div class="col-sm-9">
      <input type="text" class="form-control" name="captcha-text" id="captcha-text" />
      </div>      
      </div>
      </div>
      <button type="submit" class="btn btn-primary">Enviar</button>
      <input type='hidden' name='recipient' value='info\@sysformatics.com' >
      <input type='hidden' name='redirect' value="http://sysformatics.com/sys/es/contacto/Formulario-enviado.html" >
      <input type='hidden' id="catch" name='captcha-md5sum' value="$md5sum" >
      <input type='hidden' name="required" value="email,nombre,apellido,asunto,mensaje">
      </form>
      </div>
      </div>
      </div>
      </div>
      
      <footer class="footer-margin">
      <p lang="en"><a href="../../en/contact/fm-contact-us.cgi">English</a></p>
      <hr>
      <p><a href="../tienda/tienda.html">Tienda</a> &middot; <a href="../soporte/soporte.html">Soporte</a> &middot; <a href="../acerca-de/quienes-somos.html">Quiénes Somos</a> &middot; <a href="../contacto/fm-contact-us.cgi">Contáctenos</a></p>
      <p>&copy; 2013 Sysformatics.</p>
      </footer>

      </div> <!-- /container -->

      <!-- Javascript
      ================================================== -->
      <script src="http://code.jquery.com/jquery.js"></script>
      <script src="../../assets/js/bootstrap.min.js"></script>
      
<!-- Accordion dropdown menu helper -->
    <script src="../../assets/js/jquery-ui-1.10.3.accordion.js"></script>

    <script>
      // Accordion dropdown menu
      jQuery(function() {
      jQuery( ".topnav" ).accordion({active: "a.default",alwaysOpen: true,autoHeight:false,clearStyle: true,collapsible: true});
      });
      
      //capture the click on the a tag
      jQuery(".topnav  .header-link a").click(function() {
      window.location = jQuery(this).attr('href');
      return false;
      });
    </script>

      <!-- AddThis Smart Layers BEGIN -->
      <!-- Go to http://www.addthis.com/get/smart-layers to customize -->
      <script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-520259f274c70552"></script>
      <script type="text/javascript">
      addthis.layers({
	  'theme' : 'gray',
	  'share' : {
	      'position' : 'right',
	      'numPreferredServices' : 4
	  }, 
		  'follow' : {
		      'services' : [
			  {'service': 'facebook', 'id': 'pages/Sysformatics/482146858508732'},
			  {'service': 'twitter', 'id': 'Sysformatics'},
			  {'service': 'linkedin', 'id': 'sysformatics', 'usertype': 'company'}
			  ]
	      }   
		     });
    </script><!-- AddThis Smart Layers END -->

	<!-- Google Analytics BEGIN -->
	<script type="text/javascript">

	var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-35786145-1']);
    _gaq.push(['_trackPageview']);

    (function() {
	var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script><!-- Google Analytics END -->

</body></html>
END_OF_HTML
