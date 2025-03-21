<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mac = escapeshellarg($_POST["mac"]);
    $version = escapeshellarg($_POST["version"]);

    $command = "python3 network_config.py $mac $version";
    $output = shell_exec($command);

    if ($output === null) {
        echo "Error executing Python script.";
    } else {
        $data = json_decode($output, true);
        echo "<h2>Assigned IP Information</h2>";
        echo "<pre>";
        print_r($data);
        echo "</pre>";
    }
}
?>
