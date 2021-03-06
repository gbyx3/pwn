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

## Upgrading shell
Ctrl + z, `stty raw -echo` `fg` enter, enter
```
script /dev/null -c bash
```
```
python3 -c 'import pty;pty.spawn("/bin/bash")'
```
