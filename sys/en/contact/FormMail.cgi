#!/usr/bin/perl
##############################################################################
# FormMail                        Version 1.92x                              #
# Copyright 1995-2002 Matt Wright mattw@scriptarchive.com                    #
# Created 06/09/95                Last Modified 04/21/02                     #
# Matt's Script Archive, Inc.:    http://www.scriptarchive.com/              #
##############################################################################
# COPYRIGHT NOTICE                                                           #
# Copyright 1995-2002 Matthew M. Wright  All Rights Reserved.                #
#                                                                            #
# FormMail may be used and modified free of charge by anyone so long as this #
# copyright notice and the comments above remain intact.  By using this      #
# code you agree to indemnify Matthew M. Wright from any liability that      #
# might arise from its use.                                                  #
#                                                                            #
# Selling the code for this program without prior written consent is         #
# expressly forbidden.  In other words, please ask first before you try and  #
# make money off of my program.                                              #
#                                                                            #
# Obtain permission before redistributing this software over the Internet or #
# in any other medium. In all cases copyright and header must remain intact. #
##############################################################################
# ACCESS CONTROL FIX: Peter D. Thompson Yezek                                #
#                     http://www.securityfocus.com/archive/1/62033           #
##############################################################################
# Define Variables                                                           #
#      Detailed Information Found In README File.                            #

# $mailprog defines the location of your sendmail program on your unix       #
# system. The flags -i and -t should be passed to sendmail in order to       #
# have it ignore single dots on a line and to read message for recipients    #

$mailprog = '/usr/sbin/sendmail -i -t -odb';

# @referers allows forms to be located only on servers which are defined     #
# in this field.  This security fix from the last version which allowed      #
# anyone on any server to use your FormMail script on their web site.        #

@referers = ('sysformatics.com');

# @recipients defines the e-mail addresses or domain names that e-mail can   #
# be sent to.  This must be filled in correctly to prevent SPAM and allow    #
# valid addresses to receive e-mail.  Read the documentation to find out how #
# this variable works!!!  It is EXTREMELY IMPORTANT.                         #
@recipients = &fill_recipients(@referers);

# ACCESS CONTROL FIX: Peter D. Thompson Yezek                                #
# @valid_ENV allows the sysadmin to define what environment variables can    #
# be reported via the env_report directive.  This was implemented to fix     #
# the problem reported at http://www.securityfocus.com/bid/1187              #

@valid_ENV = ('REMOTE_HOST','REMOTE_ADDR','REMOTE_USER','HTTP_USER_AGENT');

# Stealth tweak: set $stealth=1 and an invalid referrer will raise a 404     #
# error. You don't want this if you have to use a system that actually can't #
# set a referrer.                                                            #

$stealth=0;

# Captcha support to help get rid of pesky scammers.                         #
# Set to 1 to enable.                                                        #
# When enabled your submitting form must contain two inputs.                 #
# The first should be called captcha-md5sum and should contain only the      #
# md5sum of the loaded captcha.                                              #
# The second input should be called captcha-text and will be where the user  #
# types in what they think is the captcha text.                              #
# Without these two fields the captcha authentication cannot be passed.      #

$captcha_enabled=1;

# You MUST create the following directories yourself. FormMail will not work #
# without them, unless you are not using Captcha support.                    #

# Set this to a directory that is not accessible via the web.                #
# Often something like /home/yourname/.captcha_data
$captcha_datadir = "/websites/123reg/LinuxPackage25/sy/sf/or/sysformatics.com/public_html/.captcha_data";

# Set this to a directory that will store the captcha images. This should    #
# be accessible via the web because it will be included on the page.         #
# Often something like /home/yourname/public_html/captcha_img
$captcha_outputdir = "/websites/123reg/LinuxPackage22/sy/sf/or/sysformatics.com/public_html/sys/en/contact/img";

# NOTE: This is version 1.92x, a third-party modification that fixes more    #
# security holes. Do NOT replace this with version 1.92.                     #

# Done                                                                       #
##############################################################################

# Check Referring URL
&check_url;

# Retrieve Date
&get_date;

# Parse Form Contents
&parse_form;

# Check Required Fields
&check_required;

# Check the Captcha is correct
if($captcha_enabled == 1) {
    &check_captcha;
}

# Send E-Mail
&send_mail;

# Return HTML Page or Redirect User
&return_html;

# This is only run if $captcha_enabled is set to 1.
# It checks that the captcha has been entered correctly,
# returning an error if not.
sub check_captcha {
    require Authen::Captcha;

    my $captcha = Authen::Captcha->new(
	data_folder => $captcha_datadir,
	output_folder => $captcha_outputdir,
	);

    my $submittedmd5sum = $Form{'captcha-md5sum'} || '';
    my $submittedtext = $Form{'captcha-text'} || '';

    if($captcha->check_code($submittedtext,$submittedmd5sum) != 1) {
	print STDERR "The error is being called from check_captcha error handling...\n";
	&error('bad_captcha');
    }
}


# NOTE rev1.91: This function is no longer intended to stop abuse, that      #
#    functionality is now embedded in the checks made on @recipients and the #
#    recipient form field.                                                   #

sub check_url {

    # Localize the check_referer flag which determines if user is valid.     #
    local($check_referer) = 0;

    # If a referring URL was specified, for each valid referer, make sure    #
    # that a valid referring URL was passed to FormMail.                     #

    if ($ENV{'HTTP_REFERER'}) {
        foreach $referer (@referers) {
            if ($ENV{'HTTP_REFERER'} =~m{
                  ^                  # Start of string
                  https?://          # HTTP or HTTPS
                  (?: [^\@]* \@ ) ?  # There could be a username
                  (?: [\w\.\-]* )    # Domain fragments
                  $referer          
                  (?: / | $ )        # End of (the domain part of) the URL.
            }ix) {
                $check_referer = 1;
                last;
            }
        }
    }
    else {
        if($stealth) {
	    print "Status: 404 Not Found\n\n";
	    exit;
        } else {
	    $check_referer = 1;
        }
    }

    # If the HTTP_REFERER was invalid, send back an error.                   #
    if ($check_referer != 1) { &error('bad_referer') }
}

sub get_date {

    # Define arrays for the day of the week and month of the year.           #
    @days   = ('Sunday','Monday','Tuesday','Wednesday',
               'Thursday','Friday','Saturday');
    @months = ('January','February','March','April','May','June','July',
               'August','September','October','November','December');

    # Get the current time and format the hour, minutes and seconds.  Add    #
    # 1900 to the year to get the full 4 digit year.                         #
    ($sec,$min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[0,1,2,3,4,5,6];
    $time = sprintf("%02d:%02d:%02d",$hour,$min,$sec);
    $year += 1900;

    # Format the date.                                                       #
    $date = "$days[$wday], $months[$mon] $mday, $year at $time";

}

sub parse_form {

    # Define the configuration associative array.                            #
    %Config = ('recipient','',          'subject','',
               'email','',              'realname','',
               'redirect','',           'bgcolor','',
               'background','',         'link_color','',
               'vlink_color','',        'text_color','',
               'alink_color','',        'title','',
               'sort','',               'print_config','',
               'required','',           'env_report','',
               'return_link_title','',  'return_link_url','',
               'print_blank_fields','', 'missing_fields_redirect','',
	       'lastname','');

    # Determine the form's REQUEST_METHOD (GET or POST) and split the form   #
    # fields up into their name-value pairs.  If the REQUEST_METHOD was      #
    # not GET or POST, send an error.                                        #
    if ($ENV{'REQUEST_METHOD'} eq 'GET') {
        # Split the name-value pairs
        @pairs = split(/&/, $ENV{'QUERY_STRING'});
    }
    elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
        # Get the input
        read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	
        # Split the name-value pairs
        @pairs = split(/&/, $buffer);
    }
    else {
        &error('request_method');
    }

    # For each name-value pair:                                              #
    foreach $pair (@pairs) {

        # Split the pair up into individual variables.                       #
        local($name, $value) = split(/=/, $pair);
	
        # Decode the form encoding on the name and value variables.          #
        # v1.92: remove null bytes                                           #
        $name =~ tr/+/ /;
        $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $name =~ tr/\0//d;

        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $value =~ tr/\0//d;

        # If the field name has been specified in the %Config array, it will #
        # return a 1 for defined($Config{$name}}) and we should associate    #
        # this value with the appropriate configuration variable.  If this   #
        # is not a configuration form field, put it into the associative     #
        # array %Form, appending the value with a ', ' if there is already a #
        # value present.  We also save the order of the form fields in the   #
        # @Field_Order array so we can use this order for the generic sort.  #
        if (defined($Config{$name})) {
            $Config{$name} = $value;
        }
        else {
            if ($Form{$name} ne '') {
                $Form{$name} = "$Form{$name}, $value";
            }
            else {
                push(@Field_Order,$name);
                $Form{$name} = $value;
            }
        }
    }

    # The next six lines remove any extra spaces or new lines from the       #
    # configuration variables, which may have been caused if your editor     #
    # wraps lines after a certain length or if you used spaces between field #
    # names or environment variables.                                        #
    $Config{'required'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'required'} =~ s/(\s+)?\n+(\s+)?//g;
    $Config{'env_report'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'env_report'} =~ s/(\s+)?\n+(\s+)?//g;
    $Config{'print_config'} =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
    $Config{'print_config'} =~ s/(\s+)?\n+(\s+)?//g;

    # Split the configuration variables into individual field names.         #
    @Required = split(/,/,$Config{'required'});
    @Env_Report = split(/,/,$Config{'env_report'});
    @Print_Config = split(/,/,$Config{'print_config'});

    # ACCESS CONTROL FIX: Only allow ENV variables in @valid_ENV in          #
    # @Env_Report for security reasons.                                      #
    foreach $env_item (@Env_Report) {
        foreach $valid_item (@valid_ENV) {
            if ( $env_item eq $valid_item ) { push(@temp_array, $env_item) }
        }
    } 
    @Env_Report = @temp_array;
}

sub check_required {

    # Localize the variables used in this subroutine.                        #
    local($require, @error);

    # The following insures that there were no newlines in any fields which  #
    # will be used in the header.                                            #
    if ($Config{'subject'} =~ /(\n|\r)/m || $Config{'email'} =~ /(\n|\r)/m ||
        $Config{'realname'} =~ /(\n|\r)/m || $Config{'lastname'} =~ /(\n|\r)/m || $Config{'recipient'} =~ /(\n|\r)/m) {
        &error('invalid_headers');
    }

    if (!$Config{'recipient'}) {
        if (!defined(%Form)) { print STDERR "There is no Form...?\n"; &error('bad_referer'); }
        else                 { &error('no_recipient') }
    }
    else {
        # This block of code requires that the recipient address end with    #
        # a valid domain or e-mail address as defined in @recipients.        #
        $valid_recipient = 0;
        foreach $send_to (split(/,/,$Config{'recipient'})) {
            foreach $recipient (@recipients) {
                if ($send_to =~ /^$recipient$/i) {
                    push(@send_to,$send_to); last;
                }
            }
        }
        if ($#send_to < 0) { &error('no_recipient') }
        $Config{'recipient'} = join(',',@send_to);
    }

    # For each require field defined in the form:                            #
    foreach $require (@Required) {

        # If the required field is the email field, the syntax of the email  #
        # address if checked to make sure it passes a valid syntax.          #
        if ($require eq 'email' && !&check_email($Config{$require})) {
            push(@error,$require);
        }

        # Otherwise, if the required field is a configuration field and it   #
        # has no value or has been filled in with a space, send an error.    #
        elsif (defined($Config{$require})) {
            if ($Config{$require} eq '') { push(@error,$require); }
        }

        # If it is a regular form field which has not been filled in or      #
        # filled in with a space, flag it as an error field.                 #
        elsif (!defined($Form{$require}) || $Form{$require} eq '') {
            push(@error,$require);
        }
    }

    # If any error fields have been found, send error message to the user.   #
    if (@error) { &error('missing_fields', @error) }
}

sub return_html {
    # Local variables used in this subroutine initialized.                   #
    local($key,$sort_order,$sorted_field);

    # Now that we have finished using form values for any e-mail related     #
    # reasons, we will convert all of the form fields and config values      #
    # to remove any cross-site scripting security holes.                     #
    local($field);
    foreach $field (keys %Config) {
        $safeConfig{$field} = &clean_html($Config{$field});
    }

    foreach $field (keys %Form) {
        $Form{$field} = &clean_html($Form{$field});
    }


    # If redirect option is used, print the redirectional location header.   #
    if ($Config{'redirect'}) {
        print "Location: $safeConfig{'redirect'}\n\n";
    }

    # Otherwise, begin printing the response page.                           #
    else {

        # Print HTTP header and opening HTML tags.                           #
        print "Content-type: text/html\n\n";
        print "<html>\n <head>\n";

        # Print out title of page                                            #
        if ($Config{'title'}) { print "<title>$safeConfig{'title'}</title>\n" }
        else                  { print "<title>Thank You</title>\n"        }

        print " </head>\n <body";

        # Get Body Tag Attributes                                            #
        &body_attributes;

        # Close Body Tag                                                     #
        print ">\n  <center>\n";

        # Print custom or generic title.                                     #
        if ($Config{'title'}) { print "<h1>$safeConfig{'title'}</h1>\n" }
        else { print "<h1>Thank You For Filling Out This Form</h1>\n" }

        print "</center>\n";

        print "Below is what you submitted to $safeConfig{'recipient'} on ";
        print "$date<p><hr size=1 width=75\%><p>\n";

        # If a sort order is specified, sort the form fields based on that.  #
        if ($Config{'sort'} =~ /^order:.*,.*/) {

            # Set the temporary $sort_order variable to the sorting order,   #
            # remove extraneous line breaks and spaces, remove the order:    #
            # directive and split the sort fields into an array.             #
            $sort_order = $Config{'sort'};
            $sort_order =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
            $sort_order =~ s/(\s+)?\n+(\s+)?//g;
            $sort_order =~ s/order://;
            @sorted_fields = split(/,/, $sort_order);

            # For each sorted field, if it has a value or the print blank    #
            # fields option is turned on print the form field and value.     #
            foreach $sorted_field (@sorted_fields) {
                local $sfname = &clean_html($sorted_field);

                if ($Config{'print_blank_fields'} || $Form{$sorted_field} ne '') {
                    print "<b>$sfname:</b> $Form{$sorted_field}<p>\n";
                }
            }
        }

        # Otherwise, use the order the fields were sent, or alphabetic.      #
        else {

            # Sort alphabetically if requested.
            if ($Config{'sort'} eq 'alphabetic') {
                @Field_Order = sort @Field_Order;
            }

            # For each form field, if it has a value or the print blank      #
            # fields option is turned on print the form field and value.     #
            foreach $field (@Field_Order) {
                local $fname = &clean_html($field);

                if ($Config{'print_blank_fields'} || $Form{$field} ne '') {
                    print "<b>$fname:</b> $Form{$field}<p>\n";
                }
            }
        }

        print "<p><hr size=1 width=75%><p>\n";

        # Check for a Return Link and print one if found.                    #
        if ($Config{'return_link_url'} && $Config{'return_link_title'}) {
            print "<ul>\n";
            print "<li><a href=\"$safeConfig{'return_link_url'}\">$safeConfig{'return_link_title'}</a>\n";
            print "</ul>\n";
        }

        # Print the page footer.                                             #
        print <<"(END HTML FOOTER)";
        <hr size=1 width=75%><p> 
	    <center><font size=-1><a href="http://www.scriptarchive.com/formmail.html">FormMail</a> V1.92 &copy; 1995 - 2002  Matt Wright<br>
	    A Free Product of <a href="http://www.scriptarchive.com/">Matt's Script Archive, Inc.</a></font></center>
        </body>
       </html>
(END HTML FOOTER)
}
}

sub send_mail {
    # Localize variables used in this subroutine.                            #
    local($print_config,$key,$sort_order,$sorted_field,$env_report);

    # Open The Mail Program
    open(MAIL,"|$mailprog 1>&2");

    print MAIL "To: $Config{'recipient'}\n";
    print MAIL "From: \"$Config{'realname'}\" \"$Config{'lastname'}\" <$Config{'email'}>\n";

    # Check for Message Subject
    if ($Config{'subject'}) { print MAIL "Subject: $Config{'subject'}\n\n" }
    else                    { print MAIL "Subject: Communication from visitor to website sysformatics.com\n\n" }

    print MAIL "Below is the result of your feedback form.  It was submitted by\n";
    print MAIL "$Config{'realname'} $Config{'lastname'} ($Config{'email'}) on $date\n";
    print MAIL "-" x 75 . "\n\n";

    if (@Print_Config) {
        foreach $print_config (@Print_Config) {
            if ($Config{$print_config}) {
                print MAIL "$print_config: $Config{$print_config}\n\n";
            }
        }
    }

    # If a sort order is specified, sort the form fields based on that.      #
    if ($Config{'sort'} =~ /^order:.*,.*/) {

        # Remove extraneous line breaks and spaces, remove the order:        #
        # directive and split the sort fields into an array.                 #
        local $sort_order = $Config{'sort'};
        $sort_order =~ s/(\s+|\n)?,(\s+|\n)?/,/g;
        $sort_order =~ s/(\s+)?\n+(\s+)?//g;
        $sort_order =~ s/order://;
        @sorted_fields = split(/,/, $sort_order);

        # For each sorted field, if it has a value or the print blank        #
        # fields option is turned on print the form field and value.         #
        foreach $sorted_field (@sorted_fields) {
            if ($Config{'print_blank_fields'} || $Form{$sorted_field} ne '') {
                print MAIL "$sorted_field: $Form{$sorted_field}\n\n";
            }
        }
    }

    # Otherwise, print fields in order they were sent or alphabetically.     #
    else {

        # Sort alphabetically if specified:                                  #
        if ($Config{'sort'} eq 'alphabetic') {
            @Field_Order = sort @Field_Order;
        }

        # For each form field, if it has a value or the print blank          #
        # fields option is turned on print the form field and value.         #
        foreach $field (@Field_Order) {
            if ($Config{'print_blank_fields'} || $Form{$field} ne '') {
                print MAIL "$field: $Form{$field}\n\n";
            }
        }
    }

    print MAIL "-" x 75 . "\n\n";

    # Send any specified Environment Variables to recipient.                 #
    foreach $env_report (@Env_Report) {
        if ($ENV{$env_report}) {
            print MAIL "$env_report: $ENV{$env_report}\n";
        }
    }

    close (MAIL);
}

sub check_email {
    # Initialize local email variable with input to subroutine.              #
    $email = $_[0];

    # If the e-mail address contains:                                        #
    if ($email =~ /(@.*@)|(\.\.)|(@\.)|(\.@)|(^\.)/ ||

        # the e-mail address contains an invalid syntax.  Or, if the         #
        # syntax does not match the following regular expression pattern     #
        # it fails basic syntax verification.                                #

        $email !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z0-9]+)(\]?)$/) {

        # Basic syntax requires:  one or more characters before the @ sign,  #
        # followed by an optional '[', then any number of letters, numbers,  #
        # dashes or periods (valid domain/IP characters) ending in a period  #
        # and then 2 or 3 letters (for domain suffixes) or 1 to 3 numbers    #
        # (for IP addresses).  An ending bracket is also allowed as it is    #
        # valid syntax to have an email address like: user@[255.255.255.0]   #

        # Return a false value, since the e-mail address did not pass valid  #
        # syntax.                                                            #
        return 0;
    }

    else {

        # Return a true value, e-mail verification passed.                   #
        return 1;
    }
}

# This was added into v1.91 to further secure the recipients array.  Now, by #
# default it will assume that valid recipients include only users with       #
# usernames A-Z, a-z, 0-9, _ and - that match your domain exactly.  If this  #
# is not what you want, you should read more detailed instructions regarding #
# the configuration of the @recipients variable in the documentation.        #
sub fill_recipients {
    local(@domains) = @_;
    local($domain,@return_recips);

    foreach $domain (@domains) {
        if ($domain =~ /^\d+\.\d+\.\d+\.\d+$/) {
            push(@return_recips,'[\w\-\.]+\@\[' . "\Q$domain\E" . '\]');
        }
        else {
            push(@return_recips,'[\w\-\.]+\@'."\Q$domain\E");
        }
    }

    return @return_recips;
}

# This function will convert <, >, & and " to their HTML equivalents.        #
sub clean_html {
    local $value = $_[0];
    $value =~ s/\&/\&amp;/g;
    $value =~ s/</\&lt;/g;
    $value =~ s/>/\&gt;/g;
    $value =~ s/"/\&quot;/g;
    return $value;
}

sub body_attributes {
    # Check for Background Color
    if ($Config{'bgcolor'}) { print " bgcolor=\"$safeConfig{'bgcolor'}\"" }

    # Check for Background Image
    if ($Config{'background'}) { print " background=\"$safeConfig{'background'}\"" }

    # Check for Link Color
    if ($Config{'link_color'}) { print " link=\"$safeConfig{'link_color'}\"" }

    # Check for Visited Link Color
    if ($Config{'vlink_color'}) { print " vlink=\"$safeConfig{'vlink_color'}\"" }

    # Check for Active Link Color
    if ($Config{'alink_color'}) { print " alink=\"$safeConfig{'alink_color'}\"" }

    # Check for Body Text Color
    if ($Config{'text_color'}) { print " text=\"$safeConfig{'text_color'}\"" }
}

sub error { 
    # Localize variables and assign subroutine input.                        #
    local($error,@error_fields) = @_;
    local($host,$missing_field,$missing_field_list);
	
    # Local variables for html layout
    local($layout_1,$layout_cd,$layout_fs,$layout_fe,$layout_2);
    
    $layout_1 = '
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
	
	
	<style type="text/css">  
      @media (min-width: 767px) {
      .thumbnail-fix {min-height:560px;}
      }
      @media (min-width: 992px) {
      .thumbnail-fix {min-height:537px;}
      }

    </style>
	
	<!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" href="../../assets/ico/apple-touch-icon.png">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">
	
	<!-- Google Analytics BEGIN -->
    <script type="text/javascript">';
    
    $layout_1 .= "
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-35786145-1']);
      _gaq.push(['_trackPageview']);

      (function() {
      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
      ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script><!-- Google Analytics END -->
	
	</head>";
    
    $layout_1 .= '
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
      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href=';

$layout_1 .= "
'../store/store.html'";

$layout_1 .= '
">
     <img src="../../assets/img/sysstore-logo.png" height="29"></img>
      </button>
      
      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href=';

$layout_1 .= "
'../contact/fm-contact-us.cgi'";

$layout_1 .= '
">
      <span class="glyphicon glyphicon-comment"></span>
      </button>
      
      <button type="button" class="navbar-toggle navbar-toggle-pos" onclick="window.location.href=';

$layout_1 .= "
'../support/support.html'";

$layout_1 .= '
">
      <span class="glyphicon glyphicon-asterisk"></span>
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
      <li><a class="dropdown-item-adj" href="../services/it-support/it-support.html">IT Support Services</a></li>
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
	  <h2 class="margin-fix">Contact Sysformatics</h2>
	<div class="row">';

    $layout_cd = '
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
		</div>';

    $layout_fs = '
		<div class="col-lg-8 col-sm-8">
			<div class="thumbnail thumbnail-fix">
				<div class="caption">
<h3 class="h3-fix">Feedback</h3>';

    $layout_fe = '
</div>
			</div>
		</div>';

    $layout_2 = '	
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

    <script>
      // Accordion dropdown menu
      jQuery(function() {
      jQuery( ".topnav" ).accordion({active: "a.default",alwaysOpen: true,autoHeight:false,clearStyle: true,collapsible: true});
      });
      
      //capture the click on the a tag
      jQuery(".topnav  .header-link a").click(function() {
      window.location = jQuery(this).attr("href");
      return false;
      });
    </script>

	<!-- AddThis Smart Layers BEGIN -->
    <!-- Go to http://www.addthis.com/get/smart-layers to customize -->
    <script type="text/javascript" src="//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-520259f274c70552"></script>
    <script type="text/javascript">';

    $layout_2 .= "
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
    </script><!-- AddThis Smart Layers END -->";
    
    $layout_2 .= '
	 <!-- Google Analytics BEGIN -->
    <script type="text/javascript">';

    
    $layout_2 .= "
var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-35786145-1']);
      _gaq.push(['_trackPageview']);

      (function() {
      var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
      ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
      var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();

    </script><!-- Google Analytics END -->";	
    
    
    if ($error eq 'bad_referer') {
        if ($ENV{'HTTP_REFERER'} =~ m|^https?://([\w\.]+)|i) {
            $host = $1;
            my $referer = &clean_html($ENV{'HTTP_REFERER'});
            print <<"(END ERROR HTML)";
Content-type: text/html
<!DOCTYPE html>
<html lang="en">
$layout_1
	<div class="hidden-sm">
	$layout_cd
	</div>
	$layout_fs
	<h3 class="h3-fix">Bad Referrer - Access Denied</h3>
   </table>
   <table border=0 width=600 bgcolor=#CFCFCF>
    <h4 class="text-info">The form attempting to use
     <a href="http://www.scriptarchive.com/formmail.html">FormMail</a>
     resides at <tt>$referer</tt>, which is not allowed to access
     this cgi script.

     If you are attempting to configure FormMail to run with this form, you need
     to add the following to \@referers, explained in detail in the 
     <a href="http://www.scriptarchive.com/readme/formmail.html">README</a> file.</h4>

     Add <tt>'$host'</tt> to your <tt><b>\@referers</b></tt> array.<hr size=1><br>
     <input Type="button" class="btn btn-info" VALUE="&larr; Go back" onClick="history.go(-1);return true;">
	$layout_fe
	<div class="visible-sm">
	$layout_cd
	</div>
	$layout_2
 </body>
</html>
(END ERROR HTML)
        }
        else {
            
			print "Location: fm-contact-us.cgi\n\n";
        }
    }

    elsif ($error eq 'request_method') {
            print <<"(END ERROR HTML)";
Content-type: text/html
<!DOCTYPE html>
<html lang="en">
	$layout_1
	<div class="hidden-sm">
	$layout_cd
	</div>
	$layout_fs
	<h3 class="h3-fix">Error: Request Method</h3>
    <h4 class="text-info">The Request Method of the Form you submitted did not match
     either <tt>GET</tt> or <tt>POST</tt>.  Please check the form and make sure the
     <tt>method=</tt> statement is in upper case and matches <tt>GET</tt> or <tt>POST</tt>.</h4><br>
     <input Type="button" class="btn btn-info" VALUE="&larr; Go back" onClick="history.go(-1);return true;">
     $layout_fe
	<div class="visible-sm">
	$layout_cd
	</div>
	$layout_2
 </body>
</html>
(END ERROR HTML)
    }

    elsif($error eq 'bad_captcha') {
      print <<"(END ERROR HTML)";
Content-type: text/html

    <!DOCTYPE html>
<html lang="en">
	$layout_1
	<div class="hidden-sm">
	$layout_cd
	</div>
	$layout_fs
	<h3 class="text-danger">Bad image verification code</h3>
	<h4 class="text-info">The entered image verification code was incorrect, please try again.</h4><br>
	<input Type="button" class="btn btn-info" VALUE="&larr; Go back" onClick="history.go(-1);return true;">
    $layout_fe
	<div class="visible-sm">
	$layout_cd
	</div>
	$layout_2
 </body>
</html>
(END ERROR HTML)
    }

    elsif ($error eq 'no_recipient') {
            print <<"(END ERROR HTML)";
Content-type: text/html
<!DOCTYPE html>
<html lang="en">
    $layout_1
	<div class="hidden-sm">
	$layout_cd
	</div>
	$layout_fs
    <h3 class="text-danger">Error: Bad/No Recipient</h3>
    <h4 class="text-info">There was no recipient or an invalid recipient specified in the data sent to FormMail.  Please
     make sure you have filled in the <tt>recipient</tt> form field with an e-mail
     address that has been configured in <tt>\@recipients</tt>.</h4><br>
	<input Type="button" class="btn btn-info" VALUE="&larr; Go back" onClick="history.go(-1);return true;">
    $layout_fe
	<div class="visible-sm">
	$layout_cd
	</div>
	$layout_2
 </body>
</html>
(END ERROR HTML)
    }

    elsif ($error eq 'invalid_headers') {
            print <<"(END ERROR HTML)";
Content-type: text/html

     <!DOCTYPE html>
<html lang="en">
	$layout_1
	<div class="hidden-sm">
	$layout_cd
	</div>
	$layout_fs
	<h3 class="text-danger">Bad Header Fields</h3>
    <h4 class="text-info">The header fields, which include <tt>recipient</tt>, <tt>email</tt>, <tt>realname</tt>, <tt>lastname</tt>, <tt>telephone</tt> and <tt>subject</tt> were
     filled in with invalid values. You may not include any newline characters in these parameters.<br>
	Please return to the feedback form and try again.</h4><br>
	<input Type="button" class="btn btn-info" VALUE="&larr; Go back" onClick="history.go(-1);return true;">
    $layout_fe
	<div class="visible-sm">
	$layout_cd
	</div>
	$layout_2
 </body>
</html>
(END ERROR HTML)
    }

    elsif ($error eq 'missing_fields') {
        if ($Config{'missing_fields_redirect'}) {
            print "Location: " . &clean_html($Config{'missing_fields_redirect'}) . "\n\n";
        }
        else {
            foreach $missing_field (@error_fields) {
                $missing_field_list .= "<li>" . &clean_html($missing_field) . "\n";
            }

            print <<"(END ERROR HTML)";
Content-type: text/html

<!DOCTYPE html>
<html lang="en">
	$layout_1
	<div class="hidden-sm">
	$layout_cd
	</div>
	$layout_fs
	<h3 class="text-danger">Error: Blank Fields</h3>
	<h4 class="text-info">The following fields were left blank in your submission form:</h4>
	<h4 class="text-info"><ul>$missing_field_list</ul>
	<h4 class="text-info">These fields must be filled in before you can successfully submit the form.<br>
	 Please return to the feedback form and try again.</h4><br>
	<input Type="button" class="btn btn-info" VALUE="&larr; Go back" onClick="history.go(-1);return true;">
	$layout_fe
	<div class="visible-sm">
	$layout_cd
	</div>
	$layout_2	
 </body>
</html>
(END ERROR HTML)
        }
    }

    exit;
}
