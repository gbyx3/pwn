# pwn
Cheat sheet
## Port scanning
```
ip="10.0.0.1" && for i in {20..25}; do echo > /dev/tcp/$ip/$i ; if [ $? -eq 0 ]; then echo -e "Port: \e[4m$i\e[0m is Open on host: $ip" ; fi ; done 2>/dev/null
```