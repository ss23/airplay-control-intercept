<?php

require_once __DIR__ . '/vendor/autoload.php';

$name = false;
if (file_exists('/tmp/playing.txt')) {
	$file = file_get_contents('/tmp/playing.txt');
	// It's an IP address of the currently playing user
	switch ($file) {
		case 'fe80::3e07:54ff:fe5a:7f6d':
			$name = 'Igor';
			break;
		case '192.168.2.126':
			$name = 'Stephen';
			break;
		case '':
			$name = false;
			break;
		default:
			$name = 'Unknown';
	}
}

if ($name === false) {
	$playing = "Speakers not in use";
} else if ($name == 'Unknown') {
	$playing = "Currently playing: Unknown (let Stephen know who it is!)";
} else {
	$playing = "Currently playing: $name";
}

$loader = new Twig_Loader_Filesystem('templates');
$twig = new Twig_Environment($loader, array(
	'cache' => '/tmp/twigcache',
));

echo $twig->render('index.html', array(
	'title' => 'Airplay Control - Fargesia',
	'playing' => $playing,
));

