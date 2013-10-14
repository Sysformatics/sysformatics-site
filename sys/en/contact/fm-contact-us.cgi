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
my $captcha_outputdir = "/websites/123reg/LinuxPackage22/sy/sf/or/sysformatics.com/public_html/sys/en/contact/img";

# This directory is the same as above, but using the web accessible
# URL path.
my $image_dir = "/sys/en/contact/img";

# This should be the location of the FormMail.cgi script.
my $formmail = "/sys/en/contact/FormMail.cgi";

# This is where the user should be taken to after submitting the form.
my $redirect = "http://sysformatics.com/sys/en/contact/email_sent.html";


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
    <html lang="en">
    <head>
    <title>Sysformatics | Contact us</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="Sysformatics">
    <meta name="description" content="Contact Sysformatics">
    <meta name="keywords" content="sysformatics,contact sysformatics,business contact">

    <!-- STYLES -->
    <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet">
    <link href="../../assets/css/bootstrap.min.css" rel="stylesheet">
    <link href="../../assets/css/social-buttons.css" rel="stylesheet">
    <link href="../../assets/css/bootstrap-glyphicons.css" rel="stylesheet">
    <link href="../../assets/css/systrap.css" rel="stylesheet">
    <link href="../../assets/css/contact.css" rel="stylesheet">
    
    <!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" href="../../assets/ico/apple-touch-icon.png">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">
    
    </script>
    
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
      <h4>Intelligent information solutions that can learn and evolve with your business</h4>
      </div>
      </div>
      <div class="navbar-inner">
      <div class="container">
      <ul class="nav navbar-nav">
      <li><a href="../../../index.html">Home</a></li>
      <li class="dropdown">
      <a href="../services/" class="dropdown-toggle" data-toggle="dropdown">Services <b class="caret"></b></a>
      <ul class="dropdown-menu">
      <li><a href="../services/backup/backup.html">Online Backup</a></li>
      <li><a href="../services/email/email-man.html">Email Management</a></li>
      <li><a href="../services/web/web-design.html">Web Design & Development</a></li>
      <li class="divider"></li>
      <li class="dropdown-header">Support Services</li>
      <li><a class="dropdown-item-adj" href="../services/it-support/it-support.html">IT Support Services</a></li>
      <li><a class="dropdown-item-adj" href="../services/it-support/it-preventive.html">IT Preventive Maintenance</a></li>
      </ul>
      </li>
      <li class="dropdown">
      <a href="../products/" class="dropdown-toggle" data-toggle="dropdown">Products <b class="caret"></b></a>
      <ul class="dropdown-menu">
      <li><a href="../products/prioritix/prioritix.html">PrioritiX</a></li>
      <li><a href="../products/syschecker/syschecker.html">SysChecker</a></li>
      </ul>
      </li>
      <li><a href="../support/support.html">Support</a></li>
      <li class="dropdown">
      <a href="../about/" class="dropdown-toggle" data-toggle="dropdown">About <b class="caret"></b></a>
      <ul class="dropdown-menu">
      <li><a href="../about/about-us.html">About us</a></li>
      </ul>
      </li>
      <li class="active"><a href="../contact/fm-contact-us.cgi">Contact us</a></li>
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
      <a class="navbar-brand" href="../../../index.html">Sysformatics</a>
      </div>
      <div class="col-6 col-sm-6" style="text-align:right;padding-right:5px;padding-left:0"> 
      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href='../contact/fm-contact-us.cgi'">
      <span class="glyphicon glyphicon-comment"></span>
      </button>
      
      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href='../support/support.html'">
      <span class="glyphicon glyphicon-asterisk"></span>
      </button>
      </button>
      </div>

      <div class="nav-collapse collapse">
      <ul class="topnav nav navbar-nav navbar-nav-sm">		
      <li class="dropdown dropdown-sm">
      <a class="dropdown-toggle" data-toggle="collapse">Services <b class="caret"></b></a>
      <ul class="nav navbar-nav-sub-sm">
      <li><a href="../services/backup/backup.html">Online Backup</a></li>
      <li><a href="../services/email/email-man.html">Email Management</a></li>
      <li><a href="../services/web/web-design.html">Web Design & Development</a></li>
      <li class="divider"></li>
      <li><a class="dropdown-item-adj" href="../services/it-support/it-support.html">IT Support Support</a></li>
      <li><a class="dropdown-item-adj" href="../services/it-support/it-preventive.html">IT Preventive Maintenance</a></li>
      </ul>
      </li>
      <li class="dropdown dropdown-sm">
      <a class="dropdown-toggle" data-toggle="collapse">Products <b class="caret"></b></a>
      <ul class="nav navbar-nav-sub-sm">
      <li><a href="../products/prioritix/prioritix.html">PrioritiX</a></li>
      <li><a href="../products/syschecker/syschecker.html">SysChecker</a></li>
      </ul>
      </li>
      <li class="dropdown-sm header-link"><a href="../support/support.html">Support</a></li>
      <li class="dropdown dropdown-sm">
      <a class="dropdown-toggle" data-toggle="collapse">About <b class="caret"></b></a>
      <ul class="nav navbar-nav-sub-sm">
      <li><a href="../about/about-us.html">About us</a></li>
      </ul>
      </li>
      <li class="dropdown-sm header-link"><a href="../contact/fm-contact-us.cgi">Contact us</a></li>
      </ul>
      </div><!-- End nav-collapse -->
      </div>
      </div>
      </div><!-- End Hidden Desktop -->
      </div><!-- End Header & Menu bar -->

      <div class="container">

      <img src="../../assets/img/ID-201308201759.jpg" class="img-responsive" alt="">
      <h2 class="margin-fix">Contact Sysformatics</h2>
      
      <div class="row">
      <div class="col-lg-4 col-sm-4">
      <div class="thumbnail thumbnail-fix">
      <div class="caption">
      <h3 class="h3-fix">Enquiries</h3>
      <address>
      <dotted-underline>Email:</dotted-underline> <a href="mailto:info&#64;sysformatics.com">info&#64;sysformatics.com</a><br>
      <dotted-underline>Skype:</dotted-underline> <a href="skype:info.sysformatics?call">info.sysformatics</a>
      </address>
      <h3 class="h3-fix">Support</h3>
      <address>
      <dotted-underline>Email:</dotted-underline>  <a href="mailto:support&#64;sysformatics.com">support&#64;sysformatics.com</a><br>
      <dotted-underline>Skype:</dotted-underline> <a href="skype:support.sysformatics?call">support.sysformatics</a>
      </address><br>
      <h3 class="h3-fix">Office Directory</h3>
      <address>
      <strong>EMEA</strong><br>
      11 Thessaly Road<br>
      London, SW8 4XN<br>
      United Kingdom<br>
      <dotted-underline>Tel:</dotted-underline> +44 (0) 79466 07895<br/>
      </address>
      <address>
      <strong>AMERICAS</strong><br>
      Calle 8A 11E-31<br>
      Cúcuta, Norte de Santander<br>
      Colombia<br>
      <dotted-underline>Tel:</dotted-underline> +57 (9) 7595 0046<br/>
      </address>
      </div>
      </div>
      </div>
      <div class="col-lg-8 col-sm-8">
      <div class="thumbnail thumbnail-fix">
      <div class="caption">
      <h3 class="h3-fix">Feedback</h3>
      <p>Have a question or comment about Sysformatics products and services?<br>
      Please fill out the form below. We will respond to questions and comments as quickly as possible.</p>
      <form  action="/sys/en/contact/FormMail.cgi" method='post'>
      <div class="row">
      <div class="col-lg-6">
      <div class="form-group">
      <label for="firstname">First name</label>
      <input type="text" class="form-control" id="feedbackInputFirstName1" name='realname' placeholder="Enter first name">
      </div>
      </div>
      <div class="col-lg-6">
      <div class="form-group">
      <label for="lastname">Last name</label>
      <input type="text" class="form-control" id="feedbackInputLastName1" name='lastname' placeholder="Enter last name">
      </div>
      </div>
      </div>
      <div class="row">
      <div class="col-lg-6">
      <div class="form-group">
      <label for="email">Email address</label>
      <input type="email" class="form-control" id="feedbackInputEmail1" name='email' placeholder="Enter email">
      </div>
      </div>
      <div class="col-lg-6">
      <div class="form-group">
      <label for="telephone" style="width:100%">Telephone <small class="pull-right text-muted" style="padding-top:2px;padding-right:3px">Optional</small></label>
      <input type="tel" class="form-control" id="feedbackInputTelephone1" name='telephone' placeholder="Enter telephone">
      </div>
      </div>
      </div>
      <div class="form-group">
      <label for="subject">Subject</label>
      <input type="text" class="form-control" id="feedbackInputSubject1" name='subject' placeholder="Enter summary">
      </div>
      <div class="form-group">
      <label for="message">Message</label>
      <textarea class="form-control" rows="3" id="feedbackInputMessage1" name='message' wrap=virtual></textarea>
      </div>
      <div class="form-group">
      <label for="captcha">Enter the letters</label>
      <div class="row">
      <div class="col-sm-3">
      <img src="/sys/en/contact/img/$md5sum.png" />
      </div>
      <div class="visible-sm">
      <br>
      </div>
      <div class="col-sm-9">
      <input type="text" class="form-control" name="captcha-text" id="captcha-text" />
      </div>
      
      </div>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
      <input type='hidden' name='recipient' value='info\@sysformatics.com' >
      <input type='hidden' name='redirect' value="http://sysformatics.com/sys/en/contact/form-sent.html" >
      <input type='hidden' id="catch" name='captcha-md5sum' value="$md5sum" >
      <input type='hidden' name="required" value="email,realname,lastname,subject,message">
      </form>
      </div>
      </div>
      </div>
      </div>
      
      <footer class="footer-margin">
      <p lang="es"><a href="../../es/contacto/fm-contact-us.cgi">Español</a></p>
      <hr>
      <p><a href="../support/support.html">Support</a> &middot; <a href="../about/about-us.html">About</a> &middot; <a href="../contact/fm-contact-us.cgi">Contact</a></p>
      <p>&copy; 2013 Sysformatics.</p>
      </footer>
      
      </div><!-- /container -->

      <!-- Javascript
      ================================================== -->
      <script src="http://code.jquery.com/jquery.js"></script>
      <script src="../../assets/js/bootstrap.min.js"></script>

      <!-- Accordion dropdown menu helper -->
      <script src="../../assets/js/jquery-ui-1.10.3.accordion.js"></script>
      
      <script typpe="text/javascript">
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
