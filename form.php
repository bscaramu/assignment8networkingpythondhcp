<!DOCTYPE html>
<html>
<head>
    <title>Request IP Address</title>
</head>
<body>
    <h1>Request IP Address!</h1>
    <form method="POST" action="process.php">
        <label for="mac">MAC Address:</label>
        <input type="text" name="mac" required><br><br>

        <label for="version">DHCP Version:</label>
        <select name="version" required>
            <option value="DHCPv4">DHCPv4</option>
            <option value="DHCPv6">DHCPv6</option>
        </select><br><br>

        <input type="submit" value="Request IP">
    </form>
</body>
</html>
