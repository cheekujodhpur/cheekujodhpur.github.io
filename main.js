var about = "I'm an Engineering Physics fresher at <a href = 'http://iitb.ac.in'>Indian Institute of Technology, Bombay</a><br /><br />I love to cook, travel, socialize and tap into physical sciences. My mood is usually a superposition of psychopath, mad hatter, party animal and curious being and may collapse into any of these when you meet me. The professional, less useful information can be seen on my <a href = 'cv.pdf'>CV</a>";

var contact = 'B/607, Hostel 15<br />IIT Powai<br />Mumbai,Maharashtra,India<br />400067<br /><hr />Ph: +919468854691<br /><a href = "mailto:cheekujodhpur@gmail.com">cheekujodhpur@gmail.com</a><br /><a href = "http://www.facebook.com/cheekujodhpur">Facebook</a><br /><a href = "http://www.twitter.com/kumarayush4ever">Twitter</a><br />Skype: cheekujodhpur<br />';

var projects = '<h3>Web</h3><ul style = "list-style:none;"><li><a href = "http://www.grandimagazzinibomboniere.it" target = "_blank">Grandi Magazzini</a> (e-commerce)</li><li><a href = "http://www.gruppoleopardo.com" target = "_blank">Gruppo Leopardo s.r.l.</a> (e-commerce)</li></ul>';
projects += '<h3>Astronomy and Astrophysics</h3><ul style = "list-style:none;"><li>Estimating Photometric Redshift using Machine Learning Techniques<br /><b>Prof. Sajeeth Philip</b> (<i>NIUS Astronomy 2012</i>)</li><br /><br /><li>RXTE Studies: PCA Spectral Analysis for Spectral States in 4U 1630-47<br /><b>Prof. Manojendu Choudhary</b> (<i>NIUS Astronomy 2013</i>)</li></ul>';
projects += '<h3>Hobby</h3><ul style = "list-style:none;"><li>Melting a Chewing Gum <a href = "blog/melting-chewing-gum.html">>></a><br /><i>Auust 2014</i></li><br /><li>Validating Cosmological Principle <a href = "blog/cosmological-validation.html">>></a><br /><i>August 2014</i></li><br /><li>The King under the Elevator <a href = "blog/king-under-elevator.html">>></a><br /><i>August 2014</i></li><br /><li>Milky Cool <a href = "blog/milky-cool.html">>></a><br /><i>October 2014</i><font style = "color:red"> ongoing</font></li><br /></ul>';

var resources = 'The following are hobby projects/articles which could be useful to you:<br /><ul style = "list-style:none"><li>Problems in Group Theory <a href = "blog/gruppentheorie.html">>></a></li><br /><li>[Comments] Chasing Venus: A Race to Measure the Heavens <a href = "blog/chasingvenus.html">>></a></li></ul>';

var personal = '<ul style = "list-style:none;"><li>7<sup>th</sup> IOAA <a href = "blog/volos-chapter0.html">>></a><br /><i>July 2013</li><br /><li>Doing good <a href = "blog/doing-good.html">>></a><br /><i>24 September 2014</i></li><br /><li>Learning German <a href = "blog/german.html">>></a><br /><i>14 October 2014</i></li><br /><li>Of Peace and Ducks <a href = "blog/peace.html">>></a><br /><i>December 2014</i></li><br /><li>Dialogues <a href = "blog/dialogues.html">>></a><br /><i>March 2015</i></li><br />';

function show(x)
{
	$("#details").animate(
	{
	left:"5000px"
	},
	{
	complete:function(){
	$(this).html(x)
	}}).animate(
	{
	left:"600px"
	}
	)
}
