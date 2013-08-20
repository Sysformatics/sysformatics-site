#!/usr/bin/perl
use strict;
use warnings;
use Authen::Captcha;

# You MUST create the following directories yourself. FormMail will not work
# without them, unless you are not using Captcha support.

# Set this to a directory that is not accessible via the web.
# Often something like /home/yourname/.captcha_data
my $captcha_datadir = "/websites/123reg/LinuxPackage25/sy/sf/or/sysformatics.com/public_html/.captcha_data";

# Set this to a directory that will store the captcha images. This should
# be accessible via the web because it will be included on the page.
# Often something like /home/yourname/public_html/fm/captcha_img
my $captcha_outputdir = "/websites/123reg/LinuxPackage22/sy/sf/or/sysformatics.com/public_html/sys/en/contact/img";

# This should be the same as the directory above, but using the web accessible
# URL path. If you have /home/yourname/public_html/fm/captcha_img above then
# you will need /fm/captcha_img here.
my $image_dir = "/sys/en/contact/img";


# Use the following few settings to configure the form values.

# This should be the location of the FormMail.cgi script.
my $formmail = "/sys/en/contact/FormMail.cgi";

# This is where you want the email to go.
my $recipient = 'sales@sysformatics.com';

# This is where the user should be taken to after submitting the form.
my $redirect = "http://sysformatics.com";


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


# Modify the HTML below to make your form how you like it.
# Ensure that you read the instructions carefully.
# Do not edit outside the comment sections, unless you are sure
# you know what you're doing.
print <<"END";
Content-Type: text/html; charset=ISO-8859-1

<html>
  <head>
    <title>FormMail Instructions</title>
  </head>
  <body style="width: 600px;">
    <h1>FormMail Instructions</h1>
    <p><strong>Your installation is complete.</strong>

      <p>Note: 
        <ol>
          <li>FormMail has been installed here to send mail only from pages on this domain, <strong>sysformatics.com</strong> to $recipient.</li>
          <li>For this basic configuration you do not have to make any changes to FormMail.cgi
          <li>For more advanced configuration possibilities see the  online FormMail
          <a href="http://www.scriptarchive.com/readme/formmail.html">README</a> file.</li>
          <li>If you fill this form in correctly and click
                'Submit' a new file will be created called '/sys/en/contact/fm-contact-us.cgi'.  It is
                an executable CGI script that will display a contact form inviting the user to email a message to you. 
                Your actual email address will be hidden and is stored
                in a way that will make it hard for robotic email address mining robots to detect.<br />
                To use the form all you have to do is insert the following html into one of your web pages <br /><br />
                "&lt;a href=&quot;/sys/en/contact/fm-contact-us.cgi&quot;&gt;Contact us&lt;/a&gt;"<br /><br />
                This information is repeated in '/sys/en/contact/help/README-simple.html'.
        </li>

        </ol>
      </p>
    </p>

    <form action="$formmail" method="post">
      <table>
        <tr>
          <td>
            <input type="hidden" name="subject" value="This is a test" />

            <!-- This section must remain the same for Captcha support. -->
            <input type="hidden" name="recipient" value="$recipient" />
            <input type="hidden" name="redirect" value="$redirect" />
            <input type="hidden" name="captcha-md5sum" value="$md5sum" />
            <label>Email Address: </label>
          </td><td>
            <input type="text" size="20" name="email">
          </td>
        </tr><tr>
          <td>
            <label>Name: </label>
          </td><td>
            <input type="text" size="20" name="realname">
          </td>
        </tr>
        <!-- End section -->

        <!-- You can add extra form items here -->
          <td style="vertical-align: top;">
            <label>Message: </label>
          </td><td>
            <textarea name="message" style="height: 120px; width: 300px;"></textarea>
          </td>
        </tr><tr>

        <!-- The following section must stay here for Captcha support. -->
          <td colspan="2">Please enter the image verification code below.</td>
        </tr><tr>
          <td><img src="$image_dir/$md5sum.png" /></td>
          <td>
            <input type="text" size="20" name="captcha-text" id="captcha-text" />
          </td>
        </tr>
        <!-- End section -->

        <tr>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
        </tr>

        <tr>
          <td>
            <input value="Submit Comments" type="submit" />
          </td><td>
            <input value="Clear Form" type="reset" />
          </td>
        </tr>
      </table>
    </form>

    <p>Try filling in the form above to send a test message if you like. You may need to change the email address in the settings first.<br /><br />
    You can make changes to this form or simply use it as a template by downloading this index.cgi from where you installed it and following through the comments.<br /><br />
    It will have to be a CGI file rather than an HTML file to include support for the image validation.
    </p>
  </body>
</html>
END
