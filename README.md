# pwn
Cheat sheet

## Discovery
### Port scanning
```
ip="10.0.0.1" && for i in {20..25}; do echo > /dev/tcp/$ip/$i ; if [ $? -eq 0 ]; then echo -e "Port: \e[4m$i\e[0m is Open on host: $ip" ; fi ; done 2>/dev/null
```

### Traceroute
```
# Without latency
h="google.se" && for i in {1..255}; do ping -t $i $h -c1 -n | grep From ; if [ $? -ne 0 ] ; then break ; fi ; done

# With latency (sends an additional package per hop)
h="google.se" && for ip in $(for i in {1..255}; do ping -t $i $h -c1 -n | grep From | awk '{print $2}'; if [ ${PIPESTATUS[1]} -ne 0 ] ; then break ; fi ; done) ; do ping -c1 $ip | grep from ; done
```

### LDAP
```
LDAPTLS_REQCERT=never ldapsearch -o ldif-wrap=no -D <USER>@<NETBIOS> -W -H ldap://<AD.DOMAIN.TLD> -b "dc=ad,dc=<DOMAIN>,dc=<TLD>" -s sub -x -ZZ "(&(objectClass=user)(sAMAccountName=<sAM>))"
```

## Shodan
```
jq -r 'select(.domains | any(. == "domain.tld")) | {domains, ip_str, product, port, number_vulns: (.vulns | length)}' data.json | jq -s 'sort_by(.port)'
```

## Self signed cert
```
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -sha256 -days 365 -subj "/C=US/ST=CA/O=MyOrg" -passout "pass:$(pwgen -N1 96 | tee ssl/pass.txt)"
```

## HTTPS Server
```
import http.server
import ssl

lhost = "0.0.0.0"
lport = 443
server_address = (lhost, lport)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile="ssl/cert.pem", keyfile="ssl/key.pem", ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()
```

## GROK
```
# Parse Linux Sysmon XML (Tested with, Task:1,3,4,5,9)
<Event><System><Provider Name=%{QUOTEDSTRING:ProviderName} Guid="\{%{UUID:Guid}\}"/><EventID>%{INT:EventId}</EventID><Version>%{INT:Version}</Version><Level>%{INT:Level}</Level><Task>%{INT:Task}</Task><Opcode>%{INT:Opcode}</Opcode><Keywords>%{BASE16NUM:Keywords}</Keywords><TimeCreated SystemTime="%{TIMESTAMP_ISO8601:timestamp}"/><EventRecordID>%{INT:EventRecordID}</EventRecordID><Correlation/><Execution ProcessID="%{INT:ProcessId}" ThreadID="%{INT:ThreadId}"/><Channel>%{DATA:Channel}</Channel><Computer>%{DATA:Computer}</Computer><Security UserId="%{INT:UserId}"/></System><EventData>(?:<Data Name="RuleName">%{DATA:RuleName}</Data>)?<Data Name="UtcTime">%{TIMESTAMP_ISO8601:EventTimestamp}</Data>(?:<Data Name="ProcessGuid">\{%{UUID:ProcessGuid}\}</Data>)?(?:<Data Name="ProcessId">%{INT:EventProcessId}</Data>)?(?:<Data Name="Image">%{DATA:EventImage}</Data>)?(?:<Data Name="FileVersion">%{DATA:EventFileVersion}</Data>)?(?:<Data Name="Description">%{DATA:EventDescription}</Data>)?(?:<Data Name="Product">%{DATA:EventProduct}</Data>)?(?:<Data Name="Company">%{DATA:EventCompany}</Data>)?(?:<Data Name="OriginalFileName">%{DATA:EventOriginalFileName}</Data>)?(?:<Data Name="CommandLine">%{DATA:EventCmdLine}</Data>)?(?:<Data Name="CurrentDirectory">%{DATA:EventCurrentDirectory}</Data>)?(?:<Data Name="User">%{DATA:EventUser}</Data>)?(?:<Data Name="LogonGuid">\{%{UUID:EventLogonGuid}\}</Data>)?(?:<Data Name="LogonId">%{INT:EventLogonId}</Data>)?(?:<Data Name="TerminalSessionId">%{INT:EventTerminalSessionId}</Data>)?(?:<Data Name="IntegrityLevel">%{DATA:EventIntegrityLevel}</Data>)?(?:<Data Name="Hashes">%{DATA:EventHashes}</Data>)?(?:<Data Name="ParentProcessGuid">\{%{UUID:EventParentProcessGuid}\}</Data>)?(?:<Data Name="ParentProcessId">%{INT:EventParentProcessId}</Data>)?(?:<Data Name="ParentImage">%{DATA:EventParentImage}</Data>)?(?:<Data Name="ParentCommandLine">%{DATA:EventParentCommandLine}</Data>)?(?:<Data Name="ParentUser">%{DATA:EventParentUser}</Data>)?</EventData></Event>
```

## OSINT
### Get Linkedin users
```
# https://www.linkedin.com/company/<corp>/people/
var users = document.getElementsByClassName("org-people-profile-card__profile-title");
Array.from(users).forEach(function(user) {
  console.log(user.innerText);
});
```

## Upgrading shell
Ctrl + z, `stty raw -echo` `fg` enter, enter
```
script /dev/null -c bash
```
```
python3 -c 'import pty;pty.spawn("/bin/bash")'
```
