package main
import (
	"fmt"
	"bufio"
	"os"
	"log"
	"encoding/json"
	"strconv"
)

type Behavior struct {
	Package		    string	    `json:"package"`
        OutboundConnections []Connection    `json:"connections"`
        DNSLookups          []DNSLookup     `json:"dns"`
        FileOperations      []FileOperation `json:"files"`
        Commands            []string        `json:"commands"`
}

type DNSLookup struct {
        Name        string   `json:"name"`
        IPAddresses []string `json:"addresses"`
}

type Connection struct {
        Protocol  string `json:"protocol"`
        IPAddress string `json:"address"`
        Port      string `json:"port"`
}

type FileOperation struct {
        Operation string `json:"mode"`
        Filename  string `json:"filename"`
        Flag      string `json:"flag"`
}

func main() {
	file,err := os.Open(os.Args[1])
	if err != nil {
     	   panic(err)
    	}
	defer file.Close()

	behavior := Behavior{}
	scanner := bufio.NewScanner(file)

	cache := map[string]map[string]bool{
		"commands":    {},
		"files":       {},
		"connections": {},
	}
	for scanner.Scan() {
		syscall := make(map[string]interface{})
		entry := scanner.Bytes()
		err := json.Unmarshal(entry, &syscall)
		if err != nil {
			log.Printf("error unmarshaling entry: %s: %v", entry, err)
			continue
		}
		if syscall == nil {
			continue
		}
		//log.Println(syscall)
		switch syscall["evt.type"] {
		case "execve", "execveat":
			command := syscall["proc.exeline"].(string)
			if _, ok := cache["commands"][command]; ok {
				break
			}
			behavior.Commands = append(behavior.Commands, command)
			cache["commands"][command] = true
		case "open":
			if syscall["fd.name"] == nil {
				break
			}
			filename := syscall["fd.name"].(string)
			if filename == "" {
				break
			}
			if _, ok := cache["files"][filename]; ok {
				break
			}
			flag := ""
			if syscall["evt.arg.flags"] != nil {
				flag = syscall["evt.arg.flags"].(string)
			}
			behavior.FileOperations = append(behavior.FileOperations, FileOperation{
				Filename: filename,
				Flag:     flag,
			})
			cache["files"][filename] = true
		case "connect":
			if syscall["fd.sip"] == nil || syscall["fd.sport"] == nil {
				break
			}
			sip := syscall["fd.sip"].(string)
			port := strconv.Itoa(int(syscall["fd.sport"].(float64)))
			cacheID := fmt.Sprintf("%s:%s", sip, port)
			if _, ok := cache["connections"][cacheID]; ok {
				break
			}
			behavior.OutboundConnections = append(behavior.OutboundConnections, Connection{
				IPAddress: sip,
				Port:      port,
			})
			cache["connections"][cacheID] = true
		}
	}
	b, err := json.Marshal(behavior)
    	if err != nil {
        	fmt.Println(err)
        	return
    	}
    	fmt.Println(string(b))


}

