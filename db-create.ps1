# The SubscriptionId in which to create these objects
$SubscriptionId = '336a550b-1717-4786-8d39-13201277c1f4' # Look for ID in Azure Portal > Cost Management

# Generate the resource group name and set the location for your server
$resourceGroupName = "myResourceGroup-$(Get-Random)"
$location='polandcentral'

# Set an admin login and password for your server
$adminSqlLogin = "MateuszMajczyna2000There"  # use name + random number
$password = "WhooptyDoo2000!!!"    # use long (> 14 characters) and complicated password

# Generate server name - the logical server name has to be unique in the system
$serverName = "server-$(Get-Random)"

# The sample database name
$databaseName = "MediaDB"

# The ip address range that you want to allow to access your server
$startIp = "0.0.0.0"
$endIp = "255.255.255.255" # the Internet - all IPs

# Set subscription 
Set-AzContext -SubscriptionId $subscriptionId 

# Create a resource group
$resourceGroup = New-AzResourceGroup -Name $resourceGroupName -Location $location

# Create a server with a system wide unique server name
$server = New-AzSqlServer -ResourceGroupName $resourceGroupName `
    -ServerName $serverName `
    -Location $location `
    -SqlAdministratorCredentials $(New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $adminSqlLogin, $(ConvertTo-SecureString -String $password -AsPlainText -Force))

# Create a server firewall rule that allows access from the specified IP range
$serverFirewallRule = New-AzSqlServerFirewallRule -ResourceGroupName $resourceGroupName `
    -ServerName $serverName `
    -FirewallRuleName "AllowedIPs" -StartIpAddress $startIp -EndIpAddress $endIp

# Create a blank database with an S0 performance level
$database = New-AzSqlDatabase  -ResourceGroupName $resourceGroupName `
    -ServerName $serverName `
    -DatabaseName $databaseName `
    -RequestedServiceObjectiveName "S0" `
    -SampleName "AdventureWorksLT"


Write-Host "To remove database use command: Remove-AzResourceGroup -ResourceGroupName $resourceGroupName "